import os
from pdf_loader import load_all_documents

def chunk_text(text, chunk_size=500, overlap=50):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap
    return chunks

def chunk_all_documents(data_folder="data"):
    documents = load_all_documents(data_folder)
    all_chunks = []
    for doc in documents:
        chunks = chunk_text(doc["text"])
        for i, chunk in enumerate(chunks):
            all_chunks.append({
                "text": chunk,
                "source": doc["source"],
                "category": doc["category"],
                "chunk_index": i
            })
    return all_chunks

if __name__ == "__main__":
    chunks = chunk_all_documents()
    print(f"✅ Total chunks created: {len(chunks)}")
    print(f"\nSample chunk:")
    print(f"Source: {chunks[0]['source']}")
    print(f"Category: {chunks[0]['category']}")
    print(f"Chunk index: {chunks[0]['chunk_index']}")
    print(f"Text preview: {chunks[0]['text'][:150]}")
    
    import json
    with open("chunks.json", "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2)
    print(f"✅ Chunks saved to chunks.json")