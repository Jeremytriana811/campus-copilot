from app.storage.db import get_connection


def get_latest_ingestion_runs(limit: int = 10) -> list[dict]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT id, school_id, document_count, chunk_count, status, created_at
        FROM ingestion_runs
        ORDER BY id DESC
        LIMIT ?
        """,
        (limit,),
    )
    rows = cur.fetchall()
    conn.close()
    return [dict(row) for row in rows]