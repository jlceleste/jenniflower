import tkinter as tk
from tkinter import ttk
import csv
from collections import defaultdict
import os

class Jen_todo:
    def check_path(self):
        try:
            if os.path.exists(r"todo_lists.csv"):
                path = r"todo_lists.csv"
                return path
            
        except Exception as e:
            print(f"An error occurred: {e}")
    def delete_task(self, task, widgets):
        if task in self.tasks:
            self.tasks.remove(task)
        for w in widgets:
            w.destroy()
        task.update_csv()
    def add_new_task(self, list_name, frame):
            new_task = Jen_todo.Task(
                parent=self,
                list_name=list_name,
                task="",
                done=False,
                estimated_time="",
                notes="",
                priority="Medium",
                due=""
            )
            self.tasks.append(new_task)

            # Remove the button temporarily
            frame.add_button.grid_forget()

            # Add the task row before the button
            row = frame.grid_size()[1]
            self.make_task_widgets(new_task, frame, row)

            # Re-add the button at the new bottom
            frame.add_button.grid(row=row+1, column=0, columnspan=6, pady=10, sticky="news")

            new_task.update_csv()
    class Task:
        def __init__(self, parent, list_name, task, done, estimated_time, notes, priority, due):
            self.parent = parent
            self.file_path = parent.file_path 
            self.list_name = list_name
            self.task = task
            self.done = done
            self.estimated_time = estimated_time
            self.notes = notes
            self.due = due
            self.priority = priority

        def change_list(self, new_list_name):
            self.list_name = new_list_name
            self.update_csv()

        def change_name(self, new_name):
            self.task = new_name
            self.update_csv()

        def change_done(self):
            self.done = not self.done
            self.update_csv()

        def change_time(self, time):
            self.estimated_time = time
            self.update_csv()

        def change_notes(self, note):
            self.notes = note
            self.update_csv()

        def change_due(self, due):
            self.due = due
            self.update_csv()

        def change_priority(self, p):
            self.priority = p
            self.update_csv()
        def add_new_task(self, list_name, frame):
            new_task = Jen_todo.Task(
                parent=self,
                list_name=list_name,
                task="",
                done=False,
                estimated_time="",
                notes="",
                priority="Medium",
                due=""
            )
            self.tasks.append(new_task)
            row = frame.grid_size()[1]  # Get the next available row
            self.make_task_widgets(new_task, frame, row)
            new_task.update_csv()

        def update_csv(self):
            priority_order = {"High": 0, "Medium": 1, "Low": 2}
            
            # Convert task objects to dictionaries
            task_dicts = [{
                "list_name": t.list_name,
                "task": t.task,
                "completed": str(t.done),
                "estimated_time": t.estimated_time,
                "notes": t.notes,
                "priority": t.priority,
                "due_date": t.due
            } for t in self.parent.tasks]

            # Sort the dictionaries
            sorted_tasks = sorted(
                task_dicts,
                key=lambda row: (row["completed"] == "True", priority_order.get(row["priority"], 3))
            )

            # Write sorted tasks to CSV
            
            with open(self.file_path, "w", newline="") as csvfile:
                fieldnames = ["list_name", "task", "completed", "estimated_time", "notes", "priority", "due_date"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(sorted_tasks)

    def __init__(self, root):
        self.root = root
        self.root.title("Jen's To-Do List")
        self.root.configure(bg='#fd6f95')
        self.root.attributes('-topmost', True)
        self.file_path=self.check_path()
        self.tasks = []
        try:
            with open(self.file_path, newline="") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    task = Jen_todo.Task(
                        parent=self,
                        list_name=row.get("list_name", ""),
                        task=row.get("task", ""),
                        done=row.get("completed", "False") == "True",
                        estimated_time=row.get("estimated_time", ""),
                        notes=row.get("notes", ""),
                        priority=row.get("priority", ""),
                        due=row.get("due_date", "")
                    )
                    self.tasks.append(task)
        except FileNotFoundError:
            print("todo_lists.csv not found.")

        grouped_tasks = defaultdict(list)
        for task in self.tasks:
            grouped_tasks[task.list_name].append(task)

        self.style = ttk.Style()
        self.style.theme_use('default')
        self.style.configure('TNotebook', background='#fd6f95', borderwidth=0)
        self.style.configure('TNotebook.Tab', font=("Modern No. 20", 12), foreground="white", background='#fd6f95', padding=[10, 5])
        self.style.map('TNotebook.Tab',
                       background=[("selected", "#ffb2c6"), ("active", "#ff0055")],
                       foreground=[("selected", "white"), ("active", "white")])

        self.notebook = ttk.Notebook(root, style='TNotebook')
        self.notebook.pack(expand=1, fill="both")
        
        for list_name, tasks_in_list in grouped_tasks.items():
            frame = tk.Frame(self.notebook, bg="#ffb2c6")
            self.notebook.add(frame, text=list_name)
            frame.columnconfigure(2, weight=1)
            frame.columnconfigure(1, weight=0)
            frame.columnconfigure(5, weight=1)

            for i, task in enumerate(tasks_in_list):
                self.make_task_widgets(task, frame, i)

            # Add "Create New Entry" button below last task
            new_row = len(tasks_in_list)
            # Store add_button so we can move it later
            add_button = tk.Button(
                frame,
                text="➕ Create New Entry",
                bg="#fd6f95",
                fg="white",
                font=("Modern No. 20", 10, "bold"),
                relief="raised",
                bd=3
            )
            add_button.grid(row=new_row, column=0, columnspan=6, pady=10, sticky="news")

            # Save reference in a dict so it can be reused when adding tasks
            frame.add_button = add_button
            add_button.config(command=lambda ln=list_name, fr=frame: self.add_new_task(ln, fr))

    def make_task_widgets(self, t, frame, i):
        priority_options = ["High", "Medium", "Low"]
        name_var = tk.StringVar(value=t.task)
        est_var = tk.StringVar(value=t.estimated_time)
        note_var = tk.StringVar(value=t.notes)
        due_var = tk.StringVar(value=t.due)
        prio_var = tk.StringVar(value=t.priority)
        widgets = []

        b = tk.Button(frame,
                      text=f"{'☑' if t.done else '☐'}",
                      bg=f"{'#ff0055' if t.done else '#ffb2c6'}",
                      anchor="w",
                      fg="white",
                      bd=5,
                      font=("Modern No. 20", 10),
                      command=lambda: [t.change_done(), b.config(bg=f"{'#ff0055' if t.done else '#ffb2c6'}", text=f"{'☑' if t.done else '☐'}")]
                      )
        b.grid(row=i, column=0, sticky="news")
        widgets.append(b)

        entries = [
            (name_var, t.change_name, 2),
            (est_var, t.change_time, 4),
            (note_var, t.change_notes, 5),
            (due_var, t.change_due, 3)
        ]
        for var, callback, col in entries:
            e = tk.Entry(frame,
                         textvariable=var,
                         bg="#ffb2c6",
                         fg="white",
                         highlightcolor="#ff0055",
                         highlightthickness=3,
                         highlightbackground="white",
                         justify="center",
                         relief="flat",
                         bd=2,
                         font=("Modern No. 20", 15))
            e.grid(row=i, column=col, sticky="news")
            widgets.append(e)
            e.bind("<Return>", lambda event=None, cb=callback, v=var: cb(v.get()))
            e.bind("<FocusOut>", lambda event=None, cb=callback, v=var: cb(v.get()))
            style = ttk.Style()
            style.theme_use("default")
            style.layout("CustomCombobox.TCombobox",
                        [('Combobox.downarrow', {'side': 'right', 'sticky':'w'}),
                         ('Combobox.padding', {'expand': '0', 'children':
                             [('Combobox.textarea', {'sticky': 'nswe'})]
                         })])
            style.configure("CustomCombobox.TCombobox",
                            fieldbackground="#ffb2c6",
                            background="#ffb2c6",
                            foreground="white",
                            borderwidth=0,
                            relief="flat",
                            padding=0,
                            highlightbackground="red")

            # Map is used to override states like 'readonly'
            style.map("CustomCombobox.TCombobox",
                      foreground=[
                          ("readonly", "white"),
                          ("!disabled", "white"),
                          ("active", "white")
                      ],
                      fieldbackground=[
                          ("readonly", "#ffb2c6"),
                          ("!disabled", "#ffb2c6"),
                          ("active", "#ffb2c6")
                      ],
                      background=[
                          ("readonly", "#ffb2c6"),
                          ("!disabled", "#ffb2c6"),
                          ("active", "#ffb2c6")
                      ])

            g = ttk.Combobox(
                frame,
                textvariable=prio_var,
                values=priority_options,
                state="readonly",
                font=("Modern No. 20", 12),
                justify="center",
                style="CustomCombobox.TCombobox"
            )
            g.grid(row=i, column=1, sticky="news")
            widgets.append(g)
            g.bind("<<ComboboxSelected>>", lambda event=None: t.change_priority(prio_var.get()))
            for w in widgets:
                w.bind("<Button-3>", lambda e, task=t, wlist=widgets: self.delete_task(task, wlist))
            
# Launch app
root = tk.Tk()
app = Jen_todo(root)
root.mainloop()
