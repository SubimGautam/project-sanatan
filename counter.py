from tkinter import *
from tkinter import messagebox
import tkinter as tk
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

def create_slots(parent, occupied_slots):
    slot_buttons = []
    for i in range(50):
        slot_number = i + 1
        slot_text = f"Slot {slot_number}"
        button = Button(parent, text=slot_text, command=lambda idx=slot_number: print(f"Slot {idx} clicked"))
        if str(slot_number) in occupied_slots:
            button.configure(bg="red")
        slot_buttons.append(button)
        button.grid(row=i // 10, column=i % 10, pady=5, padx=5)
    return slot_buttons

def fetch_occupied_slots():
    try:
        con = mysql.connector.connect(
            host="",
            user="root",
            password="KilDReaper004",
            database="coventry"
        )
        cursor = con.cursor()
        cursor.execute("SELECT vehicle_number FROM parking")
        occupied_slots = [str(result[0]) for result in cursor.fetchall()]  # Convert to string
        cursor.close()
        con.close()
        return occupied_slots
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Error connecting to database: {e}")
        return []

def add_vehicle():
    vehicle_number = entry_vehicle_number.get()
    vehicle_type = entry_vehicle_type.get()
    vehicle_name = entry_vehicle_name.get()
    entry_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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
            cursor.execute("INSERT INTO parking (vehicle_number, vehicle_type, vehicle_name, entry_time) VALUES (%s, %s, %s, %s)", (vehicle_number, vehicle_type, vehicle_name, entry_time))
            con.commit()
            messagebox.showinfo("Status", "Successfully inserted!")
            occupied_slots = fetch_occupied_slots()
            refresh_slots(occupied_slots)
            con.close()
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Error connecting to database: {e}")

def refresh_slots(occupied_slots):
    for button in slot_buttons:
        slot_number = int(button['text'].split()[1])
        if str(slot_number) in occupied_slots:
            button.configure(bg="red")
        else:
            button.configure(bg="SystemButtonFace")


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


root = Tk()
root.title("Dashboard")
root.geometry("800x600")

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
occupied_slots = fetch_occupied_slots()
slot_buttons = create_slots(frame_dashboard, occupied_slots)

Label(frame_add_vehicle, text="Vehicle Name:", font=('Helvetica', 16), bg="#2C3E50", fg="white").grid(row=0, pady=10, padx=10, sticky='w')
entry_vehicle_name = Entry(frame_add_vehicle, font=('Helvetica', 14))
entry_vehicle_name.grid(row=0, column=1, pady=10, padx=10)

Label(frame_add_vehicle, text="Vehicle Number:", font=('Helvetica', 16), bg="#2C3E50", fg="white").grid(row=1, pady=10, padx=10, sticky='w')
entry_vehicle_number = Entry(frame_add_vehicle, font=('Helvetica', 14))
entry_vehicle_number.grid(row=1, column=1, pady=10, padx=10)

Label(frame_add_vehicle, text="Vehicle Type:", font=('Helvetica', 16), bg="#2C3E50", fg="white").grid(row=2, pady=10, padx=10, sticky='w')
entry_vehicle_type = Entry(frame_add_vehicle, font=('Helvetica', 14))
entry_vehicle_type.grid(row=2, column=1, pady=10, padx=10)

submit_button = Button(frame_add_vehicle, text="Submit", font=('Helvetica', 16), bg="#2C3E50", fg="white",
                        command=add_vehicle)
submit_button.grid(row=4, columnspan=35, pady=20)

Label(frame_exit_vehicle, text="Vehicle Number:", font=('Helvetica', 16), bg="#2C3E50", fg="white").grid(row=0, pady=10, padx=10, sticky='w')
entry_exit_vehicle_number = Entry(frame_exit_vehicle, font=('Helvetica', 14))
entry_exit_vehicle_number.grid(row=0, column=1, pady=10, padx=10)

exit_button = Button(frame_exit_vehicle, text="Exit Vehicle", font=('Helvetica', 16), bg="#2C3E50", fg="white",
                        command=exit_vehicle)
exit_button.grid(row=1, columnspan=2, pady=20)

Label(frame_view_reports, text="View Reports", font=('Helvetica', 24), bg="#2C3E50", fg="white").pack(pady=20)

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
    tk.messagebox.showerror("Error", f"Error connecting to database: {e}")

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

root.mainloop() 