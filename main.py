import sys
from mood_picker import MoodCoordinateMapper
from prompt_gen import generate_prompt, save_entry, create_db

def get_emotion():
    """
    Get emotion either through coordinates or direct input
    Returns tuple of (emotion, coordinates or None)
    """
    while True:
        method = input("\nHow would you like to input your emotion?\n1. Use coordinates\n2. Enter emotion directly\nChoice (1/2): ").strip()
        
        if method == "1":
            try:
                # Get and validate coordinates
                x = float(input("\nEnter X coordinate (-100 to 100, negative=bad to positive=good): "))
                y = float(input("Enter Y coordinate (-100 to 100, low to high energy): "))
                
                mapper = MoodCoordinateMapper()
                emotion = mapper.get_mood_from_coordinates(x, y)
                return emotion, (x, y)
                
            except ValueError as e:
                print(f"\nError: {e}. Please try again.")
            except Exception as e:
                print(f"\nUnexpected error: {e}. Please try again.")
                
        elif method == "2":
            emotion = input("\nEnter your emotion (e.g., happy, sad, anxious): ").strip().lower()
            return emotion, None
            
        print("\nInvalid choice. Please enter 1 or 2.")

def get_journal_response(prompt):
    """
    Get multi-line journal response from user
    """
    print("\n---\n\nWrite your journal entry (press Enter twice to finish):")
    print(f"Prompt: {prompt}\n")
    
    lines = []
    while True:
        line = input()
        if line == "" and (not lines or lines[-1] == ""):
            break
        lines.append(line)
    
    return "\n".join(lines[:-1])  # Remove the last empty line

def main():
    """
    Main CLI interface for the mood journal
    """
    try:
        # Ensure database exists
        create_db()
        
        print("\n=== Welcome to Your Mood Journal ===")
        
        # Get emotion input
        emotion, coordinates = get_emotion()
        print(f"\nRecorded emotion: {emotion.capitalize()}")
        
        # Generate and display prompt
        prompt = generate_prompt(emotion)
        
        # Get journal response
        response = get_journal_response(prompt)
        
        # Save to database
        save_entry(emotion, prompt, response)
        
        print("\n✓ Journal entry saved successfully!")
        
        # Display coordinates if they were used
        if coordinates:
            print(f"Coordinates used: x={coordinates[0]}, y={coordinates[1]}")
            
    except KeyboardInterrupt:
        print("\n\nJournal entry cancelled.")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()