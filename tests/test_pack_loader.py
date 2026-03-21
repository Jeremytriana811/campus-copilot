from app.school_packs.loader import list_school_packs, load_school_pack


def test_list_school_packs_contains_ucf():
    packs = list_school_packs()
    assert "ucf_cs" in packs


def test_load_school_pack_ucf():
    pack = load_school_pack("ucf_cs")

    assert pack.school_id == "ucf_cs"
    assert pack.metadata["school_name"] == "University of Central Florida"
    assert pack.docs_dir.exists()
    assert pack.structured_dir.exists()
    assert pack.sentiment_dir.exists()