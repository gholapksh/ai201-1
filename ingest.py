import os
import re

DOCS_FOLDER = "docs"
CHUNK_SIZE = 300
CHUNK_OVERLAP = 50


def load_documents(folder_path):
    documents = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            filepath = os.path.join(folder_path, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                raw_text = f.read()
            cleaned = clean_text(raw_text)
            documents.append({"text": cleaned, "source": filename})
    return documents


def clean_text(text):
    # Remove HTML tags
    text = re.sub(r"<[^>]+>", "", text)
    # Decode common HTML entities
    text = text.replace("&amp;", "&").replace("&nbsp;", " ").replace("&#39;", "'")
    # Collapse whitespace
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def chunk_text(text, source, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()
        if len(chunk) > 0:
            chunks.append({"text": chunk, "source": source})
        start += chunk_size - overlap
    return chunks


def chunk_documents(documents):
    all_chunks = []
    for doc in documents:
        chunks = chunk_text(doc["text"], doc["source"])
        all_chunks.extend(chunks)
    return all_chunks


if __name__ == "__main__":
    docs = load_documents(DOCS_FOLDER)
    print(f"Loaded {len(docs)} documents")

    chunks = chunk_documents(docs)
    print(f"Produced {len(chunks)} chunks")

    # Inspect 5 random chunks
    import random
    samples = random.sample(chunks, min(5, len(chunks)))
    for i, chunk in enumerate(samples):
        print(f"\n--- Chunk {i+1} (source: {chunk['source']}) ---")
        print(chunk["text"])