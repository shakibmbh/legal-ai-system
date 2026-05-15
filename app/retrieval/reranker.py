
from sentence_transformers import CrossEncoder

reranker = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)

def rerank_results(query, results):

    documents = results["documents"][0]
    ids = results["ids"][0]
    metadatas = results["metadatas"][0]

    pairs = []

    for doc in documents:
        pairs.append([query, doc])

    scores = reranker.predict(pairs)

    combined = list(zip(
        documents,
        ids,
        metadatas,
        scores
    ))

    combined.sort(
        key=lambda x: x[3],
        reverse=True
    )

    reranked = {
        "documents": [[x[0] for x in combined]],
        "ids": [[x[1] for x in combined]],
        "metadatas": [[x[2] for x in combined]],
        "scores": [[float(x[3]) for x in combined]]
    }

    return reranked
