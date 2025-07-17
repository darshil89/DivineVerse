# DivineVerse

A knowledge graph-powered chatbot for exploring the stories, meanings, and mantras of deities.

![Chat UI Screenshot](assets/chat-ui.png)

## Overview
DivineVerse is an interactive web app that lets you ask questions about Hindu gods and receive insightful stories, meanings, and mantras, powered by a Neo4j knowledge graph and OpenAI.

## Features
- Chatbot interface for natural language queries
- Retrieves stories, meanings, and mantras of deities
- Powered by a vector search over a Neo4j graph database
- Modern, user-friendly UI with emoji-enhanced chat

## Tech Stack
- Python (FastAPI, Streamlit)
- Neo4j (graph database)
- OpenAI (LLM for story generation)

## Setup Instructions
1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd <repo-folder>
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Set up environment variables:**
   - Create a `.env` file with your OpenAI and Neo4j credentials.
4. **Start the backend:**
   ```bash
   uvicorn main:app --reload
   ```
5. **Start the frontend:**
   ```bash
   streamlit run app.py
   ```

## Usage
- Open the Streamlit app in your browser.
- Type your question about any Hindu deity.
- Receive a story, meaning, and mantra in response.

## API
- **POST `/chat`**: Send `{ "text": "your question" }` and receive a story about the deity.

## Screenshots

| Chat UI | Backend API |
|---------|------------|
| ![Chat UI](screenshots/chat-ui.png) | ![API Example](screenshots/api-example.png) |

> _Replace the above image paths with your actual screenshots after running the app._

## License
MIT 
