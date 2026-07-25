"""Demo 6b — Tamper-evident audit log (hash chain) for model decisions."""
import hashlib, json, os, time, pathlib
LOG = pathlib.Path("compliance/audit.log")
LOG.parent.mkdir(exist_ok=True)

def append(event: dict):
    prev = LOG.read_text().splitlines()[-1] if LOG.exists() and LOG.stat().st_size else ""
    prev_hash = json.loads(prev)["hash"] if prev else "GENESIS"
    payload = {"ts": time.time(), "event": event, "prev": prev_hash}
    payload["hash"] = hashlib.sha256(
        (prev_hash + json.dumps(event, sort_keys=True)).encode()).hexdigest()
    with LOG.open("a") as f: f.write(json.dumps(payload) + "\n")
    return payload["hash"]

def verify():
    prev_hash = "GENESIS"; ok = True
    for line in LOG.read_text().splitlines():
        e = json.loads(line)
        expected = hashlib.sha256(
            (prev_hash + json.dumps(e["event"], sort_keys=True)).encode()).hexdigest()
        if expected != e["hash"]: ok = False; break
        prev_hash = e["hash"]
    return ok

for ev in [
    {"action": "model_promoted", "model": "loan-approval", "version": "1.0.3"},
    {"action": "policy_denied",  "model": "loan-approval", "reason": "DI<0.8"},
    {"action": "model_retrained_with_reweighing", "model": "loan-approval"},
]:
    print("logged:", append(ev)[:16], ev["action"])
print("chain valid:", verify())
