import json
import numpy as np
import faiss
import pickle
import os
from sentence_transformers import SentenceTransformer
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Load everything once
embedder = SentenceTransformer("all-MiniLM-L6-v2")
index = faiss.read_index("faiss_index.bin")
with open("chunks_metadata.pkl", "rb") as f:
    chunks = pickle.load(f)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are a helpful medical information assistant. 
Your job is to explain medical test results in simple, easy-to-understand language.

STRICT RULES:
1. Only answer based on the provided context
2. Never diagnose any condition
3. Never recommend any medication or treatment
4. Always end with: "Please consult your doctor for personal medical advice."
5. If context doesn't contain the answer, say "I don't have enough information on this topic."
"""

def retrieve_chunks(query, top_k=3):
    query_embedding = embedder.encode([query]).astype("float32")
    distances, indices = index.search(query_embedding, k=top_k)
    retrieved = []
    for i, idx in enumerate(indices[0]):
        retrieved.append({
            "text": chunks[idx]["text"],
            "source": chunks[idx]["source"],
            "category": chunks[idx]["category"],
            "distance": float(distances[0][i])
        })
    return retrieved

def generate_answer(query, retrieved_chunks):
    context = "\n\n".join([
        f"Source: {c['source']}\n{c['text']}"
        for c in retrieved_chunks
    ])
    
    prompt = f"""Context from medical reference documents:
{context}

User Question: {query}

Please answer the question based only on the context above."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

def ask(query):
    from safety_layer import check_query
    is_safe, message = check_query(query)
    if not is_safe:
        print(f"\n🚫 Query blocked: {message}")
        return message
    
    print(f"\n{'='*50}")
    print(f"Question: {query}")
    print(f"{'='*50}")
    
    retrieved = retrieve_chunks(query)
    print(f"\n📚 Retrieved {len(retrieved)} chunks:")
    for i, c in enumerate(retrieved):
        print(f"  {i+1}. {c['source']} (distance: {c['distance']:.3f})")
    
    answer = generate_answer(query, retrieved)
    print(f"\n🤖 Answer:\n{answer}")
    return answer

if __name__ == "__main__":
    ask("What is normal hemoglobin level?")
    ask("What does high blood glucose mean?")
    ask("What is TSH and what does abnormal TSH mean?")