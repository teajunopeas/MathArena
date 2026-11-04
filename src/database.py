import sqlite3 as sql
from contextlib import closing, contextmanager
from pathlib import Path


@contextmanager
def _open_database(database_path: Path):
    """
    Open a database connection and close it when the context exits.

    Args:
        database_path: Path to the SQLite database file.

    Yields:
        An SQLite connection with row access and foreign keys configured.
    """
    with closing(sql.connect(database_path)) as connection:
        connection.row_factory = sql.Row
        connection.execute("PRAGMA foreign_keys = ON")
        with connection:
            yield connection

# Create the database tables if they do not exist.
def initialize_database(database_path: Path):
    """Initialize the database and create its tables if needed."""

    with _open_database(database_path) as connection:
        # Create the schema if it does not exist.
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS problems (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                statement TEXT NOT NULL,
                difficulty TEXT NOT NULL,
                language TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS topics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                parent_id INTEGER,
                FOREIGN KEY (parent_id) REFERENCES topics (id)
            );

            CREATE TABLE IF NOT EXISTS problem_topics (
                problem_id INTEGER NOT NULL,
                topic_id INTEGER NOT NULL,
                PRIMARY KEY (problem_id, topic_id),
                FOREIGN KEY (problem_id) REFERENCES problems (id),
                FOREIGN KEY (topic_id) REFERENCES topics (id)
            );

            CREATE TABLE IF NOT EXISTS sources (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                url TEXT,
                license TEXT
            );

            CREATE TABLE IF NOT EXISTS problem_sources (
                problem_id INTEGER NOT NULL,
                source_id TEXT NOT NULL,
                original_id TEXT,
                PRIMARY KEY (problem_id, source_id),
                FOREIGN KEY (problem_id) REFERENCES problems (id),
                FOREIGN KEY (source_id) REFERENCES sources (id)
            );


            CREATE TABLE IF NOT EXISTS attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                problem_id INTEGER NOT NULL,
                response_text TEXT NOT NULL,
                started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP,
                FOREIGN KEY (problem_id) REFERENCES problems (id)
            );

            """
        )




def add_problem(
    database_path: Path,
    statement: str,
    difficulty: str,
    language: str
) -> int:
    """Add a problem to the database.

    Args:
        database_path: Path to the SQLite database file.
        statement: The problem statement.
        difficulty: The difficulty level of the problem.
        language: The language in which the problem is written.

    Returns:
        The ID of the inserted row.
    """
    with _open_database(database_path) as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO problems (statement, difficulty, language)
            VALUES (?, ?, ?)
            """,
            (statement, difficulty, language),
        )
        return cursor.lastrowid


def get_problem(
    database_path: Path,
    problem_id: int
) -> dict | None:
    """
    Retrieve a problem using the ID from the database.

    Args:
        database_path: Path to the SQLite database file.
        problem_id: The ID of the problem.

    Returns:
        A dictionary containing the information about the problem, or None if not found.
    """
    with _open_database(database_path) as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT *
            FROM problems
            WHERE id = ?
            """,
            (problem_id,),
        )
        row = cursor.fetchone()
        return dict(row) if row is not None else None


def update_problem(database_path: Path, problem_id: int, changes: dict) -> bool:
    """Update a problem in the database.

    Args:
        database_path: Path to the SQLite database file.
        problem_id: The ID of the problem to update.
        changes: A dictionary containing the changes to be applied.
    """
    allowed_fields = {"statement", "difficulty", "language"}
    fields = {
        name: value
        for name, value in changes.items()
        if name in allowed_fields
    }

    if not fields:
        return False

    assignments = ", ".join(f"{name} = ?" for name in fields.keys())
    values = list(fields.values()) + [problem_id]

    with _open_database(database_path) as connection:
        cursor = connection.cursor()
        cursor.execute(
            f"""
            UPDATE problems
            SET {assignments}
            WHERE id = ?
            """,
            tuple(values),
        )

        return cursor.rowcount > 0


def delete_problem(database_path: Path, problem_id: int) -> bool:
    """Delete a problem from the database.

    Args:
        database_path: Path to the SQLite database file.
        problem_id: The ID of the problem to delete.

    Returns:
        True if the problem was deleted, False otherwise.
    """
    with _open_database(database_path) as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            DELETE FROM problems
            WHERE id = ?
            """,
            (problem_id,),
        )
        return cursor.rowcount > 0

