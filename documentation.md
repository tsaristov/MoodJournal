# Mood-Based Daily Journal Documentation

## Commit Message
```
feat: Implement Mood Coordinate Mapping System

- Add MoodCoordinateMapper class for emotion mapping
- Integrate OpenRouter API for mood word generation
- Implement coordinate-based mood determination system
- Add error handling and input validation
- Include comprehensive documentation and usage examples

The system uses a 2D coordinate space (-100 to 100) to map emotions:
- X-axis: Emotional valence (negative to positive)
- Y-axis: Energy/arousal level (low to high)

Technical details:
- Uses OpenRouter API with Claude-3-Opus model
- Implements robust error handling and fallbacks
- Includes environment variable configuration for API keys
- Provides clear documentation and usage examples
```

## Project Overview
The Mood-Based Daily Journal project currently implements a sophisticated mood mapping system that converts numerical coordinates into meaningful emotional states. The system uses a two-dimensional coordinate space where:

- The X-axis represents emotional valence (ranging from -100 to +100)
- The Y-axis represents energy/arousal level (ranging from -100 to +100)

### Key Features
1. **Coordinate-Based Mood Mapping**
   - Precise emotional state determination based on x,y coordinates
   - Input validation to ensure coordinates are within valid ranges
   - Quadrant-based emotional categorization

2. **AI-Powered Mood Word Generation**
   - Integration with OpenRouter API
   - Uses Claude-3-Opus model for accurate emotional state description
   - Single-word response format for clarity
   - Fallback mechanisms for API failures

3. **Journal Prompt Generation System**
   - AI-powered prompt generation using OpenRouter API
   - Uses Qwen 2.5 VL model for creative and contextual prompts
   - Temperature-controlled response generation (0.7) for balanced creativity
   - Fallback to default prompt if API fails

4. **Database Integration**
   - SQLite-based local storage system
   - Structured schema for journal entries including:
     * Timestamp tracking
     * Emotion recording
     * Prompt storage
     * User response storage
   - Automatic database creation and management

5. **Robust Error Handling**
   - Comprehensive input validation
   - API error handling and fallback mechanisms
   - Clear error messages and debugging information
   - Database transaction safety

### Usage
The system provides multiple interfaces:

1. Mood Coordinate Mapping:
```python
mood_mapper = MoodCoordinateMapper()
mood = mood_mapper.get_mood_from_coordinates(x, y)
```

2. Journal Entry Creation:
```python
prompt = generate_prompt(emotion)
save_entry(emotion, prompt, user_response)
```

### Technical Details
- Database: SQLite3 with local storage
- API Integration: OpenRouter API with multiple model support
  * Claude-3-Opus for mood determination
  * Qwen 2.5 VL for prompt generation
- Environment Configuration: Uses .env for API key management
- Error Handling: Comprehensive try-catch blocks with meaningful fallbacks

### Future Enhancements
- [ ] Add mood history tracking
- [ ] Implement mood visualization
- [ ] Add support for multiple languages
- [ ] Include mood trend analysis
- [ ] Add user authentication and personalization 