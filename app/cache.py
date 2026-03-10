import redis
import hashlib
import json

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

def build_cache_key(incident_id: str, timeline_text: str, repo_context: str) -> str:
    fingerprint = hashlib.sha256(
        (timeline_text + repo_context).encode()
    ).hexdigest()

    return f"incident:{incident_id}:{fingerprint}"

def get_cached_report(key: str):
    return r.get(key)

def set_cached_report(key: str, report: str, ttl=3600):
    r.set(key, report, ex=ttl)