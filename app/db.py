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
                 author VARCHAR,
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

    conn.execute("""
    CREATE TABLE IF NOT EXISTS incidents (
        incident_id VARCHAR PRIMARY KEY,
        repo_path VARCHAR,
        branch VARCHAR,
        start_time TIMESTAMP,
        end_time TIMESTAMP
    );
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS commits (
        hash VARCHAR,
        incident_id VARCHAR,
        author VARCHAR,
        timestamp TIMESTAMP,
        message VARCHAR
    );
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS commit_files (
        commit_hash VARCHAR,
        file_path VARCHAR
    );
    """)

    conn.close()