import tkinter as tk
import math
import os
from tkinter import ttk
import subprocess
class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Jen's Calculator")
        self.inv_mode = tk.BooleanVar()
        self.use_degrees = tk.BooleanVar(value=False)
        window_width = 350
        window_height = 500
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - window_width)
        y = 0
        
        
        # Configure root grid
        for c in range(4):
            self.root.columnconfigure(c, weight=1)
        for r in range(6):
            self.root.rowconfigure(r, weight=1)

        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.attributes('-topmost', True)
        fon = "Arial"
        # Top container (for entry and output)
        self.container = tk.Frame(root)
        self.container.grid(row=0, column=0, columnspan=4, sticky="nsew")
        self.container.columnconfigure(0, weight=1)
        self.container.columnconfigure(1, weight=2)
        self.container.rowconfigure(0, weight=1)

        # Entry and output label
        self.entr = tk.Entry(self.container,bg="#ffe5ee",fg="#ff0055", font=(fon,15))
        self.entr.grid(row=0, column=0, sticky="nsew")
        self.out = tk.Button(self.container, text="",command=lambda: self.reset(),fg="#ffe5ee",bg="#ff0055", font=(fon,15))
        self.out.grid(row=0, column=1, sticky="nsew")
        self.entr.icursor(0)
        fon = "French Script MT"
        style_kwargs = {"bd": 2 , "bg": "#fd6f95", "fg": "white"}
        style_kwargn = {"bd": 10, "bg": "#ff0055", "fg": "white"}

        # Numeric buttons
        self.a1 = tk.Button(root, text="1", command=lambda: self.write("1"), **style_kwargn, font=(fon,35))
        self.a1.grid(row=2, column=0, sticky="nsew")
        self.a2 = tk.Button(root, text="2", command=lambda: self.write("2"), **style_kwargn, font=(fon,35))
        self.a2.grid(row=2, column=1, sticky="nsew")
        self.a3 = tk.Button(root, text="3", command=lambda: self.write("3"), **style_kwargn, font=(fon,35))
        self.a3.grid(row=2, column=2, sticky="nsew")
        self.a4 = tk.Button(root, text="4", command=lambda: self.write("4"), **style_kwargn, font=(fon,35))
        self.a4.grid(row=3, column=0, sticky="nsew")
        self.a5 = tk.Button(root, text="5", command=lambda: self.write("5"), **style_kwargn, font=(fon,35))
        self.a5.grid(row=3, column=1, sticky="nsew")
        self.a6 = tk.Button(root, text="6", command=lambda: self.write("6"), **style_kwargn, font=(fon,35))
        self.a6.grid(row=3, column=2, sticky="nsew")
        self.a7 = tk.Button(root, text="7", command=lambda: self.write("7"), **style_kwargn, font=(fon,35))
        self.a7.grid(row=4, column=0, sticky="nsew")
        self.a8 = tk.Button(root, text="8", command=lambda: self.write("8"), **style_kwargn, font=(fon,35))
        self.a8.grid(row=4, column=1, sticky="nsew")
        self.a9 = tk.Button(root, text="9", command=lambda: self.write("9"), **style_kwargn, font=(fon,35))
        self.a9.grid(row=4, column=2, sticky="nsew")
        self.a0 = tk.Button(root, text="0", command=lambda: self.write("0"), **style_kwargn, font=(fon,35))
        self.a0.grid(row=5, column=1, sticky="nsew")
        self.adot = tk.Button(root, text=".", command=lambda: self.write("."), **style_kwargn, font=(fon,35))
        self.adot.grid(row=5, column=0, sticky="nsew")

        # Solve button
        self.eqclr_frame = tk.Frame(root)
        self.eqclr_frame.grid(row=5, column=3, sticky="nsew")
        self.eqclr_frame.columnconfigure(0, weight=1)
        self.eqclr_frame.columnconfigure(1, weight=1)
        self.eqclr_frame.rowconfigure(0, weight=1)
        # Equals button (=)
        self.aent = tk.Button(self.eqclr_frame, text="=", command=self.enter, **style_kwargs, font=(fon, 20))
        self.aent.grid(row=0, column=0, sticky="nsew")

        # Clear button (C)
        self.aclr = tk.Button(self.eqclr_frame, text="C", command=self.clear_entry, **style_kwargs, font=(fon, 20))
        self.aclr.grid(row=0, column=1, sticky="nsew")
        self.root.bind("<Return>", self.enter)

        # Operator frame
        self.add = tk.Frame(root)
        self.add.grid(row=2, column=3, sticky="nsew")
        self.add.columnconfigure(0, weight=1)
        self.add.columnconfigure(1, weight=1)
        self.add.rowconfigure(0, weight=1)
        self.add.rowconfigure(1, weight=1)
        self.aplus = tk.Button(self.add, text="+", command=lambda: self.write("+"), **style_kwargs, font=(fon,12))
        self.aplus.grid(row=0, column=0, sticky="nsew")
        self.aminus = tk.Button(self.add, text="-", command=lambda: self.write("-"), **style_kwargs, font=(fon,12))
        self.aminus.grid(row=1, column=0, sticky="nsew")
        self.atimes = tk.Button(self.add, text="*", command=lambda: self.write("*"), **style_kwargs, font=(fon,12))
        self.atimes.grid(row=0, column=1, sticky="nsew")
        self.adivide = tk.Button(self.add, text="/", command=lambda: self.write("/"), **style_kwargs, font=(fon,12))
        self.adivide.grid(row=1, column=1, sticky="nsew")

        # Negate and exponent buttons
        self.ane = tk.Button(root, text="-", command=lambda: self.write("-"), **style_kwargn, font=(fon,35))
        self.ane.grid(row=5, column=2, sticky="nsew")
        self.anexp = tk.Button(root, text="^", command=lambda: self.write("**"), **style_kwargs, font=(fon,15))
        self.anexp.grid(row=1, column=1, sticky="nsew")

        # Parentheses frame
        self.paren = tk.Frame(root)
        self.paren.grid(row=1, column=0, sticky="nsew")
        self.paren.columnconfigure(0, weight=1)
        self.paren.columnconfigure(1, weight=1)
        self.paren.rowconfigure(0, weight=1)
        self.arpar = tk.Button(self.paren, text="(", command=lambda: self.write("("), **style_kwargs, font=(fon,15))
        self.arpar.grid(row=0, column=0, sticky="nsew")
        self.alpar = tk.Button(self.paren, text=")", command=lambda: self.write(")"), **style_kwargs, font=(fon,15))
        self.alpar.grid(row=0, column=1, sticky="nsew")

        # Backspace button
        self.bksp = tk.Button(root, text="⌫", command=self.backspace, **style_kwargs, font=(fon,15))
        self.bksp.grid(row=1, column=3, sticky="nsew")

        # Trig buttons & Inv switch
        self.trig = tk.Frame(root)
        self.trig.grid(row=3, column=3, sticky="nsew")
        self.trig.rowconfigure(0, weight=5)
        #self.trig.rowconfigure(1, weight=1)
        for i in range(3):
            self.trig.columnconfigure(i, weight=1)
        

        # BooleanVar to track inverse mode

        # Trig buttons (initially in normal mode)
        self.sin = tk.Button(self.trig, text="sin", command=self.write_sin, **style_kwargs, font=(fon,12))
        self.sin.grid(row=0, column=0, sticky="nsew")
        self.cos = tk.Button(self.trig, text="cos", command=self.write_cos, **style_kwargs, font=(fon,12))
        self.cos.grid(row=0, column=1, sticky="nsew")
        self.tan = tk.Button(self.trig, text="tan", command=self.write_tan, **style_kwargs, font=(fon,12))
        self.tan.grid(row=0, column=2, sticky="nsew")

        # Checkbutton acts as the "Inv" switch (keep default style)
        self.inv_switch = tk.Button(
            self.trig,
            text="Inv",
            command=self.toggle_inv_mode,
            font=(fon, 12),
            bg="#fd6f95",
            fg="white",
            bd=4,
            relief="raised",
            activebackground="#ff0055"
        )
        self.inv_switch.grid(row=1, column=0, columnspan=3, sticky="nsew")
        self.deg_switch = tk.Button(
            self.trig,
            text="Deg",
            command=self.toggle_deg_mode,
            font=(fon, 12),
            bg="#fd6f95",
            fg="white",
            bd=4,
            relief="raised",
            activebackground="#ff0055"
        )
        self.deg_switch.grid(row=2, column=0, columnspan=3, sticky="nsew")
        self.root.update()
        # Constants frame (π and e)
        self.consts = tk.Frame(root)
        self.consts.grid(row=4, column=3, sticky="nsew")
        self.consts.columnconfigure(0, weight=1)
        self.consts.columnconfigure(1, weight=1)
        self.consts.rowconfigure(0, weight=1)
        self.consts.rowconfigure(1, weight=1)

        self.pi_btn = tk.Button(
            self.consts,
            text="π",
            command=lambda: self.write("math.pi"),
            **style_kwargs,
            font=(fon,15)
        )
        self.pi_btn.grid(row=0, column=0, sticky="nsew")

        self.e_btn = tk.Button(
            self.consts,
            text="e",
            command=lambda: self.write("math.e"),
            **style_kwargs,
            font=(fon,25)
        )
        self.e_btn.grid(row=0, column=1, sticky="nsew")
        self.log_btn = tk.Button(
            self.consts,
            text="log",
            command=lambda: self.write("math.log(n,b)"),
            **style_kwargs,
            font=(fon,15)
        )
        self.log_btn.grid(row=1, column=0, sticky="nsew")
        self.ln_btn = tk.Button(
            self.consts,
            text="ln",
            command=lambda: self.write("math.log("),
            **style_kwargs,
            font=(fon,15)
        )
        self.ln_btn.grid(row=1, column=1, sticky="nsew")
        # Conversion button (opens new window)
        self.conv_btn = tk.Button(root, text="Con.", command=self.open_conversion_window, **style_kwargs, font=(fon,10))
        self.conv_btn.grid(row=1, column=2, sticky="nsew")
    def reset(self):
        self.clear_entry()
        self.write(self.out.cget("text"))
    def clear_entry(self):
        self.entr.delete(0, tk.END)
    def toggle_deg_mode(self):
        current = self.use_degrees.get()
        self.use_degrees.set(not current)
        # Optional: Visual cue for active state
        if self.use_degrees.get():
            self.deg_switch.config(bg="#ff0055")
        else:
            self.deg_switch.config(bg="#fd6f95")
    def toggle_inv_mode(self):
        current = self.inv_mode.get()
        self.inv_mode.set(not current)
        self.update_trig_buttons()
    def write_sin(self):
        print("Inv mode:", self.inv_mode.get())
        if self.inv_mode.get():
            self.write("math.asin(")
        else:
            self.write("math.sin(")
        if self.use_degrees.get():
            self.write("math.radians(")

    def write_cos(self):
        if self.inv_mode.get():
            self.write("math.acos(")
        else:
            self.write("math.cos(")
        if self.use_degrees.get():
            self.write("math.radians(")

    def write_tan(self):
        if self.inv_mode.get():
            self.write("math.atan(")
        else:
            self.write("math.tan(")
        if self.use_degrees.get():
            self.write("math.radians(")
    def update_trig_buttons(self):
        """Update labels based on inverse toggle."""
        print("Toggle state is:", self.inv_mode.get())
        if self.inv_mode.get():
            self.sin.config(text="arcsin")
            self.cos.config(text="arccos")
            self.tan.config(text="arctan")
        else:
            self.sin.config(text="sin")
            self.cos.config(text="cos")
            self.tan.config(text="tan")

    def open_conversion_window(self):
        """Open a new window to convert the current output into other units."""
        try:
            current_val = float(self.out.cget("text"))
        except ValueError:
            current_val = None

        conv_win = tk.Toplevel(self.root)
        conv_win.title("Unit Conversion")
        conv_win.geometry("350x350")
        for i in range(3):
            conv_win.rowconfigure(i, weight=1)
        conv_win.columnconfigure(0, weight=1)
        conv_win.columnconfigure(1, weight=1)

        # Display current value
        tk.Label(conv_win, text="Value:").grid(row=0, column=0, sticky="e", padx=5)
        self.val_entry = tk.Entry(conv_win)
        self.val_entry.grid(row=0, column=1, sticky="w", padx=5)
        if current_val is not None:
            self.val_entry.insert(0, str(current_val))

        # Conversion factor (or ratio)
        tk.Label(conv_win, text="Factor:").grid(row=1, column=0, sticky="e", padx=5)
        self.factor_entry = tk.Entry(conv_win)
        self.factor_entry.grid(row=1, column=1, sticky="w", padx=5)
        self.factor_entry.insert(0, "1.0")

        # Convert button
        conv_action = tk.Button(conv_win, text="Convert", command=lambda: self.perform_conversion(), **style_kwargs, font=(fon,12))
        conv_action.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=10)

        # Result label
        self.result_label = tk.Label(conv_win, text="")
        self.result_label.grid(row=3, column=0, columnspan=2, sticky="nsew")

    def perform_conversion(self):
        """Read the value and factor, compute and display the converted result."""
        try:
            val = float(self.val_entry.get())
            factor = float(self.factor_entry.get())
            converted = val * factor
            self.result_label.config(text=f"{converted}")
        except ValueError:
            self.result_label.config(text="Invalid input")

    def backspace(self):
        # Get the current cursor position
        pos = self.entr.index("insert")

        if pos > 0:
            # Delete the character just before the cursor
            self.entr.delete(pos - 1)

    def write(self, entry):
        self.entr.insert("insert", entry)

    def enter(self, event=None):
        try:
            value = round(eval(self.entr.get()), 4)
            self.out.config(text=str(value))
        except Exception:
            self.out.config(text="Error")
            
root_calc = tk.Tk()
calc_app = Calculator(root_calc)
root_calc.mainloop()