from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pickle
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

print("Loading...", flush=True)
with open("chunks_metadata.pkl", "rb") as f:
    chunks = pickle.load(f)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
print("Ready!", flush=True)

app = FastAPI(title="Medical RAG API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BLOCKED_KEYWORDS = [
    "what medicine", "which medicine", "prescribe",
    "dosage", "dose", "treat my", "diagnose", "do i have",
    "should i take", "can i take",
]

SYSTEM_PROMPT = """You are a helpful medical information assistant.
Explain medical test results in simple language.
Never diagnose or recommend medication.
Always end with: "Please consult your doctor for personal medical advice."
"""

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str
    sources: list
    is_blocked: bool
    message: str = ""

def is_safe(query):
    query_lower = query.lower()
    for keyword in BLOCKED_KEYWORDS:
        if keyword in query_lower:
            return False
    return True

def simple_retrieve(query, top_k=3):
    query_lower = query.lower()
    scored = []
    for chunk in chunks:
        score = sum(1 for word in query_lower.split() 
                   if word in chunk["text"].lower())
        scored.append((score, chunk))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [c for _, c in scored[:top_k]]

@app.get("/")
def root():
    return {"message": "Medical RAG API is running!"}

@app.get("/health")
def health():
    return {"status": "healthy", "chunks": len(chunks)}

@app.post("/ask", response_model=QueryResponse)
def ask(request: QueryRequest):
    if not is_safe(request.question):
        return QueryResponse(
            answer="",
            sources=[],
            is_blocked=True,
            message="For treatment or diagnosis questions, please consult your doctor."
        )

    retrieved = simple_retrieve(request.question)
    context = "\n\n".join([f"Source: {c['source']}\n{c['text']}" 
                           for c in retrieved])
    prompt = f"Context:\n{context}\n\nQuestion: {request.question}"

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ]
    )

    return QueryResponse(
        answer=response.choices[0].message.content,
        sources=[{"source": c["source"], "category": c["category"], "content": c["text"][:200]} 
        for c in retrieved],
        is_blocked=False
    )