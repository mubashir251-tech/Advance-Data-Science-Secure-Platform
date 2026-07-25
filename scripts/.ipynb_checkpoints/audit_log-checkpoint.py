"""Tamper-evident hash-chained JSONL audit log."""
import argparse, hashlib, json, pathlib, time, sys
LOG = pathlib.Path("audit/chain.jsonl"); LOG.parent.mkdir(exist_ok=True)

def head_hash():
    if not LOG.exists() or LOG.stat().st_size == 0: return "0"*64
    last = LOG.read_text().strip().splitlines()[-1]
    return json.loads(last)["hash"]

def append(event: dict):
    prev = head_hash()
    payload = {"ts": time.time(), "prev": prev, "event": event}
    h = hashlib.sha256((prev + json.dumps(event, sort_keys=True)).encode()).hexdigest()
    payload["hash"] = h
    with LOG.open("a") as f: f.write(json.dumps(payload) + "\n")
    print(f"appended  hash={h[:16]}…")

ap = argparse.ArgumentParser()
sub = ap.add_subparsers(dest="cmd", required=True)
sub.add_parser("genesis")
p = sub.add_parser("predict"); p.add_argument("--input", required=True)
p = sub.add_parser("event"); p.add_argument("--json", required=True)
a = ap.parse_args()
if a.cmd == "genesis": append({"type": "genesis"})
elif a.cmd == "predict":
    payload = json.loads(pathlib.Path(a.input).read_text())
    append({"type": "predict", "input": payload, "decision": "approved"})
elif a.cmd == "event":
    append(json.loads(a.json))
