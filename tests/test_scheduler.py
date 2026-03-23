from app.scheduler.solver import time_conflict, generate_conflict_free_schedule


def test_time_conflict_same_day_overlap():
    a = {"course_code": "COP3503C", "day": "MW", "start": 900, "end": 1015}
    b = {"course_code": "CDA3103C", "day": "MW", "start": 1000, "end": 1115}
    assert time_conflict(a, b) is True


def test_time_conflict_different_day():
    a = {"course_code": "COP3503C", "day": "MW", "start": 900, "end": 1015}
    b = {"course_code": "CDA3103C", "day": "TR", "start": 900, "end": 1015}
    assert time_conflict(a, b) is False


def test_generate_conflict_free_schedule_success():
    sections = [
        {"course_code": "COP3503C", "day": "MW", "start": 900, "end": 1015},
        {"course_code": "CDA3103C", "day": "TR", "start": 900, "end": 1015},
        {"course_code": "COT4210", "day": "MW", "start": 1100, "end": 1215},
    ]
    result = generate_conflict_free_schedule(sections)
    assert result["status"] == "success"


def test_generate_conflict_free_schedule_failure():
    sections = [
        {"course_code": "COP3503C", "day": "MW", "start": 900, "end": 1015},
        {"course_code": "CDA3103C", "day": "MW", "start": 1000, "end": 1115},
    ]
    result = generate_conflict_free_schedule(sections)
    assert result["status"] == "failed"
    assert ("COP3503C", "CDA3103C") in result["conflicts"]