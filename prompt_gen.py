import sqlite3
from datetime import datetime
import requests
import json
import os
import random

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
    
    # First check if the table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='journal_entries'")
    table_exists = cursor.fetchone() is not None
    
    if not table_exists:
        # Create the table if it doesn't exist
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS journal_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            emotion TEXT NOT NULL,
            prompt TEXT NOT NULL,
            response TEXT NOT NULL,
            x_coordinate INTEGER,
            y_coordinate INTEGER
        )
        ''')
        conn.commit()
    else:
        # Check if the coordinates columns exist
        cursor.execute("PRAGMA table_info(journal_entries)")
        columns = [column[1] for column in cursor.fetchall()]
        
        # Add coordinates columns if they don't exist
        if 'x_coordinate' not in columns:
            cursor.execute('ALTER TABLE journal_entries ADD COLUMN x_coordinate INTEGER')
        if 'y_coordinate' not in columns:
            cursor.execute('ALTER TABLE journal_entries ADD COLUMN y_coordinate INTEGER')
        conn.commit()
        
    conn.close()

def generate_custom_prompt(emotion):
    """Generates a more focused prompt based on the provided emotion using OpenRouter."""
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # More specific system prompt with examples and constraints
    system_prompt = f"""You are a thoughtful, introspective journal prompt creator focused on the emotion: {emotion}.
    
    Your prompt should:
    1. Be specific and thought-provoking
    2. NEVER simply say "Describe how you're feeling right now"
    3. Include elements that encourage reflection on causes, effects, and personal growth
    4. Be 1-2 sentences maximum
    5. Always relate directly to the emotion: {emotion}
    
    Examples of good prompts for "anxious":
    - "Describe a physical sensation you associate with anxiety and how it manifests in your body today."
    - "Write about one source of your anxiety that you might be able to turn into a positive action step."
    - "What would you tell your anxiety if it were a person sitting across from you right now?"

    Please only provide the journal prompt, and no other commentary.
    """
    
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Create a unique journal prompt for someone feeling {emotion} that encourages deeper reflection."}
        ],
        "temperature": 0.7  # Increased temperature for more variation
    }
    
    try:
        response = requests.post(OPENROUTER_API_URL, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        data = response.json()
        prompt = data['choices'][0]['message']['content'].strip()
        return prompt
    except Exception as e:
        return use_fallback_prompt(emotion)

def use_fallback_prompt(emotion):
    """Provides a fallback prompt if API call fails, with varied prompts based on emotion."""
    emotion_prompts = {
        "happy": [
            f"What's one small thing contributing to your happiness today that you might normally overlook?",
            f"How is your current happiness influencing how you interact with others?",
            f"Describe a way you could channel this happiness into something creative or productive."
        ],
        "sad": [
            f"What would you tell someone else who's feeling the same sadness you're experiencing?",
            f"Is there a pattern to when this sadness appears in your life?",
            f"Write about one tiny action that might bring a moment of comfort right now."
        ],
        "angry": [
            f"If your anger could speak, what would be its main message to you?",
            f"What boundary might need reinforcing related to this anger?",
            f"Describe how the physical sensations of anger move through your body."
        ],
        "anxious": [
            f"What's one small step you could take to address a source of your anxiety?",
            f"How might this anxiety be trying to protect you?",
            f"Write about the difference between productive and unproductive worries you're experiencing."
        ],
        "excited": [
            f"How can you channel this excitement into something meaningful?",
            f"What does this excitement tell you about your values and what matters to you?",
            f"Describe how this excitement feels different from other positive emotions."
        ]
    }
    
    # Default prompts for any emotion not specifically covered
    default_prompts = [
        f"Explore one trigger that intensified your feeling of {emotion} recently.",
        f"Write about how being {emotion} affects your decision-making process.",
        f"What would you like others to understand about you when you're feeling {emotion}?",
        f"Describe how the feeling of being {emotion} manifests physically in your body.",
        f"How might this experience of feeling {emotion} be helping you grow?"
    ]
    
    # Use emotion-specific prompts if available, otherwise use default
    prompts = emotion_prompts.get(emotion.lower(), default_prompts)
    return random.choice(prompts)

def generate_prompt(emotion):
    """Tries the API first, then falls back to custom prompts if needed."""
    prompt = generate_custom_prompt(emotion)
    
    # If the prompt is the generic one or too short, use fallback
    if prompt == "Describe how you're feeling right now" or len(prompt) < 20:
        prompt = use_fallback_prompt(emotion)
        
    return prompt

def save_entry(emotion, prompt, response, x_coordinate=None, y_coordinate=None):
    """Saves the journal entry to the SQLite database."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # If coordinates are provided, save them too
    if x_coordinate is not None and y_coordinate is not None:
        cursor.execute('''
        INSERT INTO journal_entries (timestamp, emotion, prompt, response, x_coordinate, y_coordinate)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (timestamp, emotion, prompt, response, x_coordinate, y_coordinate))
    else:
        cursor.execute('''
        INSERT INTO journal_entries (timestamp, emotion, prompt, response)
        VALUES (?, ?, ?, ?)
        ''', (timestamp, emotion, prompt, response))
        
    conn.commit()
    conn.close()