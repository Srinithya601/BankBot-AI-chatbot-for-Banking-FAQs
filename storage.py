import json
import os
import uuid

STORAGE_FILE = "chat_history.json"

def load_storage():
    if not os.path.exists(STORAGE_FILE):
        return {"conversations": {}, "active_chat": None}

    with open(STORAGE_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    fixed = {}
    for cid, chat in data.get("conversations", {}).items():
        fixed[cid] = {
            "title": chat.get("title", "New Chat"),
            "messages": chat.get("messages", [])
        }

    data["conversations"] = fixed
    data["active_chat"] = data["active_chat"] if data["active_chat"] in fixed else next(iter(fixed), None)
    return data

def save_storage(data):
    with open(STORAGE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def create_new_chat(history):
    chat_id = str(uuid.uuid4())
    history["conversations"][chat_id] = {
        "title": "New Chat",
        "messages": [
            {"role": "assistant", "text": "Hello! I'm BankBot — how can I help you today?"}
        ]
    }
    history["active_chat"] = chat_id
    return history
