from app.school_packs.loader import load_school_pack
from app.rag.ingest import ingest_school_pack


def get_pack_summary(school_id: str) -> dict:
    pack = load_school_pack(school_id)

    curated_dir = pack.docs_dir / "curated"
    raw_dir = pack.docs_dir / "raw"

    curated_files = list(curated_dir.glob("*.pdf")) if curated_dir.exists() else []
    raw_files = list(raw_dir.glob("*.pdf")) if raw_dir.exists() else []

    return {
        "school_id": school_id,
        "school_name": pack.metadata.get("school_name"),
        "catalog_year": pack.metadata.get("catalog_year"),
        "curated_pdf_count": len(curated_files),
        "raw_pdf_count": len(raw_files),
        "curated_pdf_names": [p.name for p in curated_files],
        "raw_pdf_names": [p.name for p in raw_files],
    }


def run_ingestion(school_id: str) -> int:
    return ingest_school_pack(school_id)