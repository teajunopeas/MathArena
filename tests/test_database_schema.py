import tempfile
import unittest
from pathlib import Path

from src.database import (
    add_problem,
    add_topic,
    delete_attempt,
    get_attempts,
    get_problem,
    initialize_database,
    link_problem_to_topic,
    load_attempt,
    save_attempt,
)


class DatabaseTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.database_path = Path(self.temp_dir.name) / "test.db"
        initialize_database(self.database_path)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_problem_and_attempt_cycle(self):
        problem_id = add_problem(
            self.database_path,
            "Show that the sum of two even integers is even.",
            "beginner",
            "en",
        )

        problem = get_problem(self.database_path, problem_id)
        self.assertEqual(problem["statement"], "Show that the sum of two even integers is even.")

        attempt_id = save_attempt(
            self.database_path,
            problem_id,
            "Let the integers be 2a and 2b. Their sum is 2(a+b).",
        )

        attempt = load_attempt(self.database_path, attempt_id)
        self.assertEqual(attempt["problem_id"], problem_id)

        attempts = get_attempts(self.database_path, problem_id)
        self.assertEqual(len(attempts), 1)

        self.assertTrue(delete_attempt(self.database_path, attempt_id))
        self.assertIsNone(load_attempt(self.database_path, attempt_id))

    def test_problem_can_be_linked_to_topic(self):
        problem_id = add_problem(
            self.database_path,
            "Find the derivative of x².",
            "beginner",
            "en",
        )
        topic_id = add_topic(self.database_path, "calculus")

        link_problem_to_topic(self.database_path, problem_id, topic_id)

        # For a fuller test, add a function that reads problem-topic links.
        self.assertIsNotNone(get_problem(self.database_path, problem_id))


if __name__ == "__main__":
    unittest.main()
