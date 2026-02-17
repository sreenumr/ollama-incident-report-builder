import typer 
from db import init_db
from ingest import ingest_csv

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
    print(f"Ingest CSV from {path}")

if __name__ == "__main__":
    app()
