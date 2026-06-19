import os
import re
from pdf_loader import load_all_documents


def chunk_text(text, chunk_size=800, overlap=100):
    """
    Smart chunking that respects paragraph/section boundaries.
    Falls back to character-based splitting only for oversized paragraphs.
    """
    # Split on blank lines first (paragraphs / sections)
    paragraphs = re.split(r'\n\s*\n', text)
    paragraphs = [p.strip() for p in paragraphs if p.strip()]

    chunks = []
    current_chunk = ""

    for para in paragraphs:
        # If a single paragraph is bigger than chunk_size, split it on sentences
        if len(para) > chunk_size:
            sentences = re.split(r'(?<=[.!?])\s+', para)
            for sentence in sentences:
                if len(current_chunk) + len(sentence) + 1 <= chunk_size:
                    current_chunk += (" " if current_chunk else "") + sentence
                else:
                    if current_chunk:
                        chunks.append(current_chunk.strip())
                    current_chunk = sentence
            continue

        # Normal case: try to add the whole paragraph to current chunk
        if len(current_chunk) + len(para) + 2 <= chunk_size:
            current_chunk += ("\n\n" if current_chunk else "") + para
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = para

    if current_chunk:
        chunks.append(current_chunk.strip())

    # Add small overlap between chunks so context isn't lost at boundaries
    overlapped_chunks = []
    for i, chunk in enumerate(chunks):
        if i > 0 and overlap > 0:
            prev_tail = chunks[i - 1][-overlap:]
            chunk = prev_tail + "\n...\n" + chunk
        overlapped_chunks.append(chunk)

    return overlapped_chunks


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