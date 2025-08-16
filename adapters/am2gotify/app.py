from flask import Flask, request, jsonify
import os, requests

app = Flask(__name__)

GOTIFY_URL   = os.getenv("GOTIFY_URL",   "http://gotify")     # Example on Docker network: http://gotify
GOTIFY_TOKEN = os.getenv("GOTIFY_TOKEN", "")                  # Gotify Application token (required)

@app.post("/webhook")
def webhook():
    data   = request.get_json(silent=True) or {}
    status = data.get("status", "firing")
    alerts = data.get("alerts", [])

    if not GOTIFY_TOKEN:
        return jsonify({"ok": False, "err": "missing GOTIFY_TOKEN"}), 500

    for a in alerts:
        labels = a.get("labels", {})
        ann    = a.get("annotations", {})
        title  = ann.get("summary") or labels.get("alertname") or "Alert"
        body   = "\n".join(filter(None, [
            f"status: {status}",
            f"alertname: {labels.get('alertname','')}",
            f"severity: {labels.get('severity','')}",
            f"instance: {labels.get('instance','')}",
            ann.get("description","").strip()
        ]))

        # Gotify JSON API
        r = requests.post(
            f"{GOTIFY_URL}/message",
            json={"title": title, "message": body, "priority": 5},
            headers={"X-Gotify-Key": GOTIFY_TOKEN},
            timeout=5,
        )
        r.raise_for_status()

    return jsonify({"ok": True})
