from app.planner.generator import generate_better_plan


def test_planner_respects_max_courses():
    result = generate_better_plan("ucf_cs", [], max_courses_per_term=2)
    for term in result["terms"]:
        assert len(term) <= 2


def test_planner_places_prereq_before_dependent():
    result = generate_better_plan("ucf_cs", [], max_courses_per_term=3)

    flat = []
    for i, term in enumerate(result["terms"]):
        for course in term:
            flat.append((course, i))

    term_lookup = {course: term_index for course, term_index in flat}

    if "COP3503C" in term_lookup and "COP4331C" in term_lookup:
        assert term_lookup["COP3503C"] < term_lookup["COP4331C"]


def test_planner_handles_some_completed():
    result = generate_better_plan(
        "ucf_cs",
        ["COP3502C", "COT3100C", "CAP4630"],
        max_courses_per_term=3
    )

    all_planned = [course for term in result["terms"] for course in term]

    assert "COP3502C" not in all_planned
    assert "COT3100C" not in all_planned