# TODO: Add functionality for filtering results instead of returning all problems. This will be useful for future features like searching by difficulty or language.
def list_problems(database_path: Path, limit = 20) -> list[dict]:
    """
    List all problems in the database.

    Args:
        database_path: Path to the SQLite database file.
        limit: The maximum number of problems to return.
    Returns:
        A list of dictionaries, each containing information about a problem.
    """
    with _open_database(database_path) as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT *
            FROM problems
            ORDER BY id
            LIMIT ?
            """,
            (limit,)
        )
        rows = cursor.fetchall()
        return [dict(row) for row in rows]


def add_topic(database_path: Path, name: str, parent_id: int | None = None) -> int:
    """Add a topic to the database.

    Args:
        database_path: Path to the SQLite database file.
        name: The name of the topic.
        parent_id: The ID of the parent topic, if any.

    Returns:
        The ID of the inserted row.
    """
    with _open_database(database_path) as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO topics (name, parent_id)
            VALUES (?, ?)
            """,
            (name, parent_id),
        )
        return cursor.lastrowid

def link_problem_to_topic(database_path: Path, problem_id: int, topic_id: int):
    """Link a problem to a topic in the database.

    Args:
        database_path: Path to the SQLite database file.
        problem_id: The ID of the problem.
        topic_id: The ID of the topic.
    """
    with _open_database(database_path) as connection:

        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT OR IGNORE INTO problem_topics (problem_id, topic_id)
            VALUES (?, ?)
            """,
            (problem_id, topic_id),
        )

def save_attempt(database_path: Path, problem_id: int, response_text: str, completed_at: str | None = None) -> int:
    """Save an attempt to the database.

    Args:
        database_path: Path to the SQLite database file.
        problem_id: The ID of the problem.
        response_text: The text of the user's response.
        completed_at: The timestamp when the attempt was completed, if any.

    Returns:
        The ID of the inserted row.
    """
    with _open_database(database_path) as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO attempts (problem_id, response_text, completed_at)
            VALUES (?, ?, ?)
            """,
            (problem_id, response_text, completed_at),
        )
        return cursor.lastrowid

def load_attempt(database_path: Path, attempt_id: int) -> dict | None:
    """Load an attempt from the database.

    Args:
        database_path: Path to the SQLite database file.
        attempt_id: The ID of the attempt.

    Returns:
        A dictionary containing information about the attempt, or None if not found.
    """
    with _open_database(database_path) as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT * FROM attempts WHERE id = ?
            """,
            (attempt_id,),
        )
        row = cursor.fetchone()

        return dict(row) if row is not None else None


def get_attempts(database_path: Path, problem_id: int) -> list[dict]:
    """Retrieve all attempts for a specific problem from the database.

    Args:
        database_path: Path to the SQLite database file.
        problem_id: The ID of the problem.

    Returns:
        A list of dictionaries, each containing information about an attempt.
    """
    with _open_database(database_path) as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT * FROM attempts WHERE problem_id = ? ORDER BY id
            """,
            (problem_id,),
        )
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

def delete_attempt(database_path: Path, attempt_id: int) -> bool:
    """Delete an attempt from the database.

    Args:
        database_path: Path to the SQLite database file.
        attempt_id: The ID of the attempt to delete.

    Returns:
        True if the attempt was deleted, False otherwise.
    """
    with _open_database(database_path) as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            DELETE FROM attempts
            WHERE id = ?
            """,
            (attempt_id,),
        )
        return cursor.rowcount > 0

