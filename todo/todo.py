#!/usr/bin/env python3
"""Simple command-line to-do list.

Tasks are stored in a JSON file next to this script (``tasks.json``).

Usage examples:
    python todo.py add "Call the broker about 123 Main St"
    python todo.py list
    python todo.py done 2
    python todo.py remove 2
    python todo.py clear
"""

import argparse
import json
import os
from datetime import datetime

TASKS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tasks.json")


def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    try:
        with open(TASKS_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return []


def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=2)


def next_id(tasks):
    return max((t["id"] for t in tasks), default=0) + 1


def add_task(text):
    tasks = load_tasks()
    task = {
        "id": next_id(tasks),
        "text": text,
        "done": False,
        "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"Added task #{task['id']}: {text}")


def list_tasks(show_all=True):
    tasks = load_tasks()
    if not tasks:
        print("No tasks yet. Add one with:  python todo.py add \"your task\"")
        return

    pending = [t for t in tasks if not t["done"]]
    completed = [t for t in tasks if t["done"]]

    print(f"TO-DO LIST  ({len(pending)} pending, {len(completed)} done)")
    print("=" * 60)
    for t in tasks:
        mark = "[x]" if t["done"] else "[ ]"
        print(f"  {mark} #{t['id']:<3} {t['text']}")
    print("=" * 60)


def _find(tasks, task_id):
    for t in tasks:
        if t["id"] == task_id:
            return t
    return None


def complete_task(task_id):
    tasks = load_tasks()
    task = _find(tasks, task_id)
    if not task:
        print(f"No task with id #{task_id}.")
        return
    task["done"] = True
    save_tasks(tasks)
    print(f"Completed task #{task_id}: {task['text']}")


def remove_task(task_id):
    tasks = load_tasks()
    task = _find(tasks, task_id)
    if not task:
        print(f"No task with id #{task_id}.")
        return
    tasks = [t for t in tasks if t["id"] != task_id]
    save_tasks(tasks)
    print(f"Removed task #{task_id}: {task['text']}")


def clear_tasks():
    save_tasks([])
    print("Cleared all tasks.")


def build_parser():
    parser = argparse.ArgumentParser(description="A simple command-line to-do list.")
    sub = parser.add_subparsers(dest="command")

    p_add = sub.add_parser("add", help="Add a new task")
    p_add.add_argument("text", help="Task description")

    sub.add_parser("list", help="List all tasks")

    p_done = sub.add_parser("done", help="Mark a task as done")
    p_done.add_argument("id", type=int, help="Task id")

    p_remove = sub.add_parser("remove", help="Remove a task")
    p_remove.add_argument("id", type=int, help="Task id")

    sub.add_parser("clear", help="Remove all tasks")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "add":
        add_task(args.text)
    elif args.command == "list":
        list_tasks()
    elif args.command == "done":
        complete_task(args.id)
    elif args.command == "remove":
        remove_task(args.id)
    elif args.command == "clear":
        clear_tasks()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
