from tkinter import*
import tkinter as tk
from tkinter import messagebox
import mysql.connector
from tkinter import ttk

def login():
    email = entry_email.get()
    password = entry_password.get()

    if not email or not password:
        messagebox.showerror("Error", "Please enter both enail and password.")
        return

    try:
        cursor.execute("SELECT * FROM user WHERE email = %s AND password = %s", (email, password))
        user = cursor.fetchone()
        if user:
            messagebox.showinfo("Success", "Login successful!")
        else:
            messagebox.showerror("Error", "Invalid email or password.")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error logging in: {err}")

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="KilDReaper004",
    database="coventry"
)

cursor = db.cursor()

root = Tk()
root.geometry('1920x1080')
root.title('Parking')

box = tk.Frame(root, width=1920, height=1080, bg='#014421')
box.place(relx=0.5, rely=0.5, anchor='center')

welcome = Label(root, text='WELCOME', font=(30))
welcome.place(relx=0.5, y=150, anchor='center')

email = Label(box, text='Email', font=(10))
email.place(relx=0.39, y=365)
entry_email = Entry(root, width=26, font=(16))
entry_email.place(relx=0.5, y=260, anchor='center')

password = Label(box, text='Password', font=(10))
password.place(relx=0.37, y=465)
entry_password = Entry(root, show="*", width=26, font=(16))
entry_password.place(relx=0.5, y=360, anchor='center')

role = Label(box, text='Role', font=(10))
role.place(relx=0.39, y=560)
clicked = tk.StringVar()

role_menu = ttk.Combobox(root, textvariable=clicked, values=['Admin', 'User'], font=(16), width=25)
role_menu.place(relx=0.5, y=460, anchor='center')

login_button = Button(root, width=26, text='Login', font=(12), command=login)
login_button.place(relx=0.5, y=560, anchor='center')

sign_up = Label(root, text="Don't have an accout?", font=(10))
sign_up.place(relx=0.45, y=600, anchor='center')
create_one = Label(root, text="Create one.", font=(10), fg='#014421', bg='#014421')
create_one.place(relx=0.555, y=600, anchor='center')

def open_user_registration():
    root.destroy()
    from user_registration import add_user
    add_user()
register_button = Button(root, text='Register.', font=(10),command=open_user_registration)
register_button.place(relx=0.557, y=600, anchor='center')


root.mainloop()