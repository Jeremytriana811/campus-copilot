def build_context(hits: list[dict]) -> str:
    parts = []
    for i, hit in enumerate(hits, start=1):
        meta = hit["metadata"]
        parts.append(
            f"[Source {i}] Document: {meta.get('document_name')} | Page: {meta.get('page')}\n"
            f"{hit['text']}\n"
        )
    return "\n".join(parts)


def question_should_refuse_by_pattern(question: str) -> bool:
    q = question.lower()

    unsupported_patterns = [
        "which professor",
        "best professor",
        "easiest professor",
        "hardest professor",
        "best teacher",
        "rate my professor",
        "which dorm",
        "best dorm",
        "easiest class",
        "hardest class",
    ]

    return any(pattern in q for pattern in unsupported_patterns)


def should_refuse(hits: list[dict], question: str, distance_threshold: float = 0.55) -> bool:
    if question_should_refuse_by_pattern(question):
        return True

    if not hits:
        return True

    best_distance = hits[0].get("distance")
    if best_distance is None:
        return False

    return best_distance > distance_threshold


def generate_grounded_response(question: str, hits: list[dict]) -> dict:
    if should_refuse(hits, question):
        return {
            "status": "refused",
            "answer": "I could not verify this from the provided school documents.",
            "citations": []
        }

    best_hit = hits[0]
    meta = best_hit["metadata"]

    answer = (
        f"Based on the retrieved school documents, the most relevant evidence comes from "
        f"{meta.get('document_name')} page {meta.get('page')}."
    )

    citations = [
        {
            "document_name": meta.get("document_name"),
            "page": meta.get("page"),
            "snippet": best_hit["text"][:400]
        }
    ]

    return {
        "status": "grounded",
        "answer": answer,
        "citations": citations
    }