import tkinter as tk
import math
import os
from tkinter import ttk
import subprocess


root = tk.Tk()
root.wm_attributes("-transparentcolor", "white")   # if you need a transparent background
root.attributes('-topmost', True)
root.overrideredirect(True)
root.bind("<Button-3>", lambda e: root.destroy())
canvas = tk.Canvas(root, width=200, height=200, bg="white", bd=0, highlightthickness=0)
canvas.pack()


def create_slanted_oval(canvas, x0, y0, x1, y1, angle=30, steps=50, **kwargs):
    a = (x1 - x0) / 2.0
    b = (y1 - y0) / 2.0
    xc = x0 + a
    yc = y0 + b

    points = []
    for i in range(steps):
        theta = 2 * math.pi * i / steps
        x = xc + a * math.cos(theta)
        y = yc + b * math.sin(theta)
        rad = math.radians(angle)
        rx = xc + (x - xc) * math.cos(rad) - (y - yc) * math.sin(rad)
        ry = yc + (x - xc) * math.sin(rad) + (y - yc) * math.cos(rad)
        points.extend((rx, ry))

    return canvas.create_polygon(points, **kwargs)

# Tag every piece of the flower "flower"
tags = ("flower",)

petal1 = create_slanted_oval(canvas, 85, 0,   115,  90,  angle=0,   fill="#ffb2c6", tags = ("flower","1"))
petal2 = create_slanted_oval(canvas, 130, 27, 160, 117, angle=60,  fill="#ffb2c6", tags = ("flower","2"))
petal3 = create_slanted_oval(canvas, 130, 80, 160, 170, angle=120, fill="#ffb2c6", tags = ("flower","3"))
petal4 = create_slanted_oval(canvas, 85, 110, 115, 200,angle=0,   fill="#ffb2c6", tags = ("flower","4"))
petal5 = create_slanted_oval(canvas, 40, 27,  70, 117, angle=120, fill="#ffb2c6", tags = ("flower","5"))
petal6 = create_slanted_oval(canvas, 40, 80,  70, 170, angle=60,  fill="#ffb2c6",tags = ("flower","6"))
center = canvas.create_oval(80, 80, 120, 120, fill='#fd6f95',width=0, tags = ("flower","center"))

petals = [petal1, petal2, petal3, petal4, petal5, petal6]
# We'll store two things when the user presses down:
#   1.  root_window's current screen‐coordinates (root_x, root_y)
#   2.  where on the screen the mouse was pressed (mouse_x, mouse_y)
drag_data = {
    "win_x": 0,      # root.winfo_x() at the moment of ButtonPress
    "win_y": 0,      # root.winfo_y() at the moment of ButtonPress
    "mouse_x": 0,    # event.x_root at press
    "mouse_y": 0,    # event.y_root at press
}

def on_flower_press(event):
    # Remember where the window was, and where the mouse was on the screen
    drag_data["win_x"] = root.winfo_x()
    drag_data["win_y"] = root.winfo_y()
    drag_data["mouse_x"] = event.x_root
    drag_data["mouse_y"] = event.y_root

def on_flower_drag(event):
    # How far has the mouse moved on the screen since button‐down?
    dx = event.x_root - drag_data["mouse_x"]
    dy = event.y_root - drag_data["mouse_y"]

    # New window position = original window position + (dx, dy)
    new_x = drag_data["win_x"] + dx
    new_y = drag_data["win_y"] + dy

    root.geometry(f"+{new_x}+{new_y}")
def on_center_press(event):
    for petal in petals:
        current_color = canvas.itemcget(petal, "fill")
        new_color = "#ffb2c6" if current_color == "white" else "white"
        canvas.itemconfig(petal, fill=new_color)
def timer(event):
    subprocess.Popen(["python", "jentimer.py"])
def calculator(event):
    subprocess.Popen(['python','jencalculator.py'])
def notebook(event):
    subprocess.Popen(['python','jennotebook.py'])
def cover(event):
    subprocess.Popen(["python", "jencover.py"])
def cryptogram(event):
    subprocess.Popen(['python','jencryptogram.py'])
def todo(event):
    subprocess.Popen(["python", "jentodo.py"])

    

# Bind to everything tagged "flower":
canvas.tag_bind("flower", "<ButtonPress-1>", on_flower_press)
canvas.tag_bind("flower", "<B1-Motion>", on_flower_drag)
canvas.tag_bind("center", "<ButtonPress-1>", on_center_press)
canvas.tag_bind("1", "<ButtonPress-1>", timer)
canvas.tag_bind("1", "<Enter>", lambda event: root.config(cursor = "gobbler"))
canvas.tag_bind("1", "<Leave>", lambda event: root.config(cursor = "arrow"))
canvas.tag_bind("2", "<ButtonPress-1>", calculator)
canvas.tag_bind("2", "<Enter>", lambda event: root.config(cursor = "tcross"))
canvas.tag_bind("2", "<Leave>", lambda event: root.config(cursor = "arrow"))
canvas.tag_bind("3", "<ButtonPress-1>", notebook)
canvas.tag_bind("center", "<Enter>", lambda event: root.config(cursor = "heart"))
canvas.tag_bind("center", "<Leave>", lambda event: root.config(cursor = "arrow"))
canvas.tag_bind("3", "<Enter>", lambda event: root.config(cursor = "pencil"))
canvas.tag_bind("3", "<Leave>", lambda event: root.config(cursor = "arrow"))
canvas.tag_bind("4", "<ButtonPress-1>", cover)
canvas.tag_bind("4", "<Enter>", lambda event: root.config(cursor = "box_spiral"))
canvas.tag_bind("4", "<Leave>", lambda event: root.config(cursor = "arrow"))
canvas.tag_bind("5", "<ButtonPress-1>", cryptogram)
canvas.tag_bind("5", "<Enter>", lambda event: root.config(cursor = "gumby"))
canvas.tag_bind("5", "<Leave>", lambda event: root.config(cursor = "arrow"))
canvas.tag_bind("6", "<ButtonPress-1>", todo)
canvas.tag_bind("6", "<Enter>", lambda event: root.config(cursor = "star"))
canvas.tag_bind("6", "<Leave>", lambda event: root.config(cursor = "arrow"))
root.mainloop()

