
---

## Setup

### 1. Clone repository
git clone <repo-url>
cd incident-narrative-ai


---

### 2. Create virtual environment
python -m venv .venv
Windows:
.\venv\Scripts\activate
Mac/Linux:
source .venv/bin/activate


---

### 3. Install dependencies
pip install duckdb typer pydantic pandas requests redis


---

## Install Ollama (Local LLM)

Install from:

https://ollama.com

Start the server:
ollama serve

Install LLM:
ollama pull qwen2.5-coder:3b


---

## Install Redis (for caching)

Using Docker:
docker run -d -p 6379:6379 redis


---

## Usage

### Initialize database
python app\cli.py init


---

### Register an incident with repository context
python app/cli.py register-incident INC-1 ../auth-service main "2026-02-01 14:00:00" "2026-02-01 15:00:00"


This associates the incident with:

- repository path
- branch
- investigation time window

---

### Ingest repository changes
python app/cli.py ingest-repo INC-1


This extracts:

- commits within the incident window
- files changed in each commit

and stores them in DuckDB.

---

### View timeline
python app\cli.py timeline INC-1


---

### Generate postmortem report
python app\cli.py generate INC-1

Report Generated at reports\INC-1