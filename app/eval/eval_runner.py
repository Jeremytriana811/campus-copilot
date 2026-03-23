import json
from pathlib import Path

from app.rag.retriever import retrieve_chunks
from app.rag.answering import generate_grounded_response
from app.storage.db import get_connection


def load_eval_questions() -> list[dict]:
    path = Path(__file__).resolve().parent / "eval_questions.json"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def run_eval(school_id: str) -> dict:
    questions = load_eval_questions()

    total = len(questions)
    passed = 0
    grounded_answers = 0
    correct_refusals = 0
    details = []

    for item in questions:
        question = item["question"]
        should_refuse = item["should_refuse"]
        expected_doc = item["expected_doc"]

        hits = retrieve_chunks(school_id, question, k=5)
        result = generate_grounded_response(question, hits)

        top_doc = hits[0]["metadata"].get("document_name") if hits else None
        got_refusal = result["status"] == "refused"

        pass_flag = False

        if should_refuse and got_refusal:
            correct_refusals += 1
            pass_flag = True
        elif not should_refuse and not got_refusal and top_doc == expected_doc:
            grounded_answers += 1
            pass_flag = True

        if pass_flag:
            passed += 1

        details.append({
            "id": item["id"],
            "question": question,
            "expected_doc": expected_doc,
            "top_doc": top_doc,
            "status": result["status"],
            "passed": pass_flag,
        })

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO eval_runs (
            school_id, total_questions, passed_questions, grounded_answers, correct_refusals
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (school_id, total, passed, grounded_answers, correct_refusals),
    )
    conn.commit()
    conn.close()

    return {
        "total_questions": total,
        "passed_questions": passed,
        "grounded_answers": grounded_answers,
        "correct_refusals": correct_refusals,
        "details": details
    }