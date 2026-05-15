
from app.retrieval.embedder import get_embedding
from app.retrieval.vectordb import search_chunks

def retrieve(query):

    query_embedding = get_embedding(query)

    results = search_chunks(
        query_embedding=query_embedding,
        top_k=5
    )

    return results
