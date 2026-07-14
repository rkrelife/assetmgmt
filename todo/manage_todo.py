#!/usr/bin/env python3
"""
Command-line tool to manage todo.json.

Usage:
  python manage_todo.py add "Call the bank about the wire"
  python manage_todo.py done 3
  python manage_todo.py reopen 3
  python manage_todo.py list
  python manage_todo.py history

After running any command that changes the file, commit and push
todo.json so the next scheduled email reflects the update:
  git add todo.json && git commit -m "Update todo list" && git push
"""

import json
import os
import sys
from datetime import date

TODO_FILE = os.path.join(os.path.dirname(__file__), "todo.json")


def load() -> dict:
    if not os.path.exists(TODO_FILE):
        return {"next_id": 1, "items": []}
    with open(TODO_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save(data: dict) -> None:
    with open(TODO_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def cmd_add(data: dict, text: str) -> None:
    item = {
        "id": data["next_id"],
        "text": text,
        "status": "open",
        "created": date.today().isoformat(),
        "completed": None,
    }
    data["items"].append(item)
    data["next_id"] += 1
    save(data)
    print(f"Added #{item['id']}: {text}")


def cmd_done(data: dict, item_id: int) -> None:
    for item in data["items"]:
        if item["id"] == item_id:
            item["status"] = "done"
            item["completed"] = date.today().isoformat()
            save(data)
            print(f"Marked #{item_id} done: {item['text']}")
            return
    print(f"No item with id {item_id}", file=sys.stderr)
    sys.exit(1)


def cmd_reopen(data: dict, item_id: int) -> None:
    for item in data["items"]:
        if item["id"] == item_id:
            item["status"] = "open"
            item["completed"] = None
            save(data)
            print(f"Reopened #{item_id}: {item['text']}")
            return
    print(f"No item with id {item_id}", file=sys.stderr)
    sys.exit(1)


def cmd_list(data: dict) -> None:
    open_items = [i for i in data["items"] if i["status"] == "open"]
    if not open_items:
        print("No open items.")
        return
    for i in open_items:
        print(f"#{i['id']}  {i['text']}")


def cmd_history(data: dict) -> None:
    done_items = [i for i in data["items"] if i["status"] == "done"]
    if not done_items:
        print("Nothing completed yet.")
        return
    for i in sorted(done_items, key=lambda x: x["completed"] or ""):
        print(f"#{i['id']}  [{i['completed']}]  {i['text']}")


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 1

    command = sys.argv[1]
    data = load()

    if command == "add":
        if len(sys.argv) < 3:
            print("Usage: manage_todo.py add \"item text\"", file=sys.stderr)
            return 1
        cmd_add(data, " ".join(sys.argv[2:]))
    elif command == "done":
        cmd_done(data, int(sys.argv[2]))
    elif command == "reopen":
        cmd_reopen(data, int(sys.argv[2]))
    elif command == "list":
        cmd_list(data)
    elif command == "history":
        cmd_history(data)
    else:
        print(f"Unknown command: {command}")
        print(__doc__)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
