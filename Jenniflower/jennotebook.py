import tkinter as tk
import math
import os
from tkinter import ttk
class JeNotebook:
    def __init__(self, root):
        self.root = root
        self.root.title("Jen's Notebook")
        self.root.attributes('-topmost', True)
        self.root.geometry(f'300x500+0+0')
        try:
            if os.path.exists(r"G:\My Drive\jen_notes.txt"):
                path = r"G:\My Drive\jen_notes.txt"
            elif os.path.exists(r"jen_notes.txt"):
                path = r"jen_notes.txt"
        except Exception as e:
            print(f"An error occurred: {e}")
            
        self.save_file = path

        # Create the Text widget
        self.text = tk.Text(
            root,
            width=300,
            height=500,
            bg="#fd6f95",
            fg="white",
            selectbackground="#ff0055",
            insertbackground="white",
            font=("Modern No. 20", 15),
            cursor="pencil"
        )
        self.text.pack(expand=True, fill="both")

        # Load previously saved text
        self.load_notes()

        # Save notes when the window is closed
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def load_notes(self):
        """Load notes from file if available."""
        if os.path.exists(self.save_file):
            with open(self.save_file, "r", encoding="utf-8") as file:
                content = file.read()
                self.text.insert("1.0", content)

    def on_close(self):
        """Save notes to file before closing."""
        with open(self.save_file, "w", encoding="utf-8") as file:
            file.write(self.text.get("1.0", tk.END).strip())
        self.root.destroy()
root_note = tk.Tk()
note_app = JeNotebook(root_note)
root_note.mainloop()