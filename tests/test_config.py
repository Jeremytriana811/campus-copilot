from app.core.config import DATA_DIR, CHROMA_DIR, SCHOOL_PACKS_DIR


def test_config_directories_exist():
    assert DATA_DIR.exists()
    assert CHROMA_DIR.exists()
    assert SCHOOL_PACKS_DIR.exists()