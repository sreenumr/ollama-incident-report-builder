import typer 
from db import init_db
from ingest import ingest_csv
from timeline import get_timeline

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
if __name__ == "__main__":
    app()
