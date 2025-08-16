# Prometheus Monitoring Lab — Docker Compose Quickstart

Spin up a full local monitoring stack in minutes:

- **Prometheus** (9090): scrape, rules, alerts  
- **Alertmanager** (9093): routes alerts to **Gotify** via **am2gotify**  
- **Blackbox Exporter** (9115): HTTP/TCP/ICMP probes  
- **Node Exporter A/B** (9100 container → host 9101/9102): host metrics  
- **Webapp** (8000): demo counter metric  
- **Grafana** (3000): dashboards  
- **VictoriaMetrics** (8428): optional remote storage  
- **Gotify** (8082 host → 80 container): notifications

---

## Prerequisites

- Docker + Docker Compose v2
- (Optional) A **Gotify** Application token (create it at `http://localhost:8082` → *Applications*).  
  Put it in `docker-compose.yml` (service **am2gotify** → `GOTIFY_TOKEN=`) or via `.env`.

---

## Quick start

```bash
# From repo root
docker-compose up -d --build
```

### Open the UIs

- __Prometheus__ → http://localhost:9090
- __Alertmanager__ → http://localhost:9093
- __Grafana__ → http://localhost:3000 (login: admin / admin, then change)
- __Gotify__ → http://localhost:8082 (create an Application → copy token)
- __VictoriaMetrics (optional)__ → http://localhost:8428

---

## Prometheus: check & reload

```bash
# Validate config inside the container
promtool check config ./prometheus/prometheus.yml

# Reload Prometheus after editing configs/rules
curl -X POST http://localhost:9090/-/reload
```

---

## Ports (quick reference)

| Service           | Container Port | Host Port |
| ----------------- | -------------- | --------- |
| Prometheus        | 9090           | 9090      |
| Alertmanager      | 9093           | 9093      |
| Blackbox Exporter | 9115           | 9115      |
| Node Exporter A   | 9100           | 9101      |
| Node Exporter B   | 9100           | 9102      |
| Webapp            | 8000           | 8000      |
| Grafana           | 3000           | 3000      |
| VictoriaMetrics   | 8428           | 8428      |
| Gotify            | 80             | 8082      |
| am2gotify         | 5000           | 5001      |

---

## Send a test alert to Alertmanager (routes to Gotify)

> The Alertmanager config in this lab routes severity=warning, team=platform (and notify="gotify") to Gotify via am2gotify.

```bash
curl -sS -XPOST http://localhost:9093/api/v2/alerts \
  -H 'Content-Type: application/json' -d @- <<'JSON'
[
  {
    "labels": { "alertname":"GotifyOnly", "severity":"warning", "team":"platform" },
    "annotations": { "summary":"Gotify only", "description":"Warning for platform" },
    "startsAt": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  }
]
JSON
```

## Test Gotify directly

```bash
# Replace with your Gotify Application token
curl "http://localhost:8082/message?token=YOUR_APP_TOKEN" \
  -F "title=Test" -F "message=Hello from lab" -F "priority=5"
```

---

## Troubleshooting

- Panel shows “No data” → Prometheus → Status → Targets: targets should be UP.
- Recording-rule panels empty → Prometheus → Status → Rules; then reload:

```bash
curl -X POST http://localhost:9090/-/reload
```

- Blackbox Stat is 0 → the /healthz probe may intentionally fail; switch target to / or implement the endpoint.
- Only one node appears → scrape container port 9100 inside the Docker network (host mappings are 9101/9102).

---

## Stop the stack

```bash
docker-compose down
```
