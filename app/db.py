import duckdb

DB_PATH = "incident.db"

def get_connection():
    return duckdb.connect(DB_PATH)

def init_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS events (
                 id VARCHAR,
                 incident_id VARCHAR,
                 timestamp TIMESTAMP,
                 source VARCHAR,
                 author VARCHARm
                 event_type VARCHAR,
                 content VARCHAR
                 );    
""")
    
    conn.execute("""
    CREATE TABLE IF NOT EXISTS reports (
        id VARCHAR,
        incident_id VARCHAR,
        created_at TIMESTAMP,
        report_md VARCHAR
    );
    """)