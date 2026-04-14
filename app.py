"""
🤖 Advanced AI Chatbot — Production-Level
==========================================
Author: Your Name
Description: A production-grade AI chatbot with NLP, context awareness,
             user auth, chat history, and a Flask web interface.
"""

import os
import json
import logging
import hashlib
import sqlite3
from datetime import datetime
from functools import wraps
from dotenv import load_dotenv
from flask import Flask, request, jsonify, session, render_template, redirect, url_for
from openai import OpenAI

# ── Load environment variables ──────────────────────────────────────────────
load_dotenv()

# ── App Setup ────────────────────────────────────────────────────────────────
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "change-me-in-production")

# ── Logging ──────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler("chatbot.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ── OpenAI Client ────────────────────────────────────────────────────────────
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", "your-api-key-here"))

# ── Config ───────────────────────────────────────────────────────────────────
BOT_CONFIG = {
    "name": "NexusAI",
    "model": "gpt-3.5-turbo",
    "max_tokens": 512,
    "temperature": 0.7,
    "system_prompt": (
        "You are NexusAI, a helpful, concise, and friendly AI assistant. "
        "You remember the context of the conversation and give thoughtful, "
        "accurate responses. Keep answers clear and to the point."
    ),
    "max_history_turns": 10,   # number of message pairs to retain in context
}

# ── Database Setup ───────────────────────────────────────────────────────────
DB_PATH = "chatbot.db"

def init_db():
    """Initialize SQLite database with users and messages tables."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id       INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT    UNIQUE NOT NULL,
                password TEXT    NOT NULL,
                created  TEXT    DEFAULT (datetime('now'))
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                username   TEXT NOT NULL,
                role       TEXT NOT NULL,   -- 'user' or 'assistant'
                content    TEXT NOT NULL,
                intent     TEXT,
                timestamp  TEXT DEFAULT (datetime('now'))
            )
        """)
    logger.info("Database initialized.")

init_db()

# ── Auth Helpers ─────────────────────────────────────────────────────────────
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def login_required(f):
    """Decorator: redirect unauthenticated users to /login."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if "username" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated

# ── NLP: Intent Detection ─────────────────────────────────────────────────────
INTENT_PATTERNS = {
    "greeting":    ["hello", "hi", "hey", "good morning", "good evening"],
    "farewell":    ["bye", "goodbye", "see you", "quit", "exit"],
    "help":        ["help", "what can you do", "commands", "assist"],
    "identity":    ["your name", "who are you", "what are you"],
    "weather":     ["weather", "temperature", "forecast"],
    "general":     [],
}

def detect_intent(text: str) -> str:
    """Simple keyword-based intent detection."""
    text_lower = text.lower()
    for intent, keywords in INTENT_PATTERNS.items():
        if any(kw in text_lower for kw in keywords):
            return intent
    return "general"

# ── Context / History Management ─────────────────────────────────────────────
def load_history(username: str) -> list[dict]:
    """Load the last N turns from the database for context."""
    limit = BOT_CONFIG["max_history_turns"] * 2  # each turn = user + assistant
    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute(
            "SELECT role, content FROM messages WHERE username=? "
            "ORDER BY id DESC LIMIT ?",
            (username, limit)
        ).fetchall()
    return [{"role": r, "content": c} for r, c in reversed(rows)]

def save_message(username: str, role: str, content: str, intent: str = None):
    """Persist a message to the database."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO messages (username, role, content, intent) VALUES (?,?,?,?)",
            (username, role, content, intent)
        )

# ── AI Response ───────────────────────────────────────────────────────────────
def get_ai_response(username: str, user_message: str) -> dict:
    """
    Build context-aware prompt and call the OpenAI API.
    Returns dict with 'reply', 'intent', 'model'.
    """
    intent = detect_intent(user_message)
    logger.info(f"[{username}] Intent: {intent} | Message: {user_message[:60]}")

    # Build message list: system + history + new user message
    history = load_history(username)
    messages = [{"role": "system", "content": BOT_CONFIG["system_prompt"]}]
    messages += history
    messages.append({"role": "user", "content": user_message})

    try:
        completion = client.chat.completions.create(
            model=BOT_CONFIG["model"],
            messages=messages,
            max_tokens=BOT_CONFIG["max_tokens"],
            temperature=BOT_CONFIG["temperature"],
        )
        reply = completion.choices[0].message.content.strip()
        logger.info(f"[{username}] Bot replied ({len(reply)} chars)")
    except Exception as e:
        logger.error(f"OpenAI API error: {e}")
        reply = "I'm having trouble connecting right now. Please try again in a moment."

    # Persist both turns
    save_message(username, "user", user_message, intent)
    save_message(username, "assistant", reply)

    return {"reply": reply, "intent": intent, "model": BOT_CONFIG["model"]}

# ── Routes ────────────────────────────────────────────────────────────────────

@app.route("/")
@login_required
def index():
    return render_template("index.html", bot_name=BOT_CONFIG["name"],
                           username=session["username"])

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        data = request.get_json()
        username = data.get("username", "").strip()
        password = data.get("password", "").strip()
        if not username or not password:
            return jsonify({"error": "Username and password required."}), 400
        try:
            with sqlite3.connect(DB_PATH) as conn:
                conn.execute("INSERT INTO users (username, password) VALUES (?,?)",
                             (username, hash_password(password)))
            logger.info(f"New user registered: {username}")
            return jsonify({"message": "Registration successful!"})
        except sqlite3.IntegrityError:
            return jsonify({"error": "Username already exists."}), 409
    return render_template("auth.html", mode="register")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.get_json()
        username = data.get("username", "").strip()
        password = data.get("password", "").strip()
        with sqlite3.connect(DB_PATH) as conn:
            row = conn.execute(
                "SELECT id FROM users WHERE username=? AND password=?",
                (username, hash_password(password))
            ).fetchone()
        if row:
            session["username"] = username
            logger.info(f"User logged in: {username}")
            return jsonify({"message": "Login successful!"})
        return jsonify({"error": "Invalid credentials."}), 401
    return render_template("auth.html", mode="login")

@app.route("/logout")
def logout():
    username = session.pop("username", None)
    logger.info(f"User logged out: {username}")
    return redirect(url_for("login"))

@app.route("/chat", methods=["POST"])
@login_required
def chat():
    data = request.get_json()
    user_message = (data.get("message") or "").strip()
    if not user_message:
        return jsonify({"error": "Empty message."}), 400
    result = get_ai_response(session["username"], user_message)
    return jsonify(result)

@app.route("/history")
@login_required
def history():
    """Return the full chat history for the logged-in user as JSON."""
    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute(
            "SELECT role, content, intent, timestamp FROM messages WHERE username=? ORDER BY id",
            (session["username"],)
        ).fetchall()
    msgs = [{"role": r, "content": c, "intent": i, "timestamp": t}
            for r, c, i, t in rows]
    return jsonify({"history": msgs})

@app.route("/clear", methods=["POST"])
@login_required
def clear_history():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DELETE FROM messages WHERE username=?", (session["username"],))
    logger.info(f"Chat history cleared for: {session['username']}")
    return jsonify({"message": "Chat history cleared."})

# ── Entry Point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG", "false").lower() == "true", port=5000)
