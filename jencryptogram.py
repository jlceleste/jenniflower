import tkinter as tk
import math
import os
from tkinter import ttk
class Jen_Cryptogram:
    def __init__(self, root):
        import tkinter as tk
        import random
        self.root = root
        self.root.title("Jen's Cryptograms")
        self.root.attributes('-topmost', True)
        self.root.configure(bg='#ffe5ee') 
        self.root.overrideredirect(True)
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        self.root.maxsize(screen_width, screen_height)
        self.root.bind("<Button-3>", lambda e: self.root.destroy())
        file = r"quotes.txt"
        with open(file, 'r') as file:
            file_string = file.read()
        quotes_list = file_string.split("\n")
        r = random.randint(0,99)
        
        quote_with_author = quotes_list[r]
        quote = quote_with_author.split("~")[0]
        author = quote_with_author.split("~")[1]
        print(quote)
        self.text = quote.casefold()
        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        shuffled_alphabet = list(alphabet)
        random.shuffle(shuffled_alphabet)
        key = dict(zip(alphabet, shuffled_alphabet))
        encrypted_message = ''
        for char in self.text:
            if char in key:
                encrypted_message += key[char]
            else:
                encrypted_message += char # Keep non-alphabetic characters
        textl = encrypted_message.split(" ")
        self.entries = []  # Store all Entry widgets in order
        max_width = screen_width -50 # margin for safety
        x_offset = 0
        row = 0
        col = 0
        self.answer =""
        for char in self.text.replace(" ",""):
            if char.isalpha():
                self.answer += char

        for word in textl:
            # Estimate word width in pixels (roughly 30px per character + spacing)
            est_word_width = len(word) * 30 + 20

            if x_offset + est_word_width > max_width:
                row += 1
                col = 0
                x_offset = 0

            frame = tk.Frame(root, bg='#ffe5ee')
            frame.grid(row=row, column=col, padx=5, pady=5)
            x_offset += est_word_width
            col += 1
            


            for i, char in enumerate(word):
                if char.isalpha():
                    entry = tk.Entry(frame, width=1, bg="#ff0055", justify="center", fg = "white", bd=6, font =("Modern No. 20",14), insertbackground ="white")
                    entry.grid(row=0, column=i)
                    
                    label = tk.Label(frame, text=char, bg ="#ffe5ee", fg="#ff0055", font = ("Modern No. 20",15, "bold"))
                    label.grid(row=1, column=i)

                    entry.bind("<Right>", self.right)
                    entry.bind("<Left>", self.left)
                    entry.bind("<KeyRelease>", self.typed)
                    entry.bind("<BackSpace>", self.back)
                    entry.bind("<Key-space>", lambda e: "break")
                    entry.bind("<Return>", self.check)
                    vcmd = (self.root.register(self.validate_char), '%P')
                    entry.config(validate='key', validatecommand=vcmd)
                    
                    self.entries.append(entry)
                else:
                    p = tk.Label(frame, text=char, bg ="#ffe5ee", fg="#ff0055", font = ("Modern No. 20",15, "bold"))
                    p.grid(row=0, column=i)

        if self.entries:
            self.entries[0].focus_set()

    def right(self, event):
        current = event.widget
        idx = self.entries.index(current)
        if idx + 1 < len(self.entries):
                self.entries[idx + 1].focus_set()
    def left(self, event):
        current = event.widget
        idx = self.entries.index(current)
        if idx - 1 >= 0:
            self.entries[idx - 1].focus_set()
    def typed(self, event):
        if event.keysym not in ("BackSpace", "Left", "Right", "Up", "Down","space"):
            current = event.widget
            idx = self.entries.index(current)

            # Get the typed character (trimmed to 1 char)
            typed_char = current.get()[:1]
            current.delete(0, tk.END)
            current.insert(0, typed_char)
            y= False
            for ent in self.entries:
                if typed_char == ent.get() and ent != current:
                    ent.configure(bg = "red")
                    y = True
            if y:
                current.configure(bg="red")

            # Find the target encrypted character at this index
            target_encrypted = self.answer[idx]

            # Replace matching encrypted letters with typed_char
            for i, label_entry in enumerate(self.entries):
                # Only update matching positions
                if self.answer[i] == target_encrypted:
                    label_entry.delete(0, tk.END)
                    label_entry.insert(0, typed_char)
                    if y:
                        label_entry.configure(bg="red")

            # Move to next Entry if exists
                while (idx + 1) < len(self.entries) and len(self.entries[idx + 1].get())>0:
                    self.entries[idx + 1].focus_set()
                    idx+=1
                if (idx + 1) < len(self.entries):
                    self.entries[idx + 1].focus_set()
                
    def back(self, event):
        current = event.widget
        idx = self.entries.index(current)
        # Get the typed character (trimmed to 1 char)
        typed_char = current.get()[:1]
        current.delete(0, tk.END)
        current.insert(0, typed_char)
        
        # Find the target encrypted character at this index
        target_encrypted = self.answer[idx]
        if len(current.get()) == 0:
            self.entries[idx - 1].focus_set()
        # Replace matching encrypted letters with typed_char
        for i, label_entry in enumerate(self.entries):
            # Only update matching positions
            if self.answer[i] == target_encrypted:
                label_entry.delete(0, tk.END)
                label_entry.configure(bg = "#ff0055")
            if label_entry.get()==typed_char:
                label_entry.configure(bg = "#ff0055")
                    
                    
    def validate_char(self, P):
        return len(P) <= 1
    def check(self,event):
        win = tk.Toplevel(self.root)
        win.title("Jen's Cryptograms")
        win.geometry("300x100+300+300")
        win.configure(bg='#fd6f95')
        answer=self.answer
        my_answer= ""
        for ent in self.entries:
            my_answer += ent.get()
        if my_answer==answer:
            b = tk.Label(win, text="you are so smart and cool", font=("Modern No. 20", 15), fg="white", bg="#fd6f95")
            b.pack()
        else:
            b = tk.Label(win, text="WRONG :(", font=("Modern No. 20", 15), fg="white", bg="#fd6f95")
            b.pack()
            d = tk.Button(win, text="try again", font=("Modern No. 20", 15), fg="white", command = lambda: win.destroy(), bg="#ff0055")
            d.pack()
        c = tk.Button(win, text="exit", font=("Modern No. 20", 15), fg="white", command = lambda: self.root.destroy(), bg="#ff0055")
        c.pack()
        print(my_answer)
        print(answer)
        
root_crypt = tk.Tk()
crypt_app = Jen_Cryptogram(root_crypt)
root_crypt.mainloop()