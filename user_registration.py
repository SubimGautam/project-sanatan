from tkinter import *
from tkinter import messagebox
import mysql.connector

def is_valid_email(email):
    return validate_email(email)
from validate_email_address import validate_email

def add_user():
    user_name = entry_user_name.get()
    user_id = entry_user_id.get()
    full_name = entry_full_name.get()
    email = entry_email.get()
    password = entry_password.get()

    if(user_name == "" or user_id == "" or full_name =="" or password == "" or email == ""):
        messagebox.showerror("ALERT!!!", "Insert values!!")
    else:
        con = mysql.connector.connect(
            host = "",
            user = "root",
            password = "KilDReaper004",
            database = "coventry"
        )
        cursor = con.cursor()
        cursor.execute("insert into user values('" + user_name + "','" + user_id + "', '" + full_name + "', '" + email + "', '" + password + "')")
        cursor.execute("commit");

        messagebox.showinfo("Status", "Successfully insterted!")
        con.close();



root = Tk()
root.title("Vehicle Database")
root.geometry("900x600")
root.config(bg="#03fcad")
 
style = {'font': ('Georgia', 12), 'bg': "#03fcad", 'fg': "Black"}
 
Label(root, text="User_name:", **style).place(x=15, y=15)
entry_user_name = Entry(root, **style)
entry_user_name.place(x=200, y=15)
 
Label(root, text="User_number:", **style).place(x=15, y=70)
entry_user_id = Entry(root, **style)
entry_user_id.place(x=200, y=70)
 
Label(root, text="Full_name:", **style).place(x=15, y=130)
entry_full_name = Entry(root, **style)
entry_full_name.place(x=200, y=130)

Label(root, text="email:", **style).place(x=15, y=195)
entry_email = Entry(root, **style)
entry_email.place(x=200, y=195)

Label(root, text="Password:", **style).place(x=15, y=240)
entry_password = Entry(root, **style)
entry_password.place(x=200, y=240)
 
 
Button(root, text="Add User", command=add_user, height=2, width=25, bd=4, bg="#27AE60", fg="white", font=('Arial', 12, 'bold')).place(x=55, y=300)
 
root.mainloop()