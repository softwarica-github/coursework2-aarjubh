import tkinter as tk
from tkinter import ttk
import sqlite3

class AdminPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Page")

        self.connection = sqlite3.connect("voting_system7.db")
        self.cursor = self.connection.cursor()

        self.create_widgets()

    def create_widgets(self):
        self.label = ttk.Label(self.root, text="Admin Page")
        self.label.pack(pady=10)

        self.search_label = ttk.Label(self.root, text="Search Candidate:")
        self.search_label.pack()

        self.search_entry = ttk.Entry(self.root)
        self.search_entry.pack()

        self.search_button = ttk.Button(self.root, text="Search", command=self.search_candidate)
        self.search_button.pack()

        self.result_label = ttk.Label(self.root, text="")
        self.result_label.pack(pady=10)

        self.total_votes_button = ttk.Button(self.root, text="Total Votes Casted", command=self.get_total_votes)
        self.total_votes_button.pack()

        self.connection.commit()

    def search_candidate(self):
        candidate_name = self.search_entry.get()

        query = "SELECT presidential, presidential_count, provincial, provincial_count, none_count FROM votes WHERE presidential=? OR provincial=?"
        self.cursor.execute(query, (candidate_name, candidate_name))
        result = self.cursor.fetchone()

        if result:
            # Sort the counts in descending order
            sorted_counts = sorted([(result[0], result[1]), (result[2], result[3]), ("None", result[4])], key=lambda x: x[1], reverse=True)

            self.result_label.config(text="Candidate Counts:")
            for candidate, count in sorted_counts:
                self.result_label.config(text=self.result_label.cget("text") + f"\n{candidate}: {count}")
        else:
            self.result_label.config(text="Candidate not found")


    def get_total_votes(self):
        query = "SELECT COUNT(*) FROM votes"
        self.cursor.execute(query)
        total_votes = self.cursor.fetchone()[0]

        self.result_label.config(text=f"Total Votes Casted: {total_votes}")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    admin_page = AdminPage(root)
    admin_page.run()
