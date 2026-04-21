# BACKEND (FastAPI + Groq + Memory + Streaming)

from fastapi import FastAPI, Header
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

import os
from collections import defaultdict
from groq import Groq

# ---------------- APP ----------------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- PATHS (Render-safe) ----------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/")
def home():
    return FileResponse(os.path.join(TEMPLATES_DIR, "index.html"))

# ---------------- GROQ ----------------
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise RuntimeError("GROQ_API_KEY missing")

client = Groq(api_key=api_key)

# ---------------- MEMORY ----------------
memory_store = defaultdict(list)
MAX_HISTORY = 10

class ChatRequest(BaseModel):
    user_input: str

# ---------------- JARVIS CORE ----------------
SYSTEM_PROMPT = """
You are JARVIS, an advanced AI voice assistant.

Rules:
- Be concise and intelligent
- Respond like a real assistant
- Keep answers short unless asked
- You assist the user like Tony Stark's JARVIS
"""

# ---------------- HEALTH CHECK ----------------
@app.get("/health")
def health():
    return {"status": "ok"}

# ---------------- CHAT STREAM ----------------
@app.post("/chat")
async def chat(
    req: ChatRequest,
    session_id: str = Header(default="default", convert_underscores=False)
):

    history = memory_store[session_id]
    history.append(f"User: {req.user_input}")

    # Limit memory
    if len(history) > MAX_HISTORY:
        history[:] = history[-MAX_HISTORY:]

    def stream():
        try:
            # Build proper message format
            messages = [{"role": "system", "content": SYSTEM_PROMPT}]

            for m in history:
                if m.startswith("User:"):
                    messages.append({
                        "role": "user",
                        "content": m.replace("User: ", "")
                    })
                else:
                    messages.append({
                        "role": "assistant",
                        "content": m.replace("JARVIS: ", "")
                    })

            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=messages,
                stream=True
            )

            full_response = ""

            for chunk in response:
                delta = getattr(chunk.choices[0], "delta", None)
                token = getattr(delta, "content", None) if delta else None

                if token:
                    full_response += token
                    yield token.encode("utf-8")

            history.append(f"JARVIS: {full_response}")

        except Exception as e:
            yield f"Error: {str(e)}".encode("utf-8")

    return StreamingResponse(
        stream(),
        media_type="text/plain",
        headers={"Cache-Control": "no-cache"}
    )
