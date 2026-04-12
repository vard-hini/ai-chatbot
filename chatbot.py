# Simple AI Chatbot using Python

import random

# Predefined responses
responses = {
    "hello": ["Hi there!", "Hello!", "Hey! How can I help you?"],
    "how are you": ["I'm fine, thank you!", "Doing great!", "All good!"],
    "bye": ["Goodbye!", "See you later!", "Bye! Have a nice day!"],
    "your name": ["I am a simple AI chatbot.", "You can call me ChatBot!"],
}

def chatbot():
    print("🤖 ChatBot: Hello! Type 'bye' to exit.")
    
    while True:
        user_input = input("You: ").lower()

        if user_input == "bye":
            print("🤖 ChatBot: Goodbye!")
            break

        found = False

        for key in responses:
            if key in user_input:
                print("🤖 ChatBot:", random.choice(responses[key]))
                found = True
                break

        if not found:
            print("🤖 ChatBot: Sorry, I don't understand that.")

# Run chatbot
if __name__ == "__main__":
    chatbot()
    