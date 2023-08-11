import unittest
import sqlite3
from user_registration import generate_otp

class TestUserRegistration(unittest.TestCase):

    def setUp(self):
        # Create an in-memory database for testing
        self.conn = sqlite3.connect(":memory:")
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE users (
            voter_id TEXT PRIMARY KEY,
            otp_secret TEXT
        )''')
        self.conn.commit()

    def test_generate_otp(self):
        otp_secret = 'EXAMPLE_SECRET'
        generated_otp = generate_otp(otp_secret)
        self.assertIsInstance(generated_otp, str)
        self.assertEqual(len(generated_otp), 6)

    def tearDown(self):
        self.conn.close()

if __name__ == '__main__':
    unittest.main()
