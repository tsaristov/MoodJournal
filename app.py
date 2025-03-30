from flask import Flask, render_template, request, jsonify, redirect, url_for
import sqlite3
from datetime import datetime, timedelta
import json
from mood_picker import MoodCoordinateMapper
from prompt_gen import generate_prompt, save_entry, create_db

app = Flask(__name__)

# Ensure database exists
create_db()

def get_color_from_coordinates(x, y):
    """Generate a color based on x,y coordinates"""
    # Normalize coordinates from -100,100 to 0,1 range
    x_norm = (x + 100) / 200
    y_norm = (y + 100) / 200
    
    # Make colors more vibrant by increasing saturation
    h = (x_norm * 360) % 360  # Hue based on x (negative to positive)
    s = 0.7  # Fixed saturation
    l = 0.2 + (y_norm * 0.6)  # Lightness based on y (low to high energy)
    
    return f"hsl({h}, {s*100}%, {l*100}%)"

@app.route('/')
def home():
    """Render the main page with journal entries and mood chart"""
    # Get time period from query params, default to 'week'
    time_period = request.args.get('time_period', 'week')
    
    # Get journal entries
    entries = get_journal_entries(time_period)
    
    # Get emotion data for chart
    emotion_data = get_emotion_data(time_period)
    
    return render_template(
        'index.html', 
        entries=entries, 
        emotion_data=json.dumps(emotion_data),
        selected_period=time_period,
        get_color_from_coordinates=get_color_from_coordinates
    )

@app.route('/get_emotion', methods=['POST'])
def get_emotion():
    """Get emotion from coordinates or direct input"""
    try:
        data = request.json
        
        if 'coordinates' in data:
            x = data['coordinates']['x']
            y = data['coordinates']['y']
            
            try:
                mapper = MoodCoordinateMapper()
                emotion = mapper.get_mood_from_coordinates(x, y)
                return jsonify({'emotion': emotion, 'coordinates': {'x': x, 'y': y}})
            except Exception as e:
                app.logger.error(f"Error getting mood from coordinates: {str(e)}")
                return jsonify({'error': str(e)}), 400
        
        elif 'emotion' in data:
            return jsonify({'emotion': data['emotion'].capitalize()})
        
        return jsonify({'error': 'Invalid request - missing emotion or coordinates'}), 400
    except Exception as e:
        app.logger.error(f"Error in get_emotion endpoint: {str(e)}")
        return jsonify({'error': 'Server error processing request'}), 500

@app.route('/get_prompt', methods=['POST'])
def get_journal_prompt():
    """Get a journal prompt based on emotion"""
    try:
        data = request.json
        emotion = data.get('emotion')
        
        if not emotion:
            return jsonify({'error': 'Emotion is required'}), 400
        
        prompt = generate_prompt(emotion)
        return jsonify({'prompt': prompt})
    except Exception as e:
        app.logger.error(f"Error in get_prompt endpoint: {str(e)}")
        return jsonify({'error': 'Server error generating prompt'}), 500

@app.route('/save_entry', methods=['POST'])
def save_journal_entry():
    """Save journal entry to database"""
    data = request.json
    emotion = data.get('emotion')
    prompt = data.get('prompt')
    response = data.get('response')
    coordinates = data.get('coordinates')
    
    if not all([emotion, prompt, response]):
        return jsonify({'error': 'All fields are required'}), 400
    
    try:
        x_coordinate = None
        y_coordinate = None
        if coordinates and 'x' in coordinates and 'y' in coordinates:
            x_coordinate = coordinates['x']
            y_coordinate = coordinates['y']
            
        save_entry(emotion, prompt, response, x_coordinate, y_coordinate)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_journal_entries(time_period='week'):
    """Get journal entries for the specified time period"""
    conn = sqlite3.connect('journal.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Calculate date range based on time period
    end_date = datetime.now()
    
    if time_period == 'week':
        start_date = end_date - timedelta(days=7)
    elif time_period == 'month':
        start_date = end_date - timedelta(days=30)
    elif time_period == 'year':
        start_date = end_date - timedelta(days=365)
    else:  # all time
        start_date = datetime.strptime('1970-01-01', '%Y-%m-%d')
    
    # Format dates for SQLite query
    start_str = start_date.strftime('%Y-%m-%d %H:%M:%S')
    end_str = end_date.strftime('%Y-%m-%d %H:%M:%S')
    
    cursor.execute('''
    SELECT id, timestamp, emotion, prompt, response, x_coordinate, y_coordinate
    FROM journal_entries
    WHERE timestamp BETWEEN ? AND ?
    ORDER BY timestamp DESC
    ''', (start_str, end_str))
    
    entries = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return entries

def get_emotion_data(time_period='week'):
    """Get emotion data for chart visualization"""
    conn = sqlite3.connect('journal.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Calculate date range based on time period
    end_date = datetime.now()
    
    if time_period == 'week':
        start_date = end_date - timedelta(days=7)
    elif time_period == 'month':
        start_date = end_date - timedelta(days=30)
    elif time_period == 'year':
        start_date = end_date - timedelta(days=365)
    else:  # all time
        start_date = datetime.strptime('1970-01-01', '%Y-%m-%d')
    
    # Format dates for SQLite query
    start_str = start_date.strftime('%Y-%m-%d %H:%M:%S')
    end_str = end_date.strftime('%Y-%m-%d %H:%M:%S')
    
    cursor.execute('''
    SELECT emotion, COUNT(*) as count, timestamp
    FROM journal_entries
    WHERE timestamp BETWEEN ? AND ?
    GROUP BY emotion
    ORDER BY count DESC
    ''', (start_str, end_str))
    
    emotions = [dict(row) for row in cursor.fetchall()]
    
    # Get all entries for timeline data
    cursor.execute('''
    SELECT emotion, timestamp
    FROM journal_entries
    WHERE timestamp BETWEEN ? AND ?
    ORDER BY timestamp
    ''', (start_str, end_str))
    
    timeline = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return {
        'emotions': emotions,
        'timeline': timeline
    }

if __name__ == '__main__':
    app.run(debug=True)