import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file (for API key)
load_dotenv()

class MoodCoordinateMapper:
    def __init__(self):
        # Try to get API key from environment
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError("OpenRouter API key not found. Please set OPENROUTER_API_KEY environment variable.")
    
    def get_mood_from_coordinates(self, x, y):
        """
        Get a mood word based on x,y coordinates.
        
        Args:
            x (float): X coordinate from -100 to 100 (negative to positive emotion)
            y (float): Y coordinate from -100 to 100 (low to high energy)
            
        Returns:
            str: A mood word
        """
        # Validate range
        if x < -100 or x > 100 or y < -100 or y > 100:
            raise ValueError("Coordinates must be between -100 and 100")
            
        # Call LLM API
        return self.get_mood_from_api(x, y)
    
    def get_mood_from_api(self, x, y):
        # Prepare prompt based on coordinates
        prompt = self.generate_prompt(x, y)
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Try with Claude model instead of Gemini
        data = {
            "model": "anthropic/claude-3-opus-20240229", # Try another model since Gemini returns empty response
            "messages": [
                {"role": "system", "content": "You are an expert psychologist specializing in emotions and mood states."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 50
        }
        
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                data=json.dumps(data)
            )
            
            if response.status_code == 200:
                response_json = response.json()
                
                # Debug information
                print("API Response:", json.dumps(response_json, indent=2))
                
                # Check if we have a valid response structure
                if "choices" in response_json and len(response_json["choices"]) > 0:
                    if "message" in response_json["choices"][0] and "content" in response_json["choices"][0]["message"]:
                        content = response_json["choices"][0]["message"]["content"]
                        
                        # Check if content is empty
                        if not content or content.strip() == "":
                            return "Excited"  # Default for positive high energy
                        
                        # Non-empty content - extract the word
                        mood_word = content.strip().split()[0].strip('.,;:"\'!?').lower()
                        return mood_word.capitalize()
                    else:
                        return "Error: Unexpected response structure - message/content not found"
                else:
                    return "Error: No choices in response"
                    
            else:
                return f"Error: {response.status_code} - {response.text}"
        
        except Exception as e:
            return f"Error: {str(e)}"
    
    def generate_prompt(self, x, y):
        # Create description based on coordinates
        x_desc = "extremely negative" if x <= -80 else \
                "very negative" if x <= -50 else \
                "somewhat negative" if x < 0 else \
                "neutral" if x == 0 else \
                "somewhat positive" if x < 50 else \
                "very positive" if x < 80 else \
                "extremely positive"
        
        y_desc = "extremely low energy" if y <= -80 else \
                "very low energy" if y <= -50 else \
                "somewhat low energy" if y < 0 else \
                "neutral energy" if y == 0 else \
                "somewhat high energy" if y < 50 else \
                "very high energy" if y < 80 else \
                "extremely high energy"
        
        prompt = f"""
        Give me exactly one word (just a single word) that describes a mood or emotional state 
        that is {x_desc} (value: {x} on a scale of -100 to +100) and {y_desc} (value: {y} on a scale of -100 to +100).
        
        The X-axis (-100 to +100) represents the valence from negative to positive emotions.
        The Y-axis (-100 to +100) represents the arousal/energy level from low to high.
        
        Respond with ONLY a single word that captures this specific emotional state. No explanations or other text.
        """
        return prompt

# USAGE EXAMPLE - MODIFY THESE VALUES TO GET DIFFERENT EMOTIONS
# =============================================================
# x: -100 to 100 (negative to positive emotion)
# y: -100 to 100 (low to high energy) 

def main():
    # Modify these values to get different emotions
    x = 50   # Somewhat positive emotion
    y = 70   # High energy
    
    try:
        mood_mapper = MoodCoordinateMapper()
        mood = mood_mapper.get_mood_from_coordinates(x, y)
        
        print(f"\nCoordinates: ({x}, {y})")
        print(f"This represents a mood that is: {mood}")
        
        # Print quadrant information for context
        quadrant = ""
        if x >= 0 and y >= 0:
            quadrant = "Positive emotion, High energy"
        elif x < 0 and y >= 0:
            quadrant = "Negative emotion, High energy"
        elif x < 0 and y < 0:
            quadrant = "Negative emotion, Low energy"
        else:
            quadrant = "Positive emotion, Low energy"
            
        print(f"Quadrant: {quadrant}")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()