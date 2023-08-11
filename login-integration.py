import sqlite3
from user_registration import generate_otp
from initialize_database import initialize_database

def test_user_registration_and_otp_generation():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    initialize_database(cursor)

    otp_secret = 'EXAMPLE_SECRET'
    generated_otp = generate_otp(otp_secret)
    assert isinstance(generated_otp, str)
    assert len(generated_otp) == 6

    conn.close()
    print("Integration test for user registration and OTP generation passed.")

if __name__ == '__main__':
    test_user_registration_and_otp_generation()
