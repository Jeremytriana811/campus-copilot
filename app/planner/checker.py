import json
from app.core.config import SCHOOL_PACKS_DIR


def load_requirements(school_id: str) -> dict:
    path = SCHOOL_PACKS_DIR / school_id / "structured" / "requirements.json"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def check_degree_progress(school_id: str, completed_courses: list[str]) -> dict:
    reqs = load_requirements(school_id)

    completed_set = set(c.upper() for c in completed_courses)

    required_core = reqs.get("required_core_courses", [])
    missing_core = [
        course for course in required_core
        if course.upper() not in completed_set
    ]

    choice_groups = reqs.get("choice_groups", [])
    choice_group_results = []

    for group in choice_groups:
        options = [c.upper() for c in group.get("courses", [])]
        completed_in_group = [c for c in options if c in completed_set]
        needed = group.get("choose", 0) - len(completed_in_group)

        choice_group_results.append({
            "name": group.get("name"),
            "completed_options": completed_in_group,
            "remaining_to_choose": max(0, needed),
            "options": options
        })

    additional_required = reqs.get("additional_required_courses", [])
    missing_additional = [
        course for course in additional_required
        if course.upper() not in completed_set
    ]

    milestones = reqs.get("required_exam_or_milestone", [])
    missing_milestones = [
        item["code"] for item in milestones
        if item["code"].upper() not in completed_set
    ]

    return {
        "missing_core_courses": missing_core,
        "choice_group_results": choice_group_results,
        "missing_additional_required_courses": missing_additional,
        "missing_milestones": missing_milestones,
        "completed_count": len(completed_set)
    }