"""
Rebuild chunks_metadata.pkl using the improved chunker,
WITHOUT requiring sentence-transformers/FAISS.
This keeps the old keyword-search api.py working with better chunks.
"""
import pickle
from chunker import chunk_all_documents

chunks = chunk_all_documents("../data")

with open("chunks_metadata.pkl", "wb") as f:
    pickle.dump(chunks, f)

print(f"Rebuilt chunks_metadata.pkl with {len(chunks)} chunks")