from app.storage.db import init_db, get_connection


def test_db_initializes():
    init_db()
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    table_names = {row[0] for row in cur.fetchall()}
    conn.close()

    assert "app_logs" in table_names
    assert "saved_plans" in table_names
    assert "ingestion_runs" in table_names
    assert "eval_runs" in table_names