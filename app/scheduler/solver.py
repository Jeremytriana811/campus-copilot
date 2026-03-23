from itertools import combinations


def time_conflict(section_a: dict, section_b: dict) -> bool:
    if section_a["day"] != section_b["day"]:
        return False

    return not (
        section_a["end"] <= section_b["start"] or
        section_b["end"] <= section_a["start"]
    )


def generate_conflict_free_schedule(sections: list[dict]) -> dict:
    conflicts = []

    for a, b in combinations(sections, 2):
        if time_conflict(a, b):
            conflicts.append((a["course_code"], b["course_code"]))

    if conflicts:
        return {
            "status": "failed",
            "conflicts": conflicts
        }

    return {
        "status": "success",
        "sections": sections
    }