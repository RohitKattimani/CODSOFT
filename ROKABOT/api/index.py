from flask import Flask, request, jsonify
from thefuzz import process
import random

app = Flask(__name__)

CHAT_DATA = {
    "greeting": {
        "keywords": ["hi", "hello", "hey", "hola", "greetings", "sup"],
        "responses": ["Hello there!", "Hey! How's it going?", "Hi! What can I do for you?"]
    },
    "mood": {
        "keywords": ["how are you", "how's it going", "how do you feel"],
        "responses": ["I'm doing great, thanks for asking!", "Full of energy and ready to chat!", "I'm just code, but I'm having a 10/10 day."]
    },
    "capabilities": {
        "keywords": ["help", "what can you do", "commands", "functions"],
        "responses": ["I can chat, tell you the time, or just keep you company!", "I'm a rule-based bot. Ask me how I'm doing or say goodbye!"]
    },
    "joke": {
        "keywords": ["joke", "funny", "tell me something funny"],
        "responses": [
            "Why did the programmer quit his job? Because he didn't get arrays (a raise).",
            "Hardware: The part of a computer that you can kick.",
            "A SQL query walks into a bar, walks up to two tables, and asks, 'Can I join you?'"
        ]
    },
    "goodbye": {
        "keywords": ["bye", "goodbye", "see ya", "exit", "later"],
        "responses": ["See you later!", "Goodbye!", "Have a fantastic day!"]
    }
}

def get_enhanced_response(user_input):
    user_input = user_input.lower().strip()
    
    # I'll Check for exact or partial keyword matches
    for intent, data in CHAT_DATA.items():
        for keyword in data["keywords"]:
            # I'm using Fuzzy match as it checks if the keyword is roughly 85% similar to the input
            match_score = process.extractOne(user_input, data["keywords"])
            
            if match_score[1] > 85:
                return random.choice(data["responses"])

    # 2. special "Dynamic" rule (e.g., Time)
    if "time" in user_input:
        from datetime import datetime
        return f"The current time is {datetime.now().strftime('%H:%M')}."

    # Catch-all fallback
    return "I'm still learning! Try asking me for a joke or say hello."

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get("message", "")
    response = get_enhanced_response(user_message)
    return jsonify({"response": response})

def handler(event, context):
    return app(event, context)