#!/usr/bin/env bash
# Run 1 Flower server + 3 clients in one terminal (background).
set -euo pipefail
cd "$(dirname "$0")/.."
source .venv-flower/bin/activate
mkdir -p reports
python scripts/flower_server.py > reports/flower_server.log 2>&1 &
SERVER=$!
sleep 2
for i in 0 1 2; do
  python scripts/flower_client.py $i > reports/flower_client_$i.log 2>&1 &
done
wait $SERVER || true
echo "=== server tail ==="; tail -20 reports/flower_server.log
echo "=== client 0 tail ==="; tail -10 reports/flower_client_0.log
