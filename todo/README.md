# To-Do List

A small, dependency-free command-line to-do list. Tasks are saved to
`tasks.json` in this folder.

## Usage

```bash
cd todo

# Add a task
python todo.py add "Call the broker about 123 Main St"

# List all tasks
python todo.py list

# Mark task #2 as done
python todo.py done 2

# Remove task #2
python todo.py remove 2

# Clear all tasks
python todo.py clear
```

## Notes

- No external dependencies — uses only the Python standard library.
- `tasks.json` is created automatically on the first `add`.
