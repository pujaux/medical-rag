from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": "Say hello in one sentence"}]
)
print("✓ Groq connected:", response.choices[0].message.content)

from sentence_transformers import SentenceTransformer
embedder = SentenceTransformer("all-MiniLM-L6-v2")
test_embedding = embedder.encode("test sentence")
print("✓ Embeddings working, shape:", test_embedding.shape)

import chromadb
client2 = chromadb.Client()
collection = client2.create_collection("test")
print("✓ ChromaDB working")

print("\n✅ All systems go! Day 1 complete.")