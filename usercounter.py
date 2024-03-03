from tkinter import *
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk
import mysql.connector
 
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
 
def reserve():
    vehicle_number = entry_vehicle_number.get()
    vehicle_type = entry_vehicle_type.get()
    vehicle_name = entry_vehicle_name.get()
    entry_time = entry_entry_time.get()
    slot_number = entry_slot_number.get()
    exit_time = entry_exit_time.get()
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
            cursor.execute("INSERT INTO parking (vehicle_number, vehicle_type, vehicle_name,slot_number,entry_time,exit_time) VALUES (%s, %s, %s, %s,%s,%s)", (vehicle_number, vehicle_type, vehicle_name,slot_number, entry_time,exit_time))
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
 
def submit_complaint():
    complaint_text = complaint_entry.get()[:255]
    if complaint_text.strip() == "":
        messagebox.showerror("ALERT!!!", "Enter complaint!!")
    else:
        try:
            con = mysql.connector.connect(
                host="",
                user="root",
                password="KilDReaper004",
                database="coventry"
            )
            cursor = con.cursor()
            cursor.execute("INSERT INTO complain (complain) VALUES (%s)", (complaint_text,))
            con.commit()
            messagebox.showinfo("Status", "Complaint submitted successfully!")
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Error connecting to database: {e}")
 
root = Tk()
root.title("Dashboard")
root.geometry("800x600")  
 
frame1 = Frame(root, bg="#398376", width=200, height=600)
frame1.grid(row=0, column=0, sticky="ns")
 
frame_dashboard = Frame(root, bg="#2C3E50", bd=2, relief="solid")
frame_complain = Frame(root, bg="#2C3E50", bd=2, relief="solid")  
frame_reserve = Frame(root, bg="#2C3E50", bd=2, relief="solid")
 
frames = {"Dashboard": frame_dashboard, "Complain": frame_complain, "Reserve": frame_reserve}
 
for frame in frames.values():
        frame.grid(row=0, column=1, sticky="nsew")
 
labels = ["Dashboard", "Complain", "Reserve"]
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
        raise_frame(frame_reserve)
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
 
Label(frame_complain, text="Submit a Complaint (upto 255 words)", font=('Helvetica', 20), bg="#2C3E50", fg="white").pack()
complaint_entry = Text(frame_complain,height=5, width=50, font=('Helvetica', 14))
complaint_entry.pack(pady=10)
submit_button = Button(frame_complain, text="Submit", font=('Helvetica', 16), bg="#2C3E50", fg="white", command=submit_complaint)
submit_button.pack(pady=10)
 
Label(frame_reserve, text="Reserve Parking Slot", font=('Helvetica', 24), bg="#2C3E50", fg="white")
 
Label(frame_reserve, text="Vehicle Name:", font=('Helvetica', 16), bg="#2C3E50", fg="white").grid(row=0, pady=10, padx=10, sticky='w')
entry_vehicle_name = Entry(frame_reserve, font=('Helvetica', 14))
entry_vehicle_name.grid(row=0, column=1, pady=10, padx=10)
 
Label(frame_reserve, text="Vehicle Number:", font=('Helvetica', 16), bg="#2C3E50", fg="white").grid(row=1, pady=10, padx=10, sticky='w')
entry_vehicle_number = Entry(frame_reserve, font=('Helvetica', 14))
entry_vehicle_number.grid(row=1, column=1, pady=10, padx=10)
 
Label(frame_reserve, text="Vehicle Type:", font=('Helvetica', 16), bg="#2C3E50", fg="white").grid(row=2, pady=10, padx=10, sticky='w')
entry_vehicle_type = Entry(frame_reserve, font=('Helvetica', 14))
entry_vehicle_type.grid(row=2, column=1, pady=10, padx=10)
 
Label(frame_reserve, text="Slot Number:", font=('Helvetica', 16), bg="#2C3E50", fg="white").grid(row=3, pady=10, padx=10, sticky='w')
entry_slot_number = Entry(frame_reserve, font=('Helvetica', 14))
entry_slot_number.grid(row=3, column=1, pady=10, padx=10)
 
Label(frame_reserve, text="Checkin time:", font=('Helvetica', 16), bg="#2C3E50", fg="white").grid(row=4, pady=10, padx=10, sticky='w')
entry_entry_time = Entry(frame_reserve, font=('Helvetica', 14))
entry_entry_time.grid(row=4, column=1, pady=10, padx=10)
 
Label(frame_reserve, text="Checkout time:", font=('Helvetica', 16), bg="#2C3E50", fg="white").grid(row=5, pady=10, padx=10, sticky='w')
entry_exit_time = Entry(frame_reserve, font=('Helvetica', 14))
entry_exit_time.grid(row=5, column=1, pady=10, padx=10)
 
submit_button = Button(frame_reserve, text="Submit", font=('Helvetica', 16), bg="#2C3E50", fg="white",
                        command=reserve)
submit_button.grid(row=6, columnspan=35, pady=20)
 
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
tree = ttk.Treeview(root)
slot_buttons = []
root.mainloop()