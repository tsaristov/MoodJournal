### Project Title: Mood-Based Daily Journal

### Project Overview
The Mood-Based Daily Journal is a desktop or mobile application that leverages AI to create personalized daily journal prompts based on the user's self-reported mood. Users can input their mood, receive a tailored prompt, write their journal entry, and save it locally in a local database for future reflection. The goal is to encourage consistent journaling by making it engaging and emotionally relevant.

---

### Project Objectives
1. Develop an AI-driven system to generate creative, mood-specific journal prompts.
2. Create a user-friendly interface for mood input and journal entry.
3. Implement secure, local storage for journal entries (lightweight database `sqlite3`).
4. Provide a feature to review past entries by date or mood.

---

### Project Scope
- **In Scope**: Mood detection via user input, AI prompt generation, local storage, entry review.
- **Out of Scope**: Cloud storage, social sharing features, advanced natural language processing for entry analysis.

---

### Project Phases and Tasks

#### Phase 1: Planning and Research
- **Tasks**:
  1. Define mood categories, and then sub-categories (on a graphical scale, further on positive end of x-axis is positive emotions, further on negative end of x-axis is negative emotions, further on positive end of y-axis is high energy emotions, further on negative end of y-axis is low energy emotions).
  3. Choose a programming language and framework (We are using python for backend, and flask for UI).
  5. Outline basic UI/UX requirements and ideas.

#### Phase 2: Design
- **Tasks**:
  1. Design a simple UI mockup (mood input screen, prompt display, journal entry area).
  2. Create a database schema (if using SQLite).
  4. Plan data flow: mood input → AI journal prompt → user entry → local save.

#### Phase 3: Development
- **Tasks**:
  1. **Backend**:
     - Implement mood input system (e.g., dropdown or buttons for mood selection).
     - Build AI prompt generator (e.g., use a simple rule-based system or integrate a lightweight LLM like Grok).
     - Set up local storage (e.g., save entries as timestamped text files or database records).
  2. **Frontend**:
     - Develop the UI for mood selection, prompt display, and text entry.
     - Add a "Save" button to store entries and a "View Past Entries" option.
  3. Test core functionality (mood → prompt → save).

---

### Tech Stack (Suggested)
- **Programming Language**: Python (for simplicity and AI integration) or Dart (for mobile with Flutter).
- **UI Framework**: Tkinter (Python desktop), PyQt (alternative), or Flutter (cross-platform).
- **AI Component**: Rule-based prompt system or lightweight API integration with an AI model.
- **Storage**: SQLite (structured database) or plain text files (simpler).
- **Libraries**: 
  - Python: `datetime` (timestamps), `sqlite3` (database).

---

### UI Planning
1. First screen: A page where you can scroll through past prompts, and choose to enter a new prompt. 
2. Mood Chooser: After they choose to enter a new prompt, it scrolls down to the mood quadrant chooser (when hovering over a certain part of the graph, a word comes up describing the emotion at that point).
3. Then the screen scrolls down to a journal prompt comes up, and below it a text box so the user can respond to the prompt.
3. After they respond, it scrolls all the way to the top.

---

### Deliverables
1. A functional application with:
   - Mood input interface.
   - AI-generated journal prompts.
   - Local storage for entries.
   - Basic entry retrieval system.
2. Source code with comments.
3. User guide (text or PDF).

---

### Potential Challenges
1. Ensuring prompt variety and relevance without an internet-dependent AI model.
2. Balancing simplicity (local storage) with usability (entry retrieval).
3. Handling edge cases (e.g., no mood selected, large journal entries).

---

### Future Enhancements
- Add mood analysis over time (e.g., mood trends).
- Allow export/import of journal entries.
- Integrate voice input for mood or journal entries.
- Offer customizable prompt styles.