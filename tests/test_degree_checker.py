from app.planner.checker import check_degree_progress


def test_degree_progress_some_completed():
    result = check_degree_progress("ucf_cs", ["cop3502c", "COT3100C"])
    assert "COP3503C" in result["missing_core_courses"]
    assert "CDA3103C" in result["missing_core_courses"]
    assert result["completed_count"] == 2


def test_degree_progress_choice_group():
    result = check_degree_progress("ucf_cs", ["CAP4630"])
    groups = result["choice_group_results"]

    ai_ml_group = None
    for group in groups:
        if group["name"] == "advanced_core_ai_ml_choice":
            ai_ml_group = group
            break

    assert ai_ml_group is not None
    assert ai_ml_group["remaining_to_choose"] == 0


def test_degree_progress_milestone():
    result = check_degree_progress("ucf_cs", [])
    assert "COT3960" in result["missing_milestones"]
    