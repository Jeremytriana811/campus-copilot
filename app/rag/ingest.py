from pathlib import Path
from typing import List, Dict
from pypdf import PdfReader
import chromadb
from chromadb.utils import embedding_functions

from app.core.config import CHROMA_DIR
from app.school_packs.loader import load_school_pack
from app.storage.db import get_connection
from app.storage.logging import log_event


def split_text(text: str, chunk_size: int = 1200, overlap: int = 150) -> List[str]:
    text = " ".join(text.split())
    if not text:
        return []

    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks


def get_collection(school_id: str):
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )
    return client.get_or_create_collection(
        name=school_id,
        embedding_function=embedding_fn,
    )


def extract_pdf_chunks(pdf_path: Path, school_id: str) -> List[Dict]:
    reader = PdfReader(str(pdf_path))
    all_chunks = []

    for page_num, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        chunks = split_text(text)

        for chunk_idx, chunk in enumerate(chunks):
            all_chunks.append(
                {
                    "id": f"{pdf_path.stem}-p{page_num}-c{chunk_idx}",
                    "text": chunk,
                    "metadata": {
                        "school_id": school_id,
                        "document_name": pdf_path.name,
                        "page": page_num,
                    },
                }
            )

    return all_chunks


def ingest_school_pack(school_id: str) -> int:
    pack = load_school_pack(school_id)
    collection = get_collection(school_id)

    ids = []
    docs = []
    metas = []
    doc_count = 0

    curated_dir = pack.docs_dir / "curated"

    if not curated_dir.exists():
        raise FileNotFoundError(f"Curated docs folder missing for '{school_id}'.")

    for pdf_path in curated_dir.glob("*.pdf"):
        doc_count += 1
        chunks = extract_pdf_chunks(pdf_path, school_id)

        for item in chunks:
            ids.append(item["id"])
            docs.append(item["text"])
            metas.append(item["metadata"])

    if ids:
        collection.upsert(ids=ids, documents=docs, metadatas=metas)

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO ingestion_runs (school_id, document_count, chunk_count, status)
        VALUES (?, ?, ?, ?)
        """,
        (school_id, doc_count, len(ids), "success"),
    )
    conn.commit()
    conn.close()

    log_event(
        event_type="ingestion_run",
        school_id=school_id,
        payload={
            "document_count": doc_count,
            "chunk_count": len(ids),
            "status": "success",
        },
    )

    return len(ids)