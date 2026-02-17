import typer 
from db import init_db

app = typer.Typer()

@app.command()
def hello():
    print("Incident doc builder AI Status : OK")

@app.command()
def init():
    init_db()
    print("DB initialised")

if __name__ == "__main__":
    app()
