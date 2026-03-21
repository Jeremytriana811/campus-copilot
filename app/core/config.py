from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT_DIR / "data"
CHROMA_DIR = ROOT_DIR / ".chroma"
SCHOOL_PACKS_DIR = ROOT_DIR / "school_packs"
DB_PATH = DATA_DIR / "app.db"

DATA_DIR.mkdir(exist_ok=True)
CHROMA_DIR.mkdir(exist_ok=True)
SCHOOL_PACKS_DIR.mkdir(exist_ok=True)