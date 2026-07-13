# Daily To-Do Email

Sends your open to-do items to your inbox every morning at 7:30 AM
(America/Sao_Paulo time), using GitHub Actions — no server or computer of
yours needs to stay on. Items you mark done disappear from the daily list
but are never deleted — full history is kept in `todo.json`.

## How it works
- `todo.json` — the data file. Each item has a status (`open`/`done`), a
  created date, and a completed date. Nothing is ever erased.
- `manage_todo.py` — command-line tool to add items or mark them done/reopened.
- `send_todo.py` — reads `todo.json`, emails all **open** items as a numbered
  list, plus a short "recently completed" section (last 3 days) for context.
- `../.github/workflows/daily-todo-email.yml` — GitHub Actions workflow that
  runs `send_todo.py` automatically every day at 10:30 UTC (07:30 in São Paulo).

## Updating your list day-to-day
From a terminal, in the repo root:

```bash
python todo/manage_todo.py add "Call the bank about the wire"
python todo/manage_todo.py done 3
python todo/manage_todo.py list       # see what's still open
python todo/manage_todo.py history    # see everything ever completed, with dates
python todo/manage_todo.py reopen 3   # undo a mistaken "done"
```

After any change, commit and push so the next email reflects it:
```bash
git add todo/todo.json && git commit -m "Update todo list" && git push
```

If you don't want to touch a terminal at all, you can also edit
`todo/todo.json` directly on GitHub.com (open the file, click the pencil icon,
edit the JSON, commit) — a little more fiddly but no local setup needed.

## One-time setup

The code is already committed to this repo (`assetmgmt`). You only need to add
the email credentials as GitHub Actions secrets.

1. **Create an Outlook app password.**
   Outlook/Office365 accounts with modern authentication won't accept your
   normal password for SMTP. Go to
   https://account.microsoft.com/security → Advanced security options →
   App passwords, and generate one. Use this instead of your login password.
   (If your account uses OAuth-only / school-or-work tenant restrictions,
   an admin may need to enable app passwords or SMTP AUTH first.)

2. **Add GitHub repo secrets.**
   In the repo: Settings → Secrets and variables → Actions → New repository secret.
   Add these three:
   - `EMAIL_ADDRESS` — your Outlook address (the sender)
   - `EMAIL_PASSWORD` — the app password from step 1
   - `EMAIL_TO` — the address you want the list sent to (can be the same address)

3. **Test it manually.**
   In the repo: Actions tab → "Daily To-Do Email" workflow → "Run workflow"
   button. Check your inbox — you should get the email within a minute or two.

4. **Done.** From now on it runs automatically every day at 07:30 São Paulo
   time. To change the time, edit the `cron` line in
   `../.github/workflows/daily-todo-email.yml` (format: minute hour * * *, in UTC).
