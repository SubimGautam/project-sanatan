from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import mysql.connector
from datetime import datetime

def raise_frame(frame):
    frame.tkraise()

def create_buttons(parent, labels, frames):
    button_style = {'font': ('Helvetica', 14), 'bg': "#2C3E50", 'fg': "white", 'padx': 10, 'pady': 5, 'width': 15, 'height': 2}
    buttons = []
    for label in labels:
        button = Button(parent, text=label, command=lambda l=label: raise_frame(frames[l]))
        button.configure(**button_style)
        buttons.append(button)
    return buttons

def add_vehicle():
    vehicle_number = entry_vehicle_number.get()
    vehicle_type = entry_vehicle_type.get()
    vehicle_name = entry_vehicle_name.get()
    entry_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    slot_number = entry_slot_number.get()
    if vehicle_number == "" or vehicle_type == "" or vehicle_name == "":
        messagebox.showerror("ALERT!!!", "Insert values!!")
    else:
        try:
            con = mysql.connector.connect(
                host="",
                user="root",
                password="KilDReaper004",
                database="coventry"
            )
            cursor = con.cursor()
            cursor.execute("INSERT INTO parking (vehicle_number, vehicle_type, vehicle_name, entry_time,slot_number) VALUES (%s, %s, %s, %s,%s)", (vehicle_number, vehicle_type, vehicle_name, entry_time,slot_number))
            con.commit()
            messagebox.showinfo("Status", "Successfully inserted!")
            occupied_slots.append(int(slot_number))
            update_slot_colors()
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Error connecting to database: {e}")

def update_slot_colors():
    for slot_button in slot_buttons:
        slot_number = int(slot_button['text'].split()[1])
        if slot_number in occupied_slots:
            slot_button.configure(bg="red")
        else:
            slot_button.configure(bg="#2C3E50")
def exit_vehicle():
    vehicle_number = entry_exit_vehicle_number.get()
    exit_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if vehicle_number == "":
        messagebox.showerror("ALERT!!!", "Enter vehicle number!!")
    else:
        try:
            con = mysql.connector.connect(
                host="",
                user="root",
                password="KilDReaper004",
                database="coventry"
            )
            cursor = con.cursor()
            cursor.execute("UPDATE parking SET exit_time = %s WHERE vehicle_number = %s", (exit_time, vehicle_number))
            con.commit()
            messagebox.showinfo("Status", "Exit time recorded successfully!")
            con.close()
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Error connecting to database: {e}")

def refresh_dashboard():
    try:
        conn = mysql.connector.connect(
            host="",
            user="root",
            password="KilDReaper004",
            database="coventry"
        )
        cursor = conn.cursor()

        query = "SELECT DISTINCT slot_number FROM parking WHERE exit_time IS NULL"
        cursor.execute(query)
        occupied_slots_result = cursor.fetchall()
        occupied_slots.clear()
        for slot in occupied_slots_result:
            occupied_slots.append(slot[0])

        cursor.close()
        conn.close()
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Error connecting to database: {e}")

    update_slot_colors()

root = Tk()
root.title("Parking Management system")
root.geometry("1920x1080")

frame1 = Frame(root, bg="#398376", width=200, height=600)
frame1.grid(row=0, column=0, sticky="ns")

frame_dashboard = Frame(root, bg="#2C3E50", bd=2, relief="solid")
frame_add_vehicle = Frame(root, bg="#2C3E50", bd=2, relief="solid")  
frame_view_reports = Frame(root, bg="#2C3E50", bd=2, relief="solid")
frame_exit_vehicle = Frame(root, bg="#2C3E50", bd=2, relief="solid")

frames = {"Dashboard": frame_dashboard, "Add Vehicle": frame_add_vehicle, "View Reports": frame_view_reports, "Exit Vehicle": frame_exit_vehicle}

for frame in frames.values():
    frame.grid(row=0, column=1, sticky="nsew")

labels = ["Dashboard", "Add Vehicle", "View Reports", "Exit Vehicle"]
buttons = create_buttons(frame1, labels, frames)
for i, button in enumerate(buttons, 1):
    button.grid(row=i, pady=10)

Label(frame_dashboard, text="Dashboard Content", font=('Helvetica', 24), bg="#2C3E50", fg="white")
num_slots = 50
num_cols = 10
num_rows = num_slots // num_cols
slot_buttons = []
occupied_slots = []

def mark_slot_occupied(slot_number):
    if slot_number not in occupied_slots:
        occupied_slots.append(slot_number)
        update_slot_colors()
        raise_frame(frame_add_vehicle)
        entry_slot_number.delete(0, END)
        entry_slot_number.insert(0, slot_number)
