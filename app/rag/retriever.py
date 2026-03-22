from app.rag.ingest import get_collection
from app.storage.logging import log_event


def retrieve_chunks(school_id: str, question: str, k: int = 5) -> list[dict]:
    collection = get_collection(school_id)
    results = collection.query(query_texts=[question], n_results=k)

    docs = results.get("documents", [[]])[0]
    metas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    hits = []
    for doc, meta, distance in zip(docs, metas, distances):
        hits.append({
            "text": doc,
            "metadata": meta,
            "distance": distance
        })

    log_event(
        event_type="retrieval_query",
        school_id=school_id,
        payload={
            "question": question,
            "k": k,
            "hit_count": len(hits)
        },
    )

    return hits