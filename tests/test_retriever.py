from app.rag.retriever import retrieve_chunks


def test_retrieve_chunks_returns_results():
    hits = retrieve_chunks("ucf_cs", "What is the first programming course?", 5)

    assert isinstance(hits, list)
    assert len(hits) >= 1
    assert "text" in hits[0]
    assert "metadata" in hits[0]
    assert "distance" in hits[0]