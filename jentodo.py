import tkinter as tk
from datetime import date
from PIL import Image, ImageTk
import csv
import os
import ast
import sys
#####
p1="#ff0055"
p2="#fd6f95"
p3="#ffb2c6"
p4="#ffe5ee"
p5="#ffe5ee"
if os.path.exists(r"G:\My Drive\calendar_file.csv"):
    file_path = r"G:\My Drive\calendar_file.csv"
else:
    file_path = r"calendar_file.csv"
today = date.today()
today = today.strftime("%d/%m/%Y")
current_month ="August"
months=[]
i = ""
with open(file_path, 'r',newline="") as csvfile:
    reader = csv.DictReader(csvfile)
    #fieldnames = next(reader)
    for row in reader:
        if row['date'] == today:
            current_month = str((str(row['name']).split(",")[1].split(" ")[1]))
        if str(i) != str(str((str(row['name']).split(",")[1].split(" ")[1]))):
            months.append(str((str(row['name']).split(",")[1].split(" ")[1])))
        i= str((str(row['name']).split(",")[1].split(" ")[1]))
#print(months)
month_idx = months.index(current_month)        
buttons=[]

#####

root = tk.Tk()
root.configure(bg=p3) 
root.wm_attributes("-transparentcolor", "grey")  # Transparent background (Windows only)
root.attributes('-topmost', True)
root.overrideredirect(True)
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root_width = 800
root_height = 500
x = (screen_width // 2) - (root_width // 2)
y = (screen_height // 2) - (root_height // 2)
root.geometry(f"{root_width}x{root_height}+{x+250}+{y}")
root.bind("<Button-3>", lambda e: (root.destroy(), sys.exit("done")))
root.columnconfigure(0, weight =1)
root.columnconfigure(1, weight =1)
root.columnconfigure(2, weight =1)
root.columnconfigure(3, weight =1)
root.columnconfigure(4, weight =1)
root.columnconfigure(5, weight =1)
root.columnconfigure(6, weight =1)
root.rowconfigure(0, weight =1)
root.rowconfigure(1, weight =1)
root.rowconfigure(2, weight =1)
root.rowconfigure(3, weight =1)
root.rowconfigure(4, weight =1)
root.rowconfigure(5, weight =1)
root.rowconfigure(6, weight =1)
original_image = Image.open("rarrow.png")
original_image = original_image.resize((int(211/4), int(76/4)))
rarrow = ImageTk.PhotoImage(original_image)
original_image = Image.open("larrow.png")
original_image = original_image.resize((int(211/4), int(76/4)))
larrow = ImageTk.PhotoImage(original_image)
to = date.today()
to = to.strftime("%d/%B")
to=to.split('/')
def render_month(current_month):
    for button in buttons:
        button.destroy()
    #title.destroy()
    day_nums=[]
    st=0
    with open(file_path, 'r',newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        #fieldnames = next(reader)
        for row in reader:
            if current_month==str((str(row['name']).split(",")[1].split(" ")[1])):
                if str(row['date']).split("/")[1] =="1":
                    start = str(row['name']).split(",")[0]
                    if start == "Monday":
                        st = 0
                    if start == "Tuesday":
                        st = 1
                    if start == "Wednesday":
                        st = 2
                    if start == "Thursday":
                        st = 3
                    if start == "Friday":
                        st = 4
                    if start == "Saturday":
                        st = 5
                    if start == "Sunday":
                        st = 6
                    
                day_nums.append(str(row['date']).split("/")[1])
    #print(day_nums)
    title_canvas = tk.Canvas(root, height=45, width=800/7*5, bg=p2, highlightthickness=0)
    title_canvas.grid(row=0,column=1,columnspan=5, sticky = 'news')
    title = title_canvas.create_text(800/7*5/2,30,text=current_month,font=("Modern No. 20", 35), fill='white')
    #underline = title_canvas.create_image(800/7*5/2,60,image=line,anchor='s')
    #line = title_canvas.create_line(150,50,800/7*5-150,50, fill='white', width=5, arrow="both",arrowshape=(20,0,7),capstyle='round')
    #title = tk.Label(root, text = current_month, bg= p3, font=("Modern No. 20", 20,'underline'), fg="white")
    #title.grid(row =0, column = 1, columnspan=5, sticky = "news",ipadx=0,ipady=0)
    leftb = tk.Button(root, relief="flat",activeforeground=p3, activebackground= p2, image=larrow,bg= p2, font=("default",10,'bold'), fg="white", command= lambda:left())
    leftb.grid(row=0,column=0, sticky='nwes',ipadx=5)
    rightb = tk.Button(root, relief="flat",activeforeground=p3, activebackground= p2,image=rarrow,bg= p2, font=( "default",10,'bold'), fg="white", command= lambda:right())
    rightb.grid(row=0, column=6,sticky='news',ipadx=5)
    days=[]
    
    for i,day in enumerate(("M","T","W","R", "F", "S", "S"),start=0):
        canvas = tk.Canvas(root, height=35, width=800/7, bg=p3,highlightthickness=0)
        canvas.grid(row=1,column=i, sticky='news')
        c=canvas.create_oval(35,5,800/7-35,48, fill=p2, width=0) 
        d = canvas.create_text(800/7/2,28,anchor = 'center',text = day, font=("Modern No. 20", 20), fill="white")
        #d.grid(row=1, column = i)
    place = st
    #print(st)
    for day in day_nums:
        d= tk.Button(root, activeforeground=p3, activebackground= p2, text=day, bd=7, bg=p4, fg=p2, font=("Cambria", 15), anchor='ne', command=lambda d=day, c=current_month:open_day(d,c))
        d.grid(row=2+(int(place/7)), column= place % 7, sticky='news',padx=10,pady=5)
        place=place+1
        buttons.append(d)
render_month(current_month)
def left(event=None):
    global month_idx, hours
    month_idx = (month_idx -1) % len(months)
    current_month = months[month_idx]
    render_month(current_month)
    
def right(event=None):
    global month_idx
    month_idx = (month_idx +1) % len(months)
    current_month = months[month_idx]
    render_month(current_month)
    
def open_day( day, current_month):
    global canvas, hours, name, items, item_dict
    #print(day,current_month)
    try:
        dw.destroy()
    except UnboundLocalError:
        jen="idk"
    #print("open")
    with open(file_path, 'r',newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        #fieldnames = next(reader)
        for row in reader:
            if current_month == str((str(row['name']).split(",")[1].split(" ")[1])) and day == str((str(row['date']).split("/")[1])):
                name = row['name']
                date = row['date']
                items = row['items']
    if len(items) == 0:
        item_dict={}
    else:
        item_dict = ast.literal_eval(items)
    dw=tk.Toplevel(root)
    dw.overrideredirect(True)
    x = (screen_width // 2) - ((root_width+250) // 2)
    y = (screen_height // 2) - (root_height // 2)
    
    root.geometry(f"{root_width}x{root_height}+{x+250}+{y}")
    dw.geometry(f"{250}x{500}+{x}+{y}")
    dw.configure(bg="lightyellow")
    dw.attributes('-topmost', True)
    canvas= tk.Canvas(dw, height =500,width=250,bg=p2)
    canvas.pack()
    li=canvas.create_line(30,52-16,30,500, fill = "white",width=2)
    tit = canvas.create_text(125,6, anchor='n', text = name, font=("Modern No. 20", 17), fill="white")
    hours = {}
    for i in range(16):
        l=canvas.create_line(0,52-16+i*int(464/16),250,52-16+i*int(464/16), fill = "white",width=2)
        t=canvas.create_text(15,52-16+i*int(464/16),anchor = 'n',text=str((5+i)%12+1), font=("Modern No. 20", 20), fill="white")
        hours[str((6+i))+":00"]=52-16+i*int(464/16)
        hours[str((6+i))+":15"]=52-16+i*int(464/16)+ int(464/16/4)
        hours[str((6+i))+":30"]=52-16+i*int(464/16)+ int(464/16/2)
        hours[str((6+i))+":45"]=52-16+i*int(464/16)+ int(464/16/4*3)
    ##print(hours)
    #Item("jen","7:30","8:00","event")
    for key, value in item_dict.items():
        value= value.split(' ')
        i = Item(key,value[0],value[1], value[2])
    dw.bind("<Button-3>", lambda e: add_item())
class Item:
    def __init__(self,name,start,end, which):
        global hours,ty,canvas
        ty = {'class': [p1,p1,'white'],'event':[p3,p3,'white'], 'work':[p2,p4,'white'], 'chore':[p4,p1,p1]}
        ##print(hours.get(start),hours.get(end))
        bd=10
        bd2=4
        try:
            fill=ty.get(which)[0]
            outline=ty.get(which)[1]
            fg=ty.get(which)[2]
        except TypeError:
            fill=p4
            outline=p4
            fg=p2
        self.box = canvas.create_rectangle(30+bd,hours.get(start)+bd2,250-bd,hours.get(end)-bd2-1, fill=fill,width=5, tags = f"click{name}", outline = outline)
        canvas.tag_bind(f"click{name}","<Button-1>", lambda e: self.change_item())
        self.font_size=min(int(hours.get(end)-hours.get(start))-5, 15)
        ##print(font_size)
        self.title =canvas.create_text((30+bd+250-bd)/2,(hours.get(start)+bd2 +hours.get(end)-bd2)/2,anchor = 'center',text=name, font=("Modern No. 20", self.font_size), fill=fg,tags=f"click{name}")
        self.name=name
        self.start=start
        self.end=end
        self.which=which
        self.radio_var = tk.StringVar()
        self.radio_var.set(self.which)
    def change_item(self):
        try:
            change.destroy()
        except UnboundLocalError:
            jen="idk"
        change =tk.Toplevel(root)
        change.configure(bg=p3,highlightthickness=5,highlightcolor='white',highlightbackground='white') 
        change.wm_attributes("-transparentcolor", "grey")  # Transparent background (Windows only)
        change.attributes('-topmost', True)
        change.overrideredirect(True)
        change.geometry(f"{250}x{300}+{x+125}+{y}")
        change.columnconfigure(0,weight=10)
        change.columnconfigure(1,weight=1)
        change.columnconfigure(2,weight=10)
        t = tk.Entry(change, font=("Modern No. 20", 30), justify= 'center',bg=p4,fg=p2,insertbackground=p2)
        st=tk.Entry(change, font=("Modern No. 20", 20), justify= 'center',bg=p4,fg=p2,insertbackground=p2, width=5)
        st.grid(row=1,column=0,padx=0,pady=0)
        st.insert(0,self.start)
        en=tk.Entry(change, font=("Modern No. 20", 20), justify= 'center',bg=p4,fg=p2,insertbackground=p2,width=5)
        en.grid(row=1,column=2,padx=0,pady=0)
        en.insert(0,self.end)
        eq=tk.Label(change, text ="to",font=("Modern No. 20", 20),justify= 'center',bg=p3,fg=p2)
        eq.grid(row=1,column=1,padx=0,pady=0)
        j=0
        for i, (key, value) in enumerate(ty.items()):
            c1=tk.Radiobutton(change, text=key, variable= self.radio_var, font=("Modern No. 20", 15), bg=p3,fg=p2, value=key)
            c1.grid(row=2+i,column=1)
            j=2+i
        #c2=tk.Radiobutton(change, text='Event', variable= self.radio_var, font=("Modern No. 20", 15), bg=p3,fg=p2, value='event')
        #c2.grid(row=3,column=1)
        #print(self.radio_var)
        t.grid(row=0,column=0, columnspan =3, padx=10,pady=10)
        t.insert(0, self.name)
        sb= tk.Button(change, text="save", font=("Modern No. 20", 10), fg = p3, bg=p1, command = lambda: (self.save_item(t.get(),st.get(),en.get(),self.radio_var.get()), change.destroy()))
        sb.grid(row=j+1,column=1,pady=5)
    def save_item(self, name,start,end, which):
        global ty
        canvas.delete(self.box)
        canvas.delete(self.title)
        if len(name) ==0:
            update_dict(self.name,d=True)
        else:
            self.name = name
            self.start= start
            self.end=end
            self.which=which
            bd=10
            bd2=4
            try:
                fill=ty.get(which)[0]
                outline=ty.get(which)[1]
                fg=ty.get(which)[2]
            except TypeError:
                fill=p4
                outline=p4
                fg=p2
            self.box = canvas.create_rectangle(30+bd,hours.get(start)+bd2,250-bd,hours.get(end)-bd2-1, fill=fill,width=5, tags = f"click{name}", outline = outline)
            canvas.tag_bind(f"click{name}","<Button-1>", lambda e: self.change_item())
            self.font_size=min(int(hours.get(end)-hours.get(start))-5, 15)
            self.title =canvas.create_text((30+bd+250-bd)/2,(hours.get(start)+bd2 +hours.get(end)-bd2)/2,anchor = 'center',text=name, font=("Modern No. 20", self.font_size), fill=fg,tags=f"click{name}")
            update_dict(self.get_item())
    def get_item(self):
        a = {self.name : " ".join([self.start,self.end,self.which])}
        return a
def add_item(event=None):
    global canvas,hours,ty
    i = Item("","6:00","6:00","event")
    i.change_item()
def update_dict(a, d=False):
    global name, items
    if d:
        try:
            del item_dict[a]
        except KeyError:
            jen="idk"
    else:
        item_dict.update(a)
    
    temp_file_path = file_path + '.tmp'
    rows = []
    header = []
    with open(file_path, 'r', newline="") as infile:
        reader = csv.DictReader(infile)
        header = reader.fieldnames
        for row in reader:
            rows.append(row)
    for row in rows:
        if row.get('name') == name:
            row['items'] = str(item_dict)
    with open(temp_file_path, 'w', newline="") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=header)
        writer.writeheader()
        writer.writerows(rows)
    os.replace(temp_file_path, file_path)
open_day(str(int(to[0])),to[1])


root.mainloop()
