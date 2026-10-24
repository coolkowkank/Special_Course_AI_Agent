import uuid
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "cabinet_db.json")

class ContextCabinet:
    def __init__(self):
        if os.path.exists(DB_FILE):
            with open(DB_FILE, "r") as f:
                self.items = json.load(f)
        else:
            self.items = []
            self.add_item("CUSTOMER", "Looking to buy a two-bedroom flat near the metro in 18 months.", status="ACTIVE", risk="LOW")
            self.add_item("CUSTOMER", "Save for a new car (Set in 2023)", status="ACTIVE", risk="LOW")

    def _save(self):
        with open(DB_FILE, "w") as f:
            json.dump(self.items, f, indent=4)

    def add_item(self, source: str, content: str, status: str = "PENDING", risk: str = "LOW", reason: str = None):
        item_id = str(uuid.uuid4())[:8]
        item = {"id": item_id, "source": source, "content": content, "status": status, "risk": risk.upper()}
        if reason:
            item["reason"] = reason
        self.items.append(item)
        self._save()
        return item_id

    def get_items_by_status(self, status: str):
        return [item for item in self.items if item["status"] == status]

    def update_status(self, item_id: str, new_status: str):
        for item in self.items:
            if item["id"] == item_id:
                item["status"] = new_status
                break
        self._save()

    def get_active_context_string(self):
        active_items = self.get_items_by_status("ACTIVE")
        if not active_items: return "No context available."
        return "\n".join([f"- [{item['source']}] {item['content']}" for item in active_items])

    def get_muted_facts(self):
        return [item["content"] for item in self.get_items_by_status("MUTED")]