try:
    conn = mysql.connector.connect(
        host="",
        user="root",
        password="KilDReaper004",
        database="coventry"
    )
    cursor = conn.cursor()

    query = "SELECT DISTINCT slot_number FROM parking WHERE exit_time IS NULL"
    cursor.execute(query)
    occupied_slots_result = cursor.fetchall()

    for slot in occupied_slots_result:
        occupied_slots.append(slot[0])

    cursor.close()
    conn.close()
except mysql.connector.Error as e:
    messagebox.showerror("Error", f"Error connecting to database: {e}")

for i in range(num_rows):
    row_frame = Frame(frame_dashboard, bg="#2C3E50")
    row_frame.pack()
    for j in range(num_cols):
        slot_number = i*num_cols + j + 1
        slot_button = Button(row_frame, text=f"Slot {slot_number}", font=('Helvetica', 12), bg="#2C3E50", fg="white")
        slot_button.pack(side=LEFT, padx=10, pady=5)
        slot_buttons.append(slot_button)
        slot_button.config(command=lambda slot_number=slot_number: mark_slot_occupied(slot_number))

refresh = Button(frame_dashboard, text="Refresh", font=('Helvetica', 16), bg="white", fg="black",
                        command=refresh_dashboard)
refresh.pack()
                        
Label(frame_add_vehicle, text="Vehicle Name:", font=('Helvetica', 16), bg="#2C3E50", fg="white").grid(row=0, pady=10, padx=10, sticky='w')
entry_vehicle_name = Entry(frame_add_vehicle, font=('Helvetica', 14))
entry_vehicle_name.grid(row=0, column=1, pady=10, padx=10)

Label(frame_add_vehicle, text="Vehicle Number:", font=('Helvetica', 16), bg="#2C3E50", fg="white").grid(row=1, pady=10, padx=10, sticky='w')
entry_vehicle_number = Entry(frame_add_vehicle, font=('Helvetica', 14))
entry_vehicle_number.grid(row=1, column=1, pady=10, padx=10)

Label(frame_add_vehicle, text="Vehicle Type:", font=('Helvetica', 16), bg="#2C3E50", fg="white").grid(row=2, pady=10, padx=10, sticky='w')
entry_vehicle_type = Entry(frame_add_vehicle, font=('Helvetica', 14))
entry_vehicle_type.grid(row=2, column=1, pady=10, padx=10)

Label(frame_add_vehicle, text="Slot Number:", font=('Helvetica', 16), bg="#2C3E50", fg="white").grid(row=3, pady=10, padx=10, sticky='w')
entry_slot_number = Entry(frame_add_vehicle, font=('Helvetica', 14))
entry_slot_number.grid(row=3, column=1, pady=10, padx=10)

submit_button = Button(frame_add_vehicle, text="Submit", font=('Helvetica', 16), bg="#2C3E50", fg="white",
                        command=add_vehicle)
submit_button.grid(row=4, columnspan=35, pady=20)

Label(frame_exit_vehicle, text="Vehicle Number:", font=('Helvetica', 16), bg="#2C3E50", fg="white").grid(row=0, pady=10, padx=10, sticky='w')
entry_exit_vehicle_number = Entry(frame_exit_vehicle, font=('Helvetica', 14))
entry_exit_vehicle_number.grid(row=0, column=1, pady=10, padx=10)

exit_button = Button(frame_exit_vehicle, text="Exit Vehicle", font=('Helvetica', 16), bg="#2C3E50", fg="white",
                        command=exit_vehicle)
exit_button.grid(row=1, columnspan=2, pady=20)

Label(frame_view_reports, text="View Reports", font=('Helvetica', 24), bg="#2C3E50", fg="white").pack(pady=40)

table_frame = Frame(frame_view_reports, bg="#2C3E50")
table_frame.pack()

tree = ttk.Treeview(table_frame, columns=("vehicle_number", "vehicle_type", "vehicle_name", "entry_time", "exit_time"), show="headings")
tree.heading("vehicle_number", text="Vehicle Number")
tree.heading("vehicle_type", text="Vehicle Type")
tree.heading("vehicle_name", text="Vehicle Name")
tree.heading("entry_time", text="Entry Time")
tree.heading("exit_time", text="Exit Time")

tree.pack()

try:
    conn = mysql.connector.connect(
        host="",
        user="root",
        password="KilDReaper004",
        database="coventry"
    )
    cursor = conn.cursor()

    query = "SELECT * FROM parking "
    cursor.execute(query)
    users_data = cursor.fetchall()

    for user in users_data:
        tree.insert("", "end", values=user)

    cursor.close()
    conn.close()
except mysql.connector.Error as e:
    messagebox.showerror("Error", f"Error connecting to database: {e}")

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

root.mainloop()
