import os, time
from prometheus_client import start_http_server, Counter

PORT = int(os.environ.get("PORT", "8000"))
print(f"Starting Prometheus metrics on :{PORT} ...", flush=True)
start_http_server(PORT)

c = Counter("demo_requests_total", "Demo counter")
while True:
    c.inc()
    time.sleep(1)
