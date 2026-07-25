"""Re-walk the audit chain; report the first broken link."""
import hashlib, json, pathlib, sys
LOG = pathlib.Path("audit/chain.jsonl")
prev = "0"*64; n = 0
for i, line in enumerate(LOG.read_text().splitlines()):
    e = json.loads(line)
    h = hashlib.sha256((prev + json.dumps(e["event"], sort_keys=True)).encode()).hexdigest()
    if h != e["hash"] or e["prev"] != prev:
        print(f"Chain BROKEN at entry #{i}"); sys.exit(1)
    prev = h; n += 1
print(f"Chain OK — {n} entries, head={prev[:16]}…")
