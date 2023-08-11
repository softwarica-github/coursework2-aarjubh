import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sqlite3
import os
import base64
import random
import pyotp
from pyotp import TOTP
from pyotp import TOTP
import datetime
import subprocess


def login():
    voter_id = username_entry.get()
    entered_otp = password_entry.get()

    # Replace 'your_database.db' with the path and name of your SQLite database file
    database_file = 'voting_system7.db'

    try:
        conn = sqlite3.connect(database_file)
        cursor = conn.cursor()

        # Check if the voter ID and OTP match in the database
        cursor.execute("SELECT generated_otp FROM users WHERE voter_id=?", (voter_id,))
        user = cursor.fetchone()

        if user:
            stored_otp = user[0]
            if entered_otp == stored_otp:
                print("Login successful. Redirecting to the main page.")
                subprocess.Popen(["python", "main.py"])
                root.destroy()
                # You can use Toplevel or destroy the current login window and create the main window.
            else:
                print("Invalid OTP. Authentication failed.")
        else:
            print("Voter ID not found in the database. Please register first.")

    except sqlite3.Error as e:
        print(f"Error: {e}")
    finally:
        if conn:
            conn.close()
            print("Database connection closed.")
            
def admin_login():
    admin_id = admin_id_entry.get()
    admin_password = admin_password_entry.get()
    
    if admin_id == "2001617" and admin_password == "something":
        subprocess.Popen(["python", "admin.py"])
        root.destroy()
    else:
        messagebox.showerror("Admin Login", "Invalid admin credentials")

def run():
    root.mainloop()


def generate_otp(secret_key):
    totp = TOTP(secret_key, digits=6, interval=30)
    return totp.now()

# Define the submit_registration function
def submit_registration():
    otp_secret_key = pyotp.random_base32()
    generated_otp = generate_otp(otp_secret_key)  # Generate OTP here
    
    conn = sqlite3.connect("voting_system7.db")
    c = conn.cursor()
    existing_voter_id = c.execute("SELECT voter_id FROM users WHERE voter_id = ?", (voter_id_entry.get(),)).fetchone()
    if existing_voter_id:
        print("Voter ID already exists. Registration failed.")
    else:
        c.execute('''
            INSERT INTO users (first_name, last_name, age, gender, voter_id, province, address, otp_secret, generated_otp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (first_name_entry.get(), last_name_entry.get(), age_entry.get(),
            gender_entry.get(), voter_id_entry.get(), province_entry.get(),
            address_entry.get(), otp_secret_key, generated_otp))
        conn.commit()
        conn.close()
        
        print("Generated OTP:", generated_otp)
        messagebox.showinfo("Registration", "Registration successful! OTP generated and printed to terminal.")


root = tk.Tk()
root.title("Voting System")
root.geometry("600x600")

# Create tabs
tab_control = ttk.Notebook(root)
# Login Tab
login_tab = ttk.Frame(tab_control)
tab_control.add(login_tab, text='Login')
tab_control.pack(expand=1, fill="both")

# Registration Tab
registration_tab = ttk.Frame(tab_control)
tab_control.add(registration_tab, text='Registration')

# Login Tab Content
login_frame = ttk.Frame(login_tab, padding=20)
login_frame.pack(fill=tk.BOTH, expand=True)

# Add a rectangular box around the login section
login_box = ttk.Frame(login_frame, borderwidth=2, relief="solid")
login_box.pack(padx=50, pady=50)

image = Image.open("login.png")
image = image.resize((200, 200), Image.LANCZOS)
photo = ImageTk.PhotoImage(image)
image_label = ttk.Label(login_box, image=photo)
image_label.pack(pady=20)

username_label = ttk.Label(login_box, text="Voter ID")
username_label.pack(pady=5)
username_entry = ttk.Entry(login_box)
username_entry.pack(pady=5)

password_label = ttk.Label(login_box, text="OTP")
password_label.pack(pady=5)
password_entry = ttk.Entry(login_box, show="*")
password_entry.pack(pady=5)

authenticate_button = ttk.Button(login_box, text="Authenticate", command=login)
authenticate_button.pack(pady=10)

# Registration Tab Content
registration_frame = ttk.Frame(registration_tab, padding=20)
registration_frame.pack(fill=tk.BOTH, expand=True)

# Registration Fields
first_name_label = ttk.Label(registration_frame, text="First Name")
first_name_label.pack(pady=5)
first_name_entry = ttk.Entry(registration_frame)
first_name_entry.pack(pady=5)

last_name_label = ttk.Label(registration_frame, text="Last Name")
last_name_label.pack(pady=5)
last_name_entry = ttk.Entry(registration_frame)
last_name_entry.pack(pady=5)

age_label = ttk.Label(registration_frame, text="Age")
age_label.pack(pady=5)
age_entry = ttk.Entry(registration_frame)
age_entry.pack(pady=5)

gender_label = ttk.Label(registration_frame, text="Gender")
gender_label.pack(pady=5)
gender_entry = ttk.Entry(registration_frame)
gender_entry.pack(pady=5)

address_label = ttk.Label(registration_frame, text="Address")
address_label.pack(pady=5)
address_entry = ttk.Entry(registration_frame)
address_entry.pack(pady=5)

voter_id_label = ttk.Label(registration_frame, text="Voter ID")
voter_id_label.pack(pady=5)
voter_id_entry = ttk.Entry(registration_frame)
voter_id_entry.pack(pady=5)

province_label = ttk.Label(registration_frame, text="Province")
province_label.pack(pady=5)
province_entry = ttk.Entry(registration_frame)
province_entry.pack(pady=5)

register_button = ttk.Button(registration_frame, text="Register", command=submit_registration)
register_button.pack(pady=10)

# Create admin tab
admin_tab = ttk.Frame(tab_control)
tab_control.add(admin_tab, text='Admin')

admin_frame = ttk.Frame(admin_tab, padding=20)
admin_frame.pack(fill=tk.BOTH, expand=True)

admin_label = ttk.Label(admin_frame, text="Admin Login", font=("Helvetica", 20, "bold"))
admin_label.pack(pady=20)

admin_id_label = ttk.Label(admin_frame, text="Admin ID:")
admin_id_label.pack(pady=(0, 5))
admin_id_entry = ttk.Entry(admin_frame)
admin_id_entry.pack(pady=(0, 20), ipadx=10, ipady=5)

admin_password_label = ttk.Label(admin_frame, text="Password:")
admin_password_label.pack(pady=(0, 5))
admin_password_entry = ttk.Entry(admin_frame, show="*")
admin_password_entry.pack(pady=(0, 20), ipadx=10, ipady=5)

admin_login_button = ttk.Button(admin_frame, text="Login", command=admin_login)
admin_login_button.pack()

root.mainloop()
