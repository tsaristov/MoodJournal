import sqlite3
from datetime import datetime
import requests
import json
import os

# OpenRouter API settings
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = "anthropic/claude-3-haiku:beta"

# SQLite database file
DB_FILE = "journal.db"


def create_db():
    """Creates the database and table if it doesn't exist."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS journal_entries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        emotion TEXT NOT NULL,
        prompt TEXT NOT NULL,
        response TEXT NOT NULL
    )
    ''')

    conn.commit()
    conn.close()


def generate_prompt(emotion):
    """Generates a journal prompt based on the provided emotion using OpenRouter."""
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": f"You are a thoughtful, thought-provoking, and introspective journal prompt generator, specifically for the emotion {emotion}."},
            {"role": "user", "content": "Generate a journal prompt."}
        ],
        "temperature": 0.1
    }

    try:
        response = requests.post(OPENROUTER_API_URL, headers=headers, data=json.dumps(payload))
        response.raise_for_status()

        data = response.json()
        prompt = data['choices'][0]['message']['content'].strip()
        return prompt

    except Exception as e:
        print(f"Error generating prompt: {e}")
        return "Describe how you're feeling right now."


def save_entry(emotion, prompt, response):
    """Saves the journal entry to the SQLite database."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO journal_entries (timestamp, emotion, prompt, response)
    VALUES (?, ?, ?, ?)
    ''', (timestamp, emotion, prompt, response))

    conn.commit()
    conn.close()


if __name__ == "__main__":
    # Test database creation
    print("Testing database creation...")
    create_db()
    print("✓ Database created successfully\n")

    # Test prompt generation with a sample emotion
    test_emotion = "Excited"
    print(f"Testing prompt generation for emotion: {test_emotion}")
    prompt = generate_prompt(test_emotion)
    print(f"Generated prompt: {prompt}\n")

    # Test saving an entry with sample data
    test_response = "This is a test journal response."
    print("Testing database entry...")
    try:
        save_entry(test_emotion, prompt, test_response)
        print("✓ Entry saved successfully\n")

        # Verify the entry was saved by reading from the database
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM journal_entries ORDER BY id DESC LIMIT 1")
        last_entry = cursor.fetchone()
        print("Last entry in database:")
        print(f"Timestamp: {last_entry[1]}")
        print(f"Emotion: {last_entry[2]}")
        print(f"Prompt: {last_entry[3]}")
        print(f"Response: {last_entry[4]}")
        conn.close()
    except Exception as e:
        print(f"Error during testing: {e}")

