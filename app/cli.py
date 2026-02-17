import typer 

app = typer.Typer()

@app.command()
def hello():
    print("Incident doc builder AI Status : OK")

if __name__ == "__main__":
    app()
    