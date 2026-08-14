#!/usr/bin/env python3
"""
Sends the open items from todo.json as a daily email via Bluewin (Swisscom) SMTP.

Required environment variables (set as GitHub Actions secrets):
  EMAIL_ADDRESS   - the Bluewin address sending the email (e.g. you@bluewin.ch)
  EMAIL_PASSWORD  - the password for that Bluewin account
  EMAIL_TO        - the address the daily list should be sent to (defaults to rkattan@bluewin.ch)
"""

import json
import os
import smtplib
import sys
from datetime import date, timedelta
from email.mime.text import MIMEText

SMTP_SERVER = "smtpauths.bluewin.ch"
SMTP_PORT = 465  # implicit SSL/TLS
TODO_FILE = os.path.join(os.path.dirname(__file__), "todo.json")
RECENT_DAYS = 3  # how many days back to show in the "recently completed" section


def load_data() -> dict:
    if not os.path.exists(TODO_FILE):
        return {"items": []}
    with open(TODO_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def build_email_body(data: dict) -> str:
    items = data.get("items", [])
    open_items = [i for i in items if i["status"] == "open"]

    cutoff = (date.today() - timedelta(days=RECENT_DAYS)).isoformat()
    recently_done = [
        i for i in items
        if i["status"] == "done" and i.get("completed") and i["completed"] >= cutoff
    ]

    lines = []
    if not open_items:
        lines.append("Nothing pending — your to-do list is empty.")
    else:
        for i, item in enumerate(open_items, start=1):
            lines.append(f"{i}. {item['text']}")

    if recently_done:
        lines.append("")
        lines.append(f"Recently completed (last {RECENT_DAYS} days):")
        for item in sorted(recently_done, key=lambda x: x["completed"]):
            lines.append(f"  ✓ {item['text']} ({item['completed']})")

    return "\n".join(lines)


def send_email(subject: str, body: str) -> None:
    sender = os.environ["EMAIL_ADDRESS"]
    password = os.environ["EMAIL_PASSWORD"]
    recipient = os.environ.get("EMAIL_TO", "rkattan@bluewin.ch")

    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = recipient

    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
        server.login(sender, password)
        server.sendmail(sender, [recipient], msg.as_string())


def main() -> int:
    data = load_data()
    body = build_email_body(data)
    subject = f"To-Do List — {date.today().strftime('%A, %B %d, %Y')}"

    try:
        send_email(subject, body)
    except KeyError as e:
        print(f"Missing required environment variable: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Failed to send email: {e}", file=sys.stderr)
        return 1

    open_count = len([i for i in data.get("items", []) if i["status"] == "open"])
    print(f"Sent to-do email with {open_count} open item(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
