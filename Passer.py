import json
import pyperclip
from tkinter import *
from tkinter import messagebox
from cryptography.fernet import Fernet
from random import randint, choice, shuffle
import sys
import sqlite3


def password_gen():

    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]
    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)
    password = "".join(password_list)

    ps_entry.delete(0, END)
    ps_entry.insert(0, password)
    pyperclip.copy(password)


def encrypt(password):
    key = b'Io3GhZ-3C4qbcR4_RbiPAJ2aXpbU5FYJAR33t6Tn9xs='
    cipher = Fernet(key)

    password_as_bytes = str.encode(password)  # Convert string with password into bytes
    secured_password_bytes = cipher.encrypt(password_as_bytes)  # Ciphering our bytes password and get result also in bytes
    return secured_password_bytes.decode()  # Returning ciphered bytes password and convert it into string


def decrypt(password):
    key = b'Io3GhZ-3C4qbcR4_RbiPAJ2aXpbU5FYJAR33t6Tn9xs='
    cipher = Fernet(key)

    password_as_bytes = str.encode(password)  # Convert string with ciphered password into bytes
    decrypted_password_bytes = cipher.decrypt(password_as_bytes)  # Decrypting our bytes secured password and get result also in bytes
    return decrypted_password_bytes.decode()  # Returning decrypted bytes password and convert it into string


def save():

    website = ws_entry.get().lower()
    email = eu_entry.get()
    password = encrypt(ps_entry.get())

    connect = sqlite3.connect('info.db')
    cursor = connect.cursor()

    if len(website) == 0 or len(email) == 0 or len(ps_entry.get()) == 0:
        messagebox.showwarning(title="Warning", message="You have the empty field")
    else:
        try:
            cursor.execute("INSERT INTO data VALUES (?, ?, ?)", (website, email, password))
            connect.commit()
            messagebox.showinfo(message="Done!")
        except Exception as ex:
            messagebox.showinfo(message="This site is already exist")

        ws_entry.delete(0, END)
        ps_entry.delete(0, END)


def search():
    connect = sqlite3.connect('info.db')
    cursor = connect.cursor()
    try:
        cursor.execute(f"SELECT * FROM data WHERE website = '{ws_entry.get().lower()}'")
        ws = cursor.fetchall()
        em = ws[0][1]
        ps = decrypt(ws[0][2])
        messagebox.showinfo(message=f"Website: {ws_entry.get()}\nEmail: {em}\nPassword: {ps}")
        pyperclip.copy(ps)
    except IndexError:
        messagebox.showinfo(message="There is no such site in the database")


def enter_program():

    connect = sqlite3.connect('info.db')
    cursor = connect.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS data(
        website TEXT PRIMARY KEY,
        login TEXT,
        password TEXT
    )""")
    connect.commit()

    cursor.execute("SELECT * FROM data WHERE website = 'userlogpas'")
    password = cursor.fetchall()

    try:
        if pas_entr.get() == decrypt(password[0][2]):
            window.deiconify()  # Unhides the main window
            login_window.destroy()  # Removes the login_window window
        else:
            messagebox.showerror(message="Wrong password")
    except IndexError:
        cursor.execute("INSERT INTO data VALUES (?, ?, ?)", ('userlogpas', 'login', encrypt(pas_entr.get())))
        connect.commit()


def exit_program():
    sys.exit()  # Ends the script


window = Tk()  # Declares window as the tkinter main window
login_window = Toplevel()  # Creates the login_window window
window.iconbitmap("./images/lock.ico")
window.title("PasswordManager")
window.config(padx=50, pady=50)

# --------------------------------LoginForm--------------------------------------

login_window.iconbitmap("./images/lock.ico")
login_window.title("Authentication")
login_window.config(padx=10, pady=10)

pas_lable = Label(login_window, text="Password: ")
pas_entr = Entry(login_window, show="*")  # Password entry
pas_entr.focus()

eye_photo = PhotoImage(file="./images/eye.png")


def show(ps_entr=pas_entr):
    if ps_entr["show"] == "":
        ps_entr.config(show="*")
    else:
        ps_entr.config(show="")


show_btn = Button(login_window, image=eye_photo, bd=0, command=show)
log_btn = Button(login_window, text="Login", width=15, bd=0, bg="#a8ffb1", command=enter_program)  # Login button
cnl_btn = Button(login_window, text="Cancel", width=15, bd=0, command=exit_program)  # Cancel button

# These pack the elements, this includes the items for the main window
pas_entr.grid(column=1, row=0, columnspan=2, padx=5)
log_btn.grid(column=2, row=1, columnspan=2, pady=5)
cnl_btn.grid(column=0, row=1, columnspan=2, pady=5)
show_btn.grid(column=3, row=0)
pas_lable.grid(column=0, row=0)

# -------------------------------------------------------------------------------

canvas = Canvas(width=200, height=230)
lock_img = PhotoImage(file="./images/lock.png")
canvas.create_image(80, 105, image=lock_img)
canvas.grid(column=1, row=0, sticky=W)

ws_label = Label(window, text="Website:")
ws_label.grid(column=0, row=1)

ws_entry = Entry(window, width=32)
ws_entry.focus()
ws_entry.grid(column=1, row=1, columnspan=2, sticky=W)

ws_button = Button(window, text="Search", bd=1, command=search)
ws_button.grid(column=1, row=1, columnspan=2, sticky=E)

eu_label = Label(window, text="Email/Username:")
eu_label.grid(column=0, row=2)

eu_entry = Entry(window, width=40)
eu_entry.insert(0, "bogovs969@gmail.com")
eu_entry.grid(column=1, row=2, columnspan=2, sticky=W)

ps_label = Label(window, text="Password:")
ps_label.grid(column=0, row=3)

ps_entry = Entry(window, width=22)
ps_entry.grid(column=1, row=3, sticky=W)

gen_ps_button = Button(window, text="Generate password", bd=1, command=password_gen)
gen_ps_button.grid(column=1, row=3, columnspan=2, sticky=E)

add_button = Button(window, text="Add", width=34, height=2, bd=0, bg="#a8ffb1", command=save)
add_button.grid(column=1, row=4, columnspan=2, sticky=W)

window.withdraw()  # This hides the main window, it's still present it just can't be seen or interacted with
window.mainloop()
