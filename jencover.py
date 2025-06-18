import tkinter as tk
class Cover:
    def __init__(self, root):
        import tkinter as tk
        self.root = root
        self.root.overrideredirect(True)
        self.root.geometry('400x300')
        self.border_width = 5
        self.root.bind("<Button-3>", lambda e: self.root.destroy())
        self.root.attributes('-topmost', True)


        # Variables for move/resize
        self.is_resizing = False
        self.is_moving = False
        self.resize_dir = None
        self.start_x = self.start_y = 0
        self.start_w = self.start_h = 0

        # Background frame to show the area
        self.canvas = tk.Canvas(root, bg="#fd6f95",width=0,highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Bind events
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.canvas.bind("<Motion>", self.on_hover)
        self.canvas.bind("<Button-3>", lambda: self.root.destroy())
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        w=int(screen_width/screen_height *50)
        h=int(screen_height/screen_width *50)
        for i in range(w):
            for j in range(h):
                sizew=screen_width/w
                sizeh=screen_height/h
                dot = self.canvas.create_oval(i*sizew,j*sizew,i*sizew+sizew,j*sizew+sizew, fill="#ffe5ee",width=1, outline= "#fd6f95", tags=("dot"))
                
                
        self.canvas.tag_bind("dot","<Enter>", self.polka)
        self.root.focus_set()
        self.root.bind("<BackSpace>", self.depolka)
        
    def polka(self,event):
        self.canvas.itemconfig("current", fill="#fd6f95")
    def depolka(self,event):
        for dot in self.canvas.find_withtag("dot"):
            self.canvas.itemconfig(dot, fill="#ffe5ee")
    def on_hover(self, event):
        x, y = event.x, event.y
        w, h = self.root.winfo_width(), self.root.winfo_height()

        # Determine resize direction
        if x >= w - self.border_width and y >= h - self.border_width:
            self.canvas.config(cursor="bottom_right_corner")
            self.resize_dir = "bottomright"
        elif x >= w - self.border_width:
            self.canvas.config(cursor="right_side")
            self.resize_dir = "right"
        elif y >= h - self.border_width:
            self.canvas.config(cursor="bottom_side")
            self.resize_dir = "bottom"
        else:
            self.canvas.config(cursor="arrow")
            self.resize_dir = None

    def on_click(self, event):
        self.start_x = event.x_root
        self.start_y = event.y_root
        self.start_w = self.root.winfo_width()
        self.start_h = self.root.winfo_height()

        if self.resize_dir:
            self.is_resizing = True
        else:
            self.is_moving = True

    def on_drag(self, event):
        dx = event.x_root - self.start_x
        dy = event.y_root - self.start_y

        if self.is_resizing:
            new_w, new_h = self.start_w, self.start_h
            new_x = self.root.winfo_x()
            new_y = self.root.winfo_y()

            if self.resize_dir == "right":
                new_w += dx
            elif self.resize_dir == "bottom":
                new_h += dy
            elif self.resize_dir == "bottomright":
                new_w += dx
                new_h += dy

            if new_w >= 100 and new_h >= 100:
                self.root.geometry(f"{int(new_w)}x{int(new_h)}+{int(new_x)}+{int(new_y)}")

        elif self.is_moving:
            x = self.root.winfo_x() + dx
            y = self.root.winfo_y() + dy
            self.root.geometry(f"+{x}+{y}")
            self.start_x = event.x_root
            self.start_y = event.y_root

    def on_release(self, event):
        self.is_resizing = False
        self.is_moving = False
        self.resize_dir = None
root_cover = tk.Tk()
cover_app = Cover(root_cover)
root_cover.mainloop()
