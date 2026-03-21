from app.rag.ingest import ingest_school_pack
from app.school_packs.loader import load_school_pack


def test_curated_pdf_folder_exists():
    pack = load_school_pack("ucf_cs")
    curated_dir = pack.docs_dir / "curated"
    assert curated_dir.exists()


def test_ingest_school_pack_runs():
    result = ingest_school_pack("ucf_cs")
    assert result >= 1