import os

def load_all_documents(data_folder="data"):
    documents = []
    for category in os.listdir(data_folder):
        category_path = os.path.join(data_folder, category)
        if os.path.isdir(category_path):
            for filename in os.listdir(category_path):
                if filename.endswith(".txt"):
                    filepath = os.path.join(category_path, filename)
                    with open(filepath, "r", encoding="utf-8") as f:
                        text = f.read().strip()
                    if text:
                        documents.append({
                            "text": text,
                            "source": filename,
                            "category": category
                        })
                        print(f"✓ Loaded: {filename} ({category}) - {len(text)} chars")
    return documents

if __name__ == "__main__":
    docs = load_all_documents()
    print(f"\n✅ Total documents loaded: {len(docs)}")
    print("\nSample from first document:")
    print(docs[0]["text"][:200])