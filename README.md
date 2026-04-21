#Streaming Voice AI Assistant (JARVIS)

A real-time 'voice-enabled AI assistant' built using *FastAPI + Groq API*, inspired by Tony Stark’s JARVIS.  
It supports *speech-to-text, AI streaming responses, and text-to-speech*, creating a smooth conversational experience in the browser.

---

#Features

- Voice input using Web Speech API (Chrome supported)
- AI responses via Groq (Llama 3.1 model)
- Real-time streaming responses (token-by-token)
- Text-to-speech (browser-based TTS)
- Chat-style UI with user/bot messages
- Short-term memory per session
- FastAPI backend with CORS support
- Lightweight & deployable (Render / Docker ready)

---

#Tech Stack

#Backend
- FastAPI
- Uvicorn
- Groq API (LLM inference)
- Pydantic

### Frontend
- HTML
- CSS
- Vanilla JavaScript
- Web Speech API

### Deployment
- Docker
- Render (free tier compatible)

---

## Project Structure

```
Streaming Voicebot/
│
├── app/
│ └── main.py # FastAPI backend
│
├── templates/
│ └── index.html # Frontend UI
│
├── static/ # Optional assets
│
├── requirements.txt
├── Dockerfile
└── README.md

```

## Installation (Local Setup)

### 1. Clone repo
```bash
git clone https://github.com/danzinfo/streaming_voicebot.git
cd streaming_voicebot


2. Create virtual environment
python -m venv venv

Activate:

Windows:
venv\Scripts\activate


3. Install dependencies
pip install -r requirements.txt


4. Add environment variable

Create .env file or set manually:

GROQ_API_KEY=your_api_key_here


5. Run server
uvicorn app.main:app --reload

Open:

http://127.0.0.1:8000


Deployment (Render + Docker)
Docker Build:

docker build -t voicebot .
docker run -p 10000:10000 voicebot

Render Deployment
-----------------
Use:
----
Build: automatic (Docker)
Start command:
uvicorn app.main:app --host 0.0.0.0 --port 10000

Add environment variable:
-------------------------
GROQ_API_KEY

How It Works:
-------------
User speaks using microphone 
Browser converts speech → text
Text sent to FastAPI backend
Backend streams response from Groq LLM
Response is displayed in real-time chat
Browser reads response using TTS


AI Model Used:
--------------
llama-3.1-8b-instant via Groq API
Fast, low-latency inference optimized for real-time chat applications.


Future Improvements:
--------------------
WebSocket-based streaming (faster UX)
Long-term memory (Redis integration)
Wake-word activation (“Hey Jarvis”)
Mobile PWA version
Multi-user chat sessions
Conversation history UI

Limitations:
------------
Requires Chrome for voice recognition
In-memory storage resets on server restart
Groq API key required
Not yet production-scaled for heavy traffic

Author
------
Built by [Daniel]


License

MIT License
