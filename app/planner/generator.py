from app.planner.checker import load_requirements, check_degree_progress


PLANNER_PREREQS = {
    "COP3503C": ["COP3502C"],
    "CDA3103C": ["COP3502C"],
    "COP3402": ["COP3502C", "CDA3103C"],
    "COT4210": ["COT3100C"],
    "COT3960": ["COP3502C"],
    "COP4331C": ["COP3503C", "COT3960"],
    "COP4934": ["COP4331C"],
    "COP4935": ["COP4934"]
}


def choose_group_courses(reqs: dict, completed_set: set[str]) -> list[str]:
    chosen_courses = []

    for group in reqs.get("choice_groups", []):
        options = [c.upper() for c in group.get("courses", [])]
        choose_count = group.get("choose", 0)

        already_done = [c for c in options if c in completed_set]
        still_needed = max(0, choose_count - len(already_done))

        if still_needed == 0:
            continue

        remaining_options = [c for c in options if c not in completed_set]

        chosen_courses.extend(remaining_options[:still_needed])

    return chosen_courses


def prerequisites_satisfied(course: str, completed_set: set[str]) -> bool:
    prereqs = PLANNER_PREREQS.get(course.upper(), [])
    return all(pr.upper() in completed_set for pr in prereqs)


def generate_better_plan(
    school_id: str,
    completed_courses: list[str],
    max_courses_per_term: int = 3
) -> dict:
    reqs = load_requirements(school_id)
    progress = check_degree_progress(school_id, completed_courses)

    completed_set = set(c.upper() for c in completed_courses)

    remaining_courses = []
    remaining_courses.extend(progress["missing_core_courses"])
    remaining_courses.extend(progress["missing_additional_required_courses"])
    remaining_courses.extend(progress["missing_milestones"])

    chosen_group_courses = choose_group_courses(reqs, completed_set)
    remaining_courses.extend(chosen_group_courses)

    seen = set()
    deduped_remaining = []
    for course in remaining_courses:
        course_upper = course.upper()
        if course_upper not in completed_set and course_upper not in seen:
            deduped_remaining.append(course_upper)
            seen.add(course_upper)

    terms = []
    unresolved_courses = deduped_remaining[:]

    while unresolved_courses:
        available = [
            course for course in unresolved_courses
            if prerequisites_satisfied(course, completed_set)
        ]

        if not available:
            break

        term_courses = available[:max_courses_per_term]
        terms.append(term_courses)

        for course in term_courses:
            completed_set.add(course)

        unresolved_courses = [
            course for course in unresolved_courses
            if course not in term_courses
        ]

    return {
        "terms": terms,
        "unresolved_courses": unresolved_courses,
        "chosen_group_courses": chosen_group_courses
    }