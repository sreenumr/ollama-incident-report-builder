import subprocess
from db import get_connection

def ingest_repo_context(incident_id:str):
    conn = get_connection()

    incident = conn.execute("""
"SELECT repo_path, branch, start_time, end_time FROM incidents WHERE incident_id = ?",
""",(incident_id)
    ).fetchone()

    if not incident:
        raise ValueError(f"Incident {incident_id} Not Registered")
    
    repo_path,branch,start_time,end_time = incident

    #cmd to get commits
    cmd =[
        "git",
        "-C",
        repo_path,
        "log",
        f"--since={start_time}",
        f"--until={end_time}",
        "--pretty=format:%H|%an|%ad|%s",
        "--date=iso",
        branch
    ]

    result = subprocess.run(cmd,capture_output=True, text=True)
    lines = result.stdout.splitlines()

    for line in lines:
        parts = line.split("|", 3)
        if len(parts) !=4:
            continue

        commit_hash,author,timestamp,message = parts
        conn.execute("INSERT INTO commits VALUES (?,?,?,?,?)",(commit_hash,incident_id,author,timestamp,message))

        #Changed files for this incident
        files_cmd = [
            "git",
            "-C",
            "repo_path",
            "show",
            "--name-only",
            "--pretty=",
            commit_hash,
        ]

        files_result = subprocess.run(files_cmd, capture_output=True, text=True)
        for file in files_result.stdout.splitlines():
            if file.strip():
                conn.execute(
                    "INSERT INTO commit_files VALUES (?,?)",(commit_hash, file.strip())
                )