import tkinter as tk
from tkinter import Label, Frame, OptionMenu, StringVar, Button
from PIL import Image, ImageTk
from tkinter import messagebox
import sqlite3

class OpeningPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Voting System")
        self.row = 0
        self.col = 0
        
        self.window = Frame(self.root)
        self.window.pack(fill=tk.BOTH, expand=True)

        # Load and display the image
        self.image = Image.open("guide.png")
        self.image = self.image.resize((self.image.width // 3, self.image.height // 3))  # Reduce image size
        self.photo = ImageTk.PhotoImage(self.image)
        self.image_label = Label(self.window, image=self.photo)
        self.image_label.pack(pady=(10, 0))  # Add padding at the bottom

        # Header
        header_label = Label(self.window, text="Click the Buttons Below to Vote",
                             font=("Helvetica", 16, "bold"), foreground="#7951AD")
        header_label.pack(pady=(0, 20))  # Add padding at the top

        # Create a frame for the menu options
        self.menu_frame = Frame(self.window)
        self.menu_frame.pack()

        # Initialize the menu options
        self.menu_options = [
            ("Presidential Vote", "#BEE6DC", ["Name 1", "Name 2", "None"]),
            ("Provincial Vote", "#B2B2CF", ["Name A", "Name B", "None"]),
        ]

        # Create labels with colored boxes for each menu option
        self.menu_option_frames = []
        self.refresh_menu_options()

        # Create "Save and Exit" button with background color #FDA85A
        save_button = Button(self.window, text="Save and Exit", command=self.save_and_exit, bg="#FDA85A")
        save_button.pack(pady=(10, 30), side=tk.LEFT)  # Use pack geometry manager

        # Configure row and column weights to center-align the labels
        for i in range(len(self.menu_options)):
            self.menu_frame.rowconfigure(i, weight=1)

    def toggle_dropdown(self, frame):
        # Toggle the visibility of the option menu in the clicked frame
        if frame.option_menu.winfo_ismapped():
            frame.option_menu.pack_forget()
        else:
            frame.option_menu.pack(pady=5)

    def save_and_exit(self):
        # Create a StringVar object
        presidential_var = StringVar()
        provincial_var = StringVar()

        # Set the value of the StringVar objects
        presidential_var.set("Name 1")
        provincial_var.set("Name A")

        # Create the OptionMenu objects
        presidential_option = OptionMenu(self.menu_option_frames[0], presidential_var, *self.menu_options[0][2])
        provincial_option = OptionMenu(self.menu_option_frames[1], provincial_var, *self.menu_options[1][2])

        # Get the value of the StringVar objects
        presidential = presidential_var.get()
        provincial = provincial_var.get()

        # Save the vote to a database
        conn = sqlite3.connect("voting_system7.db")
        cursor = conn.cursor()

        cursor.execute("INSERT INTO votes (presidential, provincial) VALUES (?, ?)",
                    (presidential, provincial))

        conn.commit()
        conn.close()

        # Show a message to inform the user that the vote is saved
        messagebox.showinfo("Vote Saved", "Your vote is saved!")

        # Exit the application
        self.root.quit()

    def refresh_menu_options(self):
        # Remove all existing menu options
        for label_frame in self.menu_option_frames:
            label_frame.destroy()
        self.menu_option_frames = []

        # Recreate the menu options with updated data
        for option, color, options in self.menu_options:
            label_frame = Frame(self.menu_frame, bg=color, highlightbackground="gray", highlightthickness=2)
            label_frame.pack(padx=20, pady=20, side=tk.LEFT)  # Use pack geometry manager
            
            label = Label(label_frame, text=option, font=("Helvetica", 14), bg=color)
            label.pack(padx=10, pady=10)

            selected_option = StringVar(value=options[0])  # Set the default option
            option_menu = OptionMenu(label_frame, selected_option, *options)
            option_menu.pack_forget()  # Hide the menu
            label_frame.option_menu = option_menu  # Store the option menu reference

            label.bind("<Button-1>", lambda e, frame=label_frame: self.toggle_dropdown(frame))

            self.menu_option_frames.append(label_frame)

        # Configure row and column weights to center-align the labels
        for i in range(len(self.menu_options)):
            self.menu_frame.rowconfigure(i, weight=1)


def main():
    root = tk.Tk()
    app = OpeningPage(root)
    root.mainloop()

if __name__ == "__main__":
    main()
