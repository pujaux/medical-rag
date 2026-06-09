import json
import numpy as np
import faiss
import pickle
from sentence_transformers import SentenceTransformer

def create_vector_store(chunks_file="chunks.json"):
    with open(chunks_file, "r", encoding="utf-8") as f:
        chunks = json.load(f)
    print(f"✓ Loaded {len(chunks)} chunks")

    print("✓ Loading embedding model...")
    embedder = SentenceTransformer("all-MiniLM-L6-v2")

    texts = [chunk["text"] for chunk in chunks]
    print("✓ Embedding chunks...")
    embeddings = embedder.encode(texts, show_progress_bar=True)
    embeddings = np.array(embeddings).astype("float32")

    # Create FAISS index
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    print(f"✓ FAISS index created with {index.ntotal} vectors")

    # Save index and chunks
    faiss.write_index(index, "faiss_index.bin")
    with open("chunks_metadata.pkl", "wb") as f:
        pickle.dump(chunks, f)
    print("✅ Vector store saved!")
    return index, chunks

def test_retrieval(query="What is normal hemoglobin level?"):
    embedder = SentenceTransformer("all-MiniLM-L6-v2")
    index = faiss.read_index("faiss_index.bin")
    with open("chunks_metadata.pkl", "rb") as f:
        chunks = pickle.load(f)

    query_embedding = embedder.encode([query]).astype("float32")
    distances, indices = index.search(query_embedding, k=3)

    print(f"\n🔍 Query: {query}")
    for i, idx in enumerate(indices[0]):
        print(f"\n--- Result {i+1} ---")
        print(f"Source: {chunks[idx]['source']} | Category: {chunks[idx]['category']}")
        print(f"Text: {chunks[idx]['text'][:200]}")

if __name__ == "__main__":
    create_vector_store()
    test_retrieval("What is normal hemoglobin level?")
    test_retrieval("What does high glucose mean?")