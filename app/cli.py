import typer,uuid
from db import init_db,get_connection
from ingest import ingest_csv
from timeline import get_timeline
from llm import generate_report
from render import render_markdown
from datetime import datetime
from repo_context import build_repo_context
from cache import build_cache_key, get_cached_report, set_cached_report
app = typer.Typer()

@app.command()
def hello():
    print("Incident doc builder AI Status : OK")

@app.command()
def init():
    init_db()
    print("DB initialised")

@app.command()
def ingest(path:str):
    ingest_csv(path)
    print(f"Ingested CSV from {path}")

@app.command()
def timeline(incident_id: str):
    rows = get_timeline(incident_id)
    for r in rows:
        print(r)

@app.command()
def generate(incident_id: str):
    
    #Get timeline
    rows = get_timeline(incident_id)
    if not rows:
        print(f"No events found for incident {incident_id}")

    #Timeline to text
    lines = []
    for ts, source, author, event_type, content in rows:
        lines.append(f"{ts}[{source}]{author}{event_type}:{content}")

    timeline_text = "\n".join(lines)

    #Call LLM
    repo_context = build_repo_context(incident_id)
    full_input = f"""
    Incident Timeline:
    {timeline_text}

    {repo_context}
    """
    
    cache_key = build_cache_key(incident_id, timeline_text, repo_context)

    cached = get_cached_report(cache_key)
    if cached:
        print("Cache hit — returning cached report")
        print(cached)
        return

    report = generate_report(timeline_text)
    #Render .md
    md = render_markdown(report, incident_id)
    set_cached_report(cache_key, md)
    #Save to DuckDB
    conn = get_connection()
    conn.execute("""
        INSERT INTO reports VALUES (?,?,?,?)
""",(  str(uuid.uuid4()),
            incident_id,
            datetime.utcnow(),
            md,))
    
        #Write to .md file
    path = f"reports/{incident_id}"
    with open(path, "w", encoding="utf-8") as f:
        f.write(md)

    print(f"Report generated at {path} for incident {incident_id}")

@app.command()
def register_incident(incident_id:str, repo:str, branch:str, start:str, end:str):
    conn = get_connection()
    #REPLACE used just in case we need to re-register incidents, for production : ON CONFLICT DO NOT UPDATE
    conn.execute("""
    INSERT OR REPLACE INTO incidents VALUES(?,?,?,?,?)
""",(incident_id, repo, branch, start, end))
    conn.close()
    print("Incident registered")

@app.command()
def ingest_repo(incident_id:str):
    from repo_context import ingest_repo_context
    ingest_repo_context(incident_id)
    print("Repo context ingested Succesfully!")

if __name__ == "__main__":
    app()

