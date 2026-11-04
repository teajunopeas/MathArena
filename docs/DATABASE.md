# Database layer

This document describes the current SQLite schema and the intended role of the functions in `src/database.py`. The module is a learning-stage implementation; the notes below distinguish the current code from behavior that still needs correction or verification.

## Architecture

`database.py` contains small database operations as functions. Each operation accepts a database path, runs a parameterized SQL statement, and returns useful data rather than exposing a cursor to its caller.

The intended call flow is:

```text
application or script
        ↓
database.py function
        ↓
SQLite connection
        ↓
MathArena database file
```

SQLite handles persistence. Python's standard-library `sqlite3` module is sufficient for this layer; no database server or ORM is currently required.

## Tables

| Table | Purpose | Key relationships |
| --- | --- | --- |
| `problems` | Stores a problem statement, difficulty, and language. | `id` is the primary key. |
| `topics` | Stores topic names and an optional parent topic. | `parent_id` references `topics.id`, allowing a topic hierarchy. |
| `problem_topics` | Connects problems to topics. | Composite primary key `(problem_id, topic_id)`; both columns are foreign keys. |
| `sources` | Stores source metadata such as name, URL, and license. | Text `id` is the primary key. |
| `problem_sources` | Connects a problem to a source and records its original source ID. | Composite primary key `(problem_id, source_id)`; both columns are foreign keys. |
| `attempts` | Stores a user's written response and timestamps for a problem. | `problem_id` references `problems.id`. |

The relationships support multiple topics per problem, multiple problems per topic, multiple sources per problem, and multiple attempts per problem.

## Current functions

| Function | Intended result |
| --- | --- |
| `open_database(path)` | Context manager that opens a connection, configures row access and foreign-key behavior, manages the transaction, and closes the connection. |
| `initialize_database(path)` | Creates the tables if they do not already exist. |
| `add_problem(path, statement, difficulty, language)` | Inserts a problem and returns its generated ID. |
| `get_problem(path, problem_id)` | Returns one problem as a dictionary, or `None` if it is not found. |
| `update_problem(path, problem_id, changes)` | Updates allowed problem fields and returns whether a row was affected. |
| `delete_problem(path, problem_id)` | Deletes a problem and returns whether a row was affected. |
| `list_problems(path, limit=20)` | Returns up to `limit` problem dictionaries. The query currently has no explicit order. |
| `add_topic(path, name, parent_id=None)` | Inserts a topic and returns its generated ID. |
| `link_problem_to_topic(path, problem_id, topic_id)` | Adds a problem-topic relationship; duplicate pairs are ignored. |
| `save_attempt(path, problem_id, response_text, completed_at=None)` | Saves an attempt and returns its generated ID. |
| `load_attempt(path, attempt_id)` | Returns one attempt as a dictionary, or `None` if it is not found. |
| `get_attempts(path, problem_id)` | Returns the attempts for one problem as a list of dictionaries. |
| `delete_attempt(path, attempt_id)` | Deletes an attempt and returns whether a row was affected. |

## Connection and transaction behavior

SQLite connections are created with `sqlite3.connect`. A connection context (`with connection:`) commits a successful transaction or rolls it back after an error; it does not itself close the connection. The `open_database` context manager combines transaction handling with explicit connection closing.

The current module defines `open_database`, but most CRUD functions still call `sql.connect` directly. They should eventually use the shared helper so connection behavior is consistent.

Foreign-key checks are connection-specific in SQLite. The current helper intends to enable them, but the pragma is misspelled as `forein_keys`; it must be `foreign_keys`. Some functions also bypass the helper, so foreign-key enforcement is not consistently active yet.

## Important implementation checks

- `initialize_database` contains several `CREATE TABLE` statements in `executescript`; statements must be separated with semicolons.
- `get_problem` should query the declared primary-key column `problems.id`.
- `update_problem` accepts a dictionary of changes. Only column names from its allowlist may be inserted into the SQL statement; values must continue to use `?` parameters.
- Enable foreign keys on every connection used for relationship changes. Decide later whether deleting a problem should cascade to attempts and link rows or be restricted.
- Add an `ORDER BY` clause where stable ordering is required; `LIMIT` alone does not define which rows come first.
- The current `problems` table does not yet contain an official-solution column. Add it only when the data model is ready to store that content.
- Functions for `sources` and `problem_sources` have not been implemented yet.

## Suggested manual learning checks

Use a temporary database while learning. Check one operation at a time:

1. Initialize the database twice and confirm existing rows are preserved.
2. Insert a problem and retrieve it by its returned ID.
3. Update one field and confirm the other fields remain unchanged.
4. Add a topic and link it to a problem; try an invalid ID after foreign keys are enabled.
5. Save, retrieve, list, and delete an attempt.
6. Query an ID that does not exist and confirm the function's documented return value.

These are suggested checks, not a claim that the current implementation has passed them.
