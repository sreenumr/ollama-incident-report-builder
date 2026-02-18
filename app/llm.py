from schemas import Report
import requests,json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5-coder:3b"

def generate_report(timeline_text : str) -> Report:

    prompt = f"""
        You are a senior DevOps Engineer writing a post-incident report.

        Given this incident timeline, produce a JSON object with EXACTLY these fields:
        - summary (string)
        - impact (string)
        - root_cause (string)
        - factors (array of strings)
        - action_items (array of strings)

        Rules:
        - Base everything strictly on the provided timeline.
        - Do not invent facts.
        - Do not include any text outside the JSON.
        - Do not wrap in markdown.

        Timeline:
    {timeline_text}
    """

    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
    }

    resp = requests.post(OLLAMA_URL, json=payload, timeout=300)
    resp.raise_for_status()

    data = resp.json()

    raw = data.get("response", "").strip()
    if raw.startswith("```"):
        raw = raw.strip("`")
        raw = raw.replace("json", "", 1).strip()

    raw = raw.replace("```", "").strip()
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"LLM did not return valid JSON:\n{raw}") from e

    return Report(**parsed)