import pandas as pd
import uuid
from db import get_connection

def ingest_csv(path : str):
    df = pd.read_csv(path)
    conn = get_connection()

    for _, row in df.iterrows():
        conn.execute("""
    INSERT INTO events VALUES (? , ? , ? , ? , ? , ? , ? )
""",(
        str(uuid.uuid4(),
        row["incident_id"]),
        row["timestamp"],
        row["source"],
        row["author"],
        row["event_type"],
        row["content"],
         ))
    conn. close()