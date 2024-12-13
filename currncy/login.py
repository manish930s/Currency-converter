from tkinter import messagebox
from tkinter import *
import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk
import pymysql

# Selecting GUI theme - dark, light , system (for system default)
ctk.set_appearance_mode("light")

# Selecting color theme - blue, green, dark-blue
ctk.set_default_color_theme("green")

root = tk.Tk()
root.configure(bg="#fff")
root.geometry("1520x780+0+0")


def resizeImage(image_path, width, height):
    pil_image = Image.open(image_path)
    resized = pil_image.resize((width, height), Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(resized)
def connect():
    if name_entry.get() == '':
        messagebox.showerror('Error', 'Please enter your username....')
    elif email_entry.get() == '':
        messagebox.showerror('Error', 'Please enter email...')
    elif password_entry.get() == '':
        messagebox.showerror('Error', 'Please enter password....')
    elif check.get()==0:
        messagebox.showerror('Error', 'Please accept Terms')
    else:
        try:
            con = pymysql.connect(host='localhost', user='root', password='Admin@21')
            mycursor = con.cursor()
        except:
            messagebox.showerror('Error', 'Database Connectivity Issue, Please Try Again')
            return

        query = 'use currency'
        mycursor.execute(query)

        query = 'select * from login where email= %s'
        mycursor.execute(query, (email_entry.get()))

        row = mycursor.fetchone()
        if row != None:
            messagebox.showerror('Error', 'Email ID Already exists')
        else:
            query = 'INSERT INTO login(username, email, password) VALUES (%s, %s, %s)'
            mycursor.execute(query, (
                name_entry.get(), email_entry.get(), password_entry.get()))
            con.commit()
            con.close()
            messagebox.showinfo('Success', 'Registration is Successful')





logo = resizeImage("mainlogo2.jpg",110, 80)
logo_label = tk.Label(root, image=logo, borderwidth=0,bg="black")
logo_label.place(x=30,y=30)

frame = ctk.CTkFrame(master=root,width=500, height=600)
frame.place(x=490, y=160)

fontt = ctk.CTkFont(family='Inter, ui-sans-serif', size=22)

label = ctk.CTkLabel(master=frame, text='Create a Account',font=fontt)
label.place(x=160, y=20)

fontn = ctk.CTkFont(family='Inter, ui-sans-serif', size=18)

name = ctk.CTkLabel(master=frame, text='Username',font=fontn)
name.place(x=120, y=100)
name_entry = ctk.CTkEntry(master=frame, placeholder_text="Enter your name",height=40,width=250)
name_entry.place(x=120, y=150)

email = ctk.CTkLabel(master=frame, text='Email',font=fontn)
email.place(x=120, y=200)
email_entry = ctk.CTkEntry(master=frame, placeholder_text="Enter your Email",height=40,width=250)
email_entry.place(x=120, y=250)

password = ctk.CTkLabel(master=frame, text='Password',font=fontn)
password.place(x=120, y=300)
password_entry = ctk.CTkEntry(master=frame, placeholder_text="Enter a Password",height=40,width=250)
password_entry.place(x=120, y=350)

check =IntVar()
checkbox = ctk.CTkCheckBox(master=frame, text='Remember Me',variable=check)
checkbox.place(x=120, y=420)
button = ctk.CTkButton(master=frame, text='Login',height=40,width=250,font=fontn, command=connect)
button.place(x=120, y=500)

root.mainloop()
