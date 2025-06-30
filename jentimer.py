import os
from tkinter import ttk
import subprocess

class TimerOverlay:
    def __init__(self, root):
        self.root = root
        self.root.title("Timer")
        self.root.overrideredirect(True)
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        root.wm_attributes("-transparentcolor", "grey")  
        y=screen_height-25
        # Set the window to be borderless and always on top
        self.root.attributes('-topmost', True)
        self.window_width = screen_width  # Default width
        self.window_height = 25  # Default height
        self.root.resizable(True, True)
        self.root.geometry(f'{self.window_width}x{self.window_height}+0+{y}')
        self.root.configure(bg='#fd6f95')  # Background color (lightest pink)
        self.root.overrideredirect()  # Remove window borders and title bar
        self.root.columnconfigure(2, weight=1)
        self.root.columnconfigure(1, weight=2)
        self.root.columnconfigure(3, weight=2)
        self.root.rowconfigure(0, weight=1)
#         self.root.rowconfigure(0, weight=1)
        self.saved_start_time= "08:00"
        self.saved_end_time= "16:00"
        self.saved_input_time= "12:00"
        self.saved_timer_time = "25"
        self.timer_job = None
        # Variables to hold time and settings
        self.remaining = 25 * 60  # Default: 25 minutes in seconds
        self.running = False
        self.timer_duration = self.remaining  # Timer duration in seconds
        self.timer_color = '#ff0055'  # Timer text color

 	# Start Button

        # Label for the timer text
        self.label = tk.Label(root, text=self.format_time(), font=("Modern No. 20", 15), fg="white", bg="#fd6f95")
        self.label.grid(row=0, column=0, sticky = 'w')

        # Canvas for the custom progress bar
        self.canvas = tk.Canvas(root, height = 25, bg="#ffb2c6", bd=2, highlightthickness=0)
        self.canvas.grid(row=0, column=1, columnspan = 3, sticky = 'new')

        # Draw the pink progress bar on the canvas
        self.progress_bar = self.canvas.create_rectangle(4, 4, 4, 21, fill="#ff0055", outline="")

        
        # Settings button to open the settings window
        self.settings_button = tk.Button(root, text="Set", command=self.open_settings, font=("Modern No. 20", 10), bd=0, bg="#fd6f95", fg = "white")
        self.settings_button.grid(row=0, column=4, sticky ='e')

        # Variables for dragging the window
        self.dragging = False
        self.prev_x = 0
        self.prev_y = 0

        # Bind mouse events to make the window moveable
        self.root.bind("<Button-1>", self.start_drag)
        self.root.bind("<B1-Motion>", self.drag)
        self.collapsed = False
        self.label.bind("<Button-1>", self.toggle_visibility)
    def toggle_visibility(self, event=None):
        self.collapsed = not self.collapsed

        if self.collapsed:
            # Dim the progress bar by setting it to grey
            self.canvas.itemconfig(self.progress_bar, fill="grey")
            self.canvas.config(bg="grey")
            self.settings_button.grid_remove()
        else:
            # Restore original colors
            self.canvas.itemconfig(self.progress_bar, fill="#ff0055")
            self.label.config(fg="white")
            self.canvas.config(bg="#ffb2c6")
            self.canvas.grid()
            self.settings_button.grid()
    
    def format_time(self):
        """Converts time from seconds to a MM:SS format."""
        mins, secs = divmod(self.remaining, 60)
        return f"{mins:02}:{secs:02}"

    def update_timer(self):
        """Updates the timer every second."""
        self.root.attributes('-topmost', True)
        if self.running and self.remaining > 0:
            self.remaining -= 1
            self.label.config(text=self.format_time())  # Update time text

            # Update progress bar width
            progress_width = (self.timer_duration - self.remaining) / self.timer_duration * (self.window_width - 40)
            self.canvas.coords(self.progress_bar, 4, 4, progress_width+4, 21)

            # ✅ Schedule the next update (only once)
            self.timer_job = self.root.after(1000, self.update_timer)
        elif self.remaining == 0:
            self.label.config(text="Time's up!")
            self.canvas.coords(self.progress_bar, 4, 4, self.window_width - 40, 21)
            self.running = False  # Optional: Stop the timer

    def start_timer(self):
        """Starts the timer countdown."""
        if not self.running:
            self.running = True

            if self.timer_job:  # Cancel previous job if it exists
                self.root.after_cancel(self.timer_job)
                self.timer_job = None

            self.update_timer()

    def start_drag(self, event):
        """Start dragging the window."""
        self.dragging = True
        self.prev_x = event.x
        self.prev_y = event.y

    def drag(self, event):
        """Drag the window around the screen."""
        if self.dragging:
            dx = event.x - self.prev_x
            dy = event.y - self.prev_y
            x = self.root.winfo_x() + dx
            y = self.root.winfo_y() + dy
            self.root.geometry(f"+{x}+{y}")

    def open_settings(self):
        """Open the settings window to adjust timer settings."""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        #settings_window.geometry('300x500')
        settings_window.configure(bg='#fd6f95')

        #Create style
        style = ttk.Style()
        style.theme_use('default')

        #Configure the Notebook and Tab styles
        style.configure('TNotebook', font=("Modern No. 20", 12), foreground="white", background='#fd6f95', borderwidth=0)
        style.configure('TNotebook.Tab', font=("Modern No. 20", 12), foreground="white", background='#fd6f95', padding=[10, 5])
        style.map('TNotebook.Tab',
                  background=[("selected", "#ffb2c6"), ("active", "#ff0055")],
                  foreground=[("selected", "white"),("active", "white") ])

        # Notebook
        tabControl = ttk.Notebook(settings_window, style='TNotebook')
        tabControl.pack(expand=1, fill="both")

        # Tabs (Frames) with matching pink bg
        tab1 = ttk.Frame(tabControl)
        tab2 = ttk.Frame(tabControl)
        tab3 = ttk.Frame(tabControl)
        tab4 = ttk.Frame(tabControl)

        for tab in (tab1, tab2, tab3, tab4):
            tab.configure(style='TNotebook.Tab')
            tab.pack_propagate(True)  # Prevent internal resizing

            # Insert a background filler frame
            filler = tk.Frame(tab, bg='#fd6f95')
            filler.pack(fill='both', expand=True)

        tabControl.add(tab1, text='From-To')
        tabControl.add(tab2, text='Timer')
        tabControl.add(tab3, text='Alarm')
        tabControl.add(tab4, text='Settings')

        # Place widgets on pink backgrounds using the inner filler frames
        # Timer duration setting
        filler3 = tab3.winfo_children()[0]
        tk.Label(filler3, text="End timer at:", bg="#fd6f95",font=("Modern No. 20", 15), fg="white").pack(pady=5)
        self.input_time = tk.Entry(filler3)
        self.input_time.insert(0, str(self.saved_input_time))
        self.input_time.pack(pady=0)

        filler1 = tab1.winfo_children()[0]
        tk.Label(filler1, text="Start work at:", bg="#fd6f95",font=("Modern No. 20", 15), fg="white").pack(pady=5)
        self.start_time = tk.Entry(filler1)
        self.start_time.insert(0, str(self.saved_start_time))
        self.start_time.pack(pady=0)

        tk.Label(filler1, text="End work at:", bg="#fd6f95",font=("Modern No. 20", 15), fg="white").pack(pady=5)
        self.end_time = tk.Entry(filler1)
        self.end_time.insert(0, str(self.saved_end_time))
        self.end_time.pack(pady=0)

        # Timer size setting
        filler4 = tab4.winfo_children()[0]
        tk.Label(filler4, text="Set Timer Dimensions (width x height):", bg="#fd6f95",font=("Modern No. 20", 15), fg="white").pack(pady=5)
        self.width_entry = tk.Entry(filler4)
        self.width_entry.insert(0, str(self.window_width))
        self.width_entry.pack(pady=0)

        filler2 = tab2.winfo_children()[0]
        
        tk.Label(filler2, text="How long?", bg="#fd6f95",font=("Modern No. 20", 15), fg="white").pack(pady=5)
        self.timer_time = tk.Entry(filler2)
        self.timer_time.insert(0, str(self.saved_timer_time))
        self.timer_time.pack(pady=0)
        
        
        self.height_entry = tk.Entry(filler4)
        self.height_entry.insert(0, str(self.window_height))
        self.height_entry.pack(pady=0)

        # Save Button
        tk.Button(filler1, text="Save", command= lambda: self.save_settings(1), bg="#ff0055",font=("Modern No. 20", 10), fg="white").pack(pady=5)
        tk.Button(filler2, text="Save", command=lambda:self.save_settings(2), bg="#ff0055",font=("Modern No. 20", 10), fg="white").pack(pady=5)
        tk.Button(filler3, text="Save", command=lambda:self.save_settings(3), bg="#ff0055",font=("Modern No. 20", 10), fg="white").pack(pady=5)
        tk.Button(filler4, text="Save", command=lambda:self.save_settings(4), bg="#ff0055",font=("Modern No. 20", 10), fg="white").pack(pady=5)
        tk.Button(filler4, text="Close", command = lambda: self.root.destroy(), bg="#ff0055",font=("Modern No. 20", 10), fg="white").pack(pady=5)
    def calculate_minutes_till_time(self,input_time_str):
        try:
            input_time = datetime.datetime.strptime(input_time_str, "%H:%M").time()
            current_time = datetime.datetime.now().time()
    
            combined_input = datetime.datetime.combine(datetime.date.today(), input_time)
            combined_current = datetime.datetime.combine(datetime.date.today(), current_time)
    
            if combined_input <= combined_current:
                combined_input += datetime.timedelta(days=1)
    
            time_difference = combined_input - combined_current
            minutes_difference = int(time_difference.total_seconds() / 60)
    
            return minutes_difference
        except ValueError:
            print("Invalid time format. Please use HH:MM (24-hour clock).")
            return None
    def calculate_minutes_till_time2(self, end_time, start_time):
        try:
            input_time1 = datetime.datetime.strptime(start_time, "%H:%M").time()
            input_time2 = datetime.datetime.strptime(end_time, "%H:%M").time()
    
            combined_input = datetime.datetime.combine(datetime.date.today(), input_time1)
            combined_current = datetime.datetime.combine(datetime.date.today(), input_time2)
    
            if combined_input <= combined_current:
                combined_input += datetime.timedelta(days=1)
    
            time_difference = combined_input - combined_current
            minutes_difference = int(time_difference.total_seconds() / 60)
    
            #print(minutes_difference)
            return minutes_difference
        except ValueError:
            print("Invalid time format. Please use HH:MM (24-hour clock).")
            return None


    def save_settings(self, which):
        """Save the settings from the settings window."""
        try:
            if self.timer_job:
                self.root.after_cancel(self.timer_job)
                self.timer_job = None

            if which == 1:
                print(self.start_time.get())
                print(self.end_time.get())
                self.saved_start_time = self.start_time.get()
                self.saved_end_time = self.end_time.get()
                time = self.calculate_minutes_till_time2(self.start_time.get(), self.end_time.get())
                self.timer_duration = time * 60
                print(self.timer_duration)
                self.remaining = self.calculate_minutes_till_time(self.end_time.get()) *60
                print(self.remaining)
                self.running = False

            elif which == 2:
                self.saved_timer_time = self.timer_time.get()
                time = int(self.timer_time.get())
                self.timer_duration = time * 60
                self.remaining = self.timer_duration
                self.running = False

            elif which == 3:
                self.saved_input_time = self.input_time.get()
                time = self.calculate_minutes_till_time(self.input_time.get())
                self.timer_duration = time * 60
                self.remaining = self.timer_duration
                self.running = False

            elif which == 4:
                self.window_width = int(self.width_entry.get())
                self.window_height = int(self.height_entry.get())
                self.canvas.config(width=self.window_width - 40)

                screen_height = self.root.winfo_screenheight()
                y = screen_height - self.window_height
                self.root.geometry(f"{self.window_width}x{self.window_height}+0+{y}")

            self.label.config(text=self.format_time())  # update display
            self.start_timer()  # only start one update loop

        except ValueError:
            print("Invalid input for timer duration or dimensions.")
            
root_timer = ttk.Tk()
timer_app = TimerOverlay(root_timer)
root_timer.mainloop()
