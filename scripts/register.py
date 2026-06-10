import customtkinter as ctk
import re
import tkinter as tk
import db
from datetime import datetime

def register_screen(container, main_frame, show_frame):
    register_frame = ctk.CTkFrame(container, fg_color="#fca265", bg_color="#ffe7d6", width=800, height=600)
    register_frame.grid(row=0, column=0, sticky="nsew",padx=40, pady=40)
    register_frame.grid_rowconfigure(0, weight=1)
    register_frame.grid_columnconfigure(0, weight=1)

    ctk.CTkLabel(
        register_frame,
        text="User Registration",
        font=("Arial",56,"bold"),
        text_color="black"
    ).place(x=800,y=80)
    

    # Labels and Entries

    ctk.CTkLabel(register_frame, text="Username:", text_color="black",font=("Arial",29)).place(x=200,y=150)
    register_uname_entry = ctk.CTkEntry(register_frame, width=250, fg_color="white", text_color="black")
    register_uname_entry.place(x=370,y=153)

    ctk.CTkLabel(register_frame, text="First Name:", text_color="black",font=("Arial",29)).place(x=200,y=230)
    first_name_entry = ctk.CTkEntry(register_frame, width=250, fg_color="white", text_color="black")
    first_name_entry.place(x=370,y=233)

    ctk.CTkLabel(register_frame, text="Last Name:", text_color="black",font=("Arial",29)).place(x=670,y=230)
    last_name_entry = ctk.CTkEntry(register_frame, width=250, fg_color="white", text_color="black")
    last_name_entry.place(x=840,y=233)

    ctk.CTkLabel(register_frame, text="Password:", text_color="black",font=("Arial",29)).place(x=200,y=310)
    register_pwd_entry = ctk.CTkEntry(register_frame, show="*", width=250, fg_color="white", text_color="black")
    register_pwd_entry.place(x=370,y=313)

    ctk.CTkLabel(register_frame,text="Confirm Password:", text_color="black",font=("Arial",29)).place(x=670,y=310)
    confirm_entry = ctk.CTkEntry(register_frame,show="*", width=250, fg_color="white", text_color="black")
    confirm_entry.place(x=920,y=313)

    ctk.CTkLabel(register_frame,text="Email:", text_color="black",font=("Arial",29)).place(x=200,y=390)
    email_entry = ctk.CTkEntry(register_frame, width=250, fg_color="white", text_color="black")
    email_entry.place(x=370,y=393)

    ctk.CTkLabel(register_frame,text="Phone:", text_color="black",font=("Arial",29)).place(x=670,y=390)
    phone_entry = ctk.CTkEntry(register_frame, width=100, fg_color="white", text_color="black")
    phone_entry.place(x=780,y=393)

    ctk.CTkLabel(register_frame,text="Address:", text_color="black",font=("Arial",29)).place(x=200,y=470)
    address_entry = ctk.CTkEntry(register_frame, width=800, fg_color="white", text_color="black")
    address_entry.place(x=370,y=473)

    ctk.CTkLabel(register_frame,text="Date of Birth:", text_color="black",font=("Arial",29)).place(x=200,y=550)
    dob_entry = ctk.CTkEntry(register_frame, width=80, fg_color="white", text_color="black")
    dob_entry.place(x=370,y=553)
    ctk.CTkLabel(register_frame,text="(YYYY-MM-DD)", text_color="black",font=("Arial",22)).place(x=200,y=590)

    ctk.CTkLabel(register_frame,text="Gender:", text_color="black",font=("Arial",29)).place(x=200,y=630)
    gender_entry = ctk.CTkEntry(register_frame, width=250, fg_color="white", text_color="black")
    gender_entry.place(x=370,y=633)

    # Textbox
    textbox = ctk.CTkTextbox(register_frame, width=200, height=50, text_color="tomato", fg_color="white", border_color="tomato")

    def reg_submit():
        textbox.delete("0.0", "end")
        username = register_uname_entry.get()
        password = register_pwd_entry.get()
        confirm = confirm_entry.get()
        email = email_entry.get()
        phone = phone_entry.get()
        address = address_entry.get()
        gender = gender_entry.get()
        dob = dob_entry.get()
        pwd_check = password != confirm
        email_check = re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email) is None
        phone_check = re.match(r'^[6-9]\d{9}$', phone) is None
        dob_check = False
        try:
            dob_date = datetime.strptime(dob, "%d-%m-%Y")

            current_year = datetime.now().year

            if dob_date.year < 1900 or dob_date.year > current_year:
                tk.messagebox.showerror("Error", "Enter a valid birth year!")
            else:
                dob = dob_date.strftime("%Y-%m-%d")
                dob_check = True
        except ValueError:
            tk.messagebox.showerror("Error", "Invalid DOB! Must be in format DD-MM-YYYY")

        if not username or not password or not confirm or not email or not phone or not address or not gender or not dob:
            tk.messagebox.showerror("Error", "Please fill all fields!")
        elif pwd_check:
            tk.messagebox.showerror("Error", "Passwords do not match!")
        elif email_check:
            tk.messagebox.showerror("Error", "Invalid email!")
        elif phone_check:   
            tk.messagebox.showerror("Error", "Invalid phone number! Must be 10 digits starting with 6-9.")
        elif not dob_check:
            pass
        else:
            registered = db.register(username, password, email, phone, address, gender, dob)
            if registered:
                tk.messagebox.showinfo("Success", "Registration successful! You can now log in.")
            else:
                tk.messagebox.showerror("Error", "Username already exists! Please choose a different one.")
        

    ctk.CTkButton(
        register_frame,
        text="Submit",
        command=reg_submit,
        text_color="black",
        fg_color="#7ed957",
        hover_color="#99D980",
        width=200,
        height=40,
        font=("Arial", 26, "bold")    
    ).place(x=800,y=600)

    ctk.CTkButton(
        register_frame,
        text="Back",
        command=lambda: show_frame(main_frame),
        width=100,
        height=40,
        fg_color="tomato",
        text_color="black",
        hover_color="#FC846F",
        bg_color="#ffea00",
        font=("Arial", 16, "bold")
    ).place(x=50,y=50)
    
    return register_frame