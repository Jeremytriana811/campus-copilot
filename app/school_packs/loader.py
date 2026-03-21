import json
from dataclasses import dataclass
from pathlib import Path
from app.core.config import SCHOOL_PACKS_DIR


@dataclass
class SchoolPack:
    school_id: str
    root_dir: Path
    metadata: dict

    @property
    def docs_dir(self) -> Path:
        return self.root_dir / "docs"

    @property
    def structured_dir(self) -> Path:
        return self.root_dir / "structured"

    @property
    def sentiment_dir(self) -> Path:
        return self.root_dir / "sentiment"


def list_school_packs() -> list[str]:
    return sorted(
        [
            p.name
            for p in SCHOOL_PACKS_DIR.iterdir()
            if p.is_dir() and (p / "metadata.json").exists()
        ]
    )


def load_school_pack(school_id: str) -> SchoolPack:
    root_dir = SCHOOL_PACKS_DIR / school_id
    metadata_path = root_dir / "metadata.json"

    if not root_dir.exists():
        raise FileNotFoundError(f"School pack '{school_id}' does not exist.")

    if not metadata_path.exists():
        raise FileNotFoundError(f"metadata.json missing for '{school_id}'.")

    with open(metadata_path, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    if not (root_dir / "docs").exists():
        raise FileNotFoundError(f"docs/ missing for '{school_id}'.")

    return SchoolPack(
        school_id=school_id,
        root_dir=root_dir,
        metadata=metadata,
    )