from tkinter import *
import tkinter as tk
from tkinter import messagebox
import mysql.connector

def update_password():
        email = entry_email.get()
        new_password = entry_new_password.get()
        confirm_password = entry_confirm_password.get()

        if not email or not new_password or not confirm_password:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        if new_password != confirm_password:
            messagebox.showerror("Error", "New passwords do not match.")
            return

        try:
            cursor.execute("UPDATE user SET password = %s WHERE email = %s", (new_password, email))
            db.commit()
            messagebox.showinfo("Success", "Password updated successfully!")
            root.destroy()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error updating password: {err}")

root = Tk()
root.title("Forgot password")
root.geometry("900x600")
root.config(bg="white")

label_email = tk.Label(root, text="Email:")
label_email.pack()

entry_email = tk.Entry(root)
entry_email.pack()

label_new_password = tk.Label(root, text="New Password:")
label_new_password.pack()

entry_new_password = tk.Entry(root, show="*")
entry_new_password.pack()

label_confirm_password = tk.Label(root, text="Confirm Password:")
label_confirm_password.pack()

entry_confirm_password = tk.Entry(root, show="*")
entry_confirm_password.pack()

button_update_password = tk.Button(root, text="Update Password", command=update_password)
button_update_password.pack()

db = mysql.connector.connect(
    host="",
    user="root",
    passwd="KilDReaper004",
    database="coventry"
)

cursor = db.cursor()



root.mainloop()
