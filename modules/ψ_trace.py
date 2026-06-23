# 🔹 Save as: ~/psi_lab/modules/ψ_trace.py

import os
import json
from datetime import datetime

class GlifEventLogger:
    def __init__(self, path="~/psi_lab/logs/events.json"):
        self.path = os.path.expanduser(path)
        os.makedirs(os.path.dirname(self.path), exist_ok=True)

    def record(self, event_type, glif_id, data):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "event": event_type,
            "glif": glif_id,
            "data": data
        }
        try:
            with open(self.path, "a") as f:
                f.write(json.dumps(entry) + "\n")
            print(f"[ψ_trace] Event: {event_type} | Glif: {glif_id}")
        except Exception as e:
            print(f"[ψ_trace][ERROR] Failed to write log: {e}")

# Global trace instance
ψ_trace = GlifEventLogger()
