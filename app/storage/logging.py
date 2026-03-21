import json
from app.storage.db import get_connection


def log_event(event_type: str, school_id: str | None, payload: dict) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO app_logs (event_type, school_id, payload)
        VALUES (?, ?, ?)
        """,
        (event_type, school_id, json.dumps(payload)),
    )
    conn.commit()
    conn.close()


def get_recent_logs(limit: int = 20) -> list[dict]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT id, event_type, school_id, payload, created_at
        FROM app_logs
        ORDER BY id DESC
        LIMIT ?
        """,
        (limit,),
    )
    rows = cur.fetchall()
    conn.close()
    return [dict(row) for row in rows]