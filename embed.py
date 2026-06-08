import chromadb
from sentence_transformers import SentenceTransformer
from ingest import load_documents, chunk_documents

COLLECTION_NAME = "utd_cs_reviews"

# Load embedding model (runs locally, no API key)
model = SentenceTransformer("all-MiniLM-L6-v2")

# Set up ChromaDB (persists to disk so you don't re-embed every run)
client = chromadb.PersistentClient(path="./chroma_db")


def embed_and_store(chunks):
    # Delete collection if it already exists (clean rebuild)
    existing = [c.name for c in client.list_collections()]
    if COLLECTION_NAME in existing:
        client.delete_collection(COLLECTION_NAME)

    collection = client.create_collection(COLLECTION_NAME)

    texts = [c["text"] for c in chunks]
    sources = [c["source"] for c in chunks]
    ids = [f"chunk_{i}" for i in range(len(chunks))]

    print(f"Embedding {len(texts)} chunks...")
    embeddings = model.encode(texts, show_progress_bar=True).tolist()

    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=texts,
        metadatas=[{"source": s} for s in sources]
    )
    print(f"Stored {len(texts)} chunks in ChromaDB.")
    return collection


def get_collection():
    return client.get_collection(COLLECTION_NAME)


def retrieve(query, k=5):
    collection = get_collection()
    query_embedding = model.encode([query]).tolist()
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=k,
        include=["documents", "metadatas", "distances"]
    )
    chunks = []
    for i in range(len(results["documents"][0])):
        chunks.append({
            "text": results["documents"][0][i],
            "source": results["metadatas"][0][i]["source"],
            "distance": results["distances"][0][i]
        })
    return chunks


if __name__ == "__main__":
    docs = load_documents("docs")
    chunks = chunk_documents(docs)
    embed_and_store(chunks)

    # Test retrieval with 3 sample queries
    test_queries = [
        "What do students say about exam difficulty?",
        "Which professor curves grades?",
        "Is CS 2336 hard?"
    ]
    for q in test_queries:
        print(f"\nQuery: {q}")
        results = retrieve(q)
        for r in results:
            print(f"  [{r['distance']:.3f}] ({r['source']}) {r['text'][:120]}")