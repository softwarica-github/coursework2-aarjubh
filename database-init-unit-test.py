import unittest
import sqlite3
from initialize_database import initialize_database

class TestDatabaseInitialization(unittest.TestCase):

    def setUp(self):
        # Create an in-memory database for testing
        self.conn = sqlite3.connect(":memory:")
        self.cursor = self.conn.cursor()

    def test_database_initialized(self):
        initialize_database(self.cursor)
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = self.cursor.fetchall()
        expected_tables = [('users',), ('votes',)]
        self.assertEqual(tables, expected_tables)

    def tearDown(self):
        self.conn.close()

if __name__ == '__main__':
    unittest.main()
