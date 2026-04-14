
# 🤖 NexusAI — Production-Level AI Chatbot

A full-stack, production-grade AI chatbot built with Python, Flask, and the OpenAI API.
Features context-aware conversations, user authentication, persistent chat history,
intent recognition, and a sleek dark-mode web interface.

---

## ✨ Features

| Feature | Details |
|---|---|
| 🧠 AI-Powered | OpenAI GPT-3.5-turbo with multi-turn context |
| 🔍 Intent Recognition | Keyword-based NLP (greeting, farewell, help, etc.) |
| 💾 Chat Persistence | SQLite DB — history survives restarts |
| 🔐 User Auth | Register/login with SHA-256 password hashing |
| 🌐 Web UI | Flask + responsive dark-mode frontend |
| 📋 Logging | Rotating file logs + console output |
| ⚙️ Configurable | Swap model, temperature, system prompt in one dict |
| 🚀 Deploy-Ready | Environment variables, requirements.txt, Render-ready |

---

## 🚀 Quick Start

### 1. Clone & Install
```bash
git clone https://github.com/yourname/nexusai-chatbot.git
cd nexusai-chatbot
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY and SECRET_KEY
```

### 3. Run
```bash
python app.py
# Visit http://localhost:5000
```

---

## 🏗️ Project Structure

```
nexusai-chatbot/
├── app.py                  # Main Flask application
├── templates/
│   ├── index.html          # Chat interface
│   └── auth.html           # Login / Register page
├── requirements.txt
├── .env.example
├── chatbot.db              # Auto-created SQLite database
├── chatbot.log             # Auto-created log file
└── README.md
```

---

## 🌐 Deployment

### Deploy to Render (Free)
1. Push repo to GitHub
2. Go to [render.com](https://render.com) → New Web Service
3. Connect your GitHub repo
4. Set Build Command: `pip install -r requirements.txt`
5. Set Start Command: `gunicorn app:app`
6. Add environment variables: `OPENAI_API_KEY`, `SECRET_KEY`
7. Deploy!

### Deploy to HuggingFace Spaces
Use the Gradio or Docker SDK option and wrap `app.py` in a Gradio interface.

---

## 🔧 Configuration

All bot settings live in the `BOT_CONFIG` dict in `app.py`:

```python
BOT_CONFIG = {
    "name": "NexusAI",
    "model": "gpt-3.5-turbo",   # or "gpt-4"
    "max_tokens": 512,
    "temperature": 0.7,          # 0 = deterministic, 1 = creative
    "system_prompt": "...",      # personality/instructions
    "max_history_turns": 10,     # conversation memory depth
}
```

---


**Key Technologies:** Python · Flask · OpenAI API · SQLite · HTML/CSS/JS · REST APIs · NLP

**Impact:** Transformed a 40-line rule-based script into a deployable, multi-user AI
application demonstrating full-stack engineering, API integration, and software design
principles relevant to AI/ML engineering roles.

---

## 📜 License
MIT
=======
# AI Chatbot 🤖

A simple AI chatbot built using Python that responds to basic user inputs.

## Features
- Handles greetings
- Simple conversation
- Beginner-friendly

## Technologies Used
- Python

## How to Run
```bash
python chatbot.py


---

#
