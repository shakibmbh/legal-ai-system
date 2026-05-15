
import chromadb

DB_PATH = "/content/chroma_db"

client = chromadb.PersistentClient(
    path=DB_PATH
)

collection_name = "legal_documents"

try:

    collection = client.get_collection(
        name=collection_name
    )

except:

    collection = client.create_collection(
        name=collection_name
    )

def add_chunk(
    chunk_id,
    text,
    embedding,
    metadata
):

    existing = collection.get(
        ids=[chunk_id]
    )

    if existing["ids"]:
        return

    collection.add(
        ids=[chunk_id],
        documents=[text],
        embeddings=[embedding],
        metadatas=[metadata]
    )

def search_chunks(
    query_embedding,
    top_k=5
):

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results
