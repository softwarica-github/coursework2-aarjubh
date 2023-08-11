import sqlite3
from admin_page import AdminPage
from initialize_database import initialize_database

def test_admin_page_candidate_search():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    initialize_database(cursor)
    cursor.execute('''INSERT INTO votes (presidential, presidential_count, provincial, provincial_count, none_count)
        VALUES ('Candidate 1', 10, 'Candidate A', 15, 5)''')
    conn.commit()

    root = None  # Mock the root object
    admin_page = AdminPage(root)
    admin_page.cursor = cursor  # Set the mock cursor
    admin_page.search_entry = "Candidate 1"

    admin_page.search_candidate()

    expected_result = "Candidate Counts:\nCandidate A: 15\nCandidate 1: 10\nNone: 5"
    assert admin_page.result_label.cget("text") == expected_result

    conn.close()
    print("Integration test for admin page candidate search passed.")

if __name__ == '__main__':
    test_admin_page_candidate_search()
