# ROKA Bot

ROKA Bot is a lightweight, aesthetic, and rule-based conversational assistant built with Python and Flask. It uses fuzzy matching logic to understand user intent even when there are typos, providing a more versatile experience than standard keyword-matching bots.

## Features

* **Intelligent Logic**: Uses the `thefuzz` library to handle typos and variations in user input.
* **Modern UI**: A glassmorphic design interface with smooth animations and responsive layouts.
* **Theme Toggle**: Built-in light and dark mode support that persists during the session.
* **Scalable Architecture**: Organized for easy expansion of intents and responses.
* **Vercel Ready**: Pre-configured for deployment as a serverless function.

## Tech Stack

* **Backend**: Python 3.9+, Flask
* **Frontend**: HTML5, CSS3 (Custom Variables), JavaScript (Fetch API)
* **Matching**: Levenshtein distance matching via `thefuzz`
* **Deployment**: Vercel (Serverless Functions)

## Project Structure

```text
├── api/
│   └── index.py       # Main Flask application and bot logic
├── public/
│   └── index.html     # Frontend interface and styling
├── requirements.txt   # Python dependencies
└── vercel.json        # Deployment and routing configuration
