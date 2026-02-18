from db import get_connection

def get_timeline(incident_id: str):
    conn = get_connection()
    rows = conn.execute(
        """
        SELECT timestamp, source, author, event_type, content
        FROM events
        WHERE incident_id = ?
        ORDER BY timestamp ASC
        """,
        (incident_id,),
    ).fetchall()
    conn.close()
    return rows
