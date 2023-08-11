import sqlite3

def initialize_database():
    conn = sqlite3.connect("voting_system7.db")
    cursor = conn.cursor()
    print("Database initialized successfully")

    # Modify your database creation code to include OTP shares
    query_users = """CREATE TABLE IF NOT EXISTS users (
        no_id integer PRIMARY KEY AUTOINCREMENT,
        voter_id UNIQUE,
        first_name text,
        last_name text,
        age integer,
        gender text,
        province text,
        address text,
        otp_secret text,
        generated_otp text
    )"""
    cursor.execute(query_users)

    conn.commit()

    
    # Create the votes table
    query_votes= """CREATE TABLE IF NOT EXISTS votes (
        vote_no integer PRIMARY KEY  AUTOINCREMENT,
        presidential TEXT,
        provincial TEXT,
        presidential_count INTEGER DEFAULT 0,
        provincial_count INTEGER DEFAULT 0,
        none_count INTEGER DEFAULT 0
    )"""
    cursor.execute(query_votes)

    conn.commit()
    

if __name__ == "__main__":
    initialize_database()