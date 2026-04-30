import customtkinter as ctk
import db
import re
from PIL import Image, ImageTk

def show_frame(frame):
    frame.tkraise()


def main():
    app = ctk.CTk()
    app.title("Cat-Nip")
    app.geometry("800x600")
    app.after(0, lambda: app.state('zoomed')) 

    # App icon
    Icon = ctk.CTkImage(Image.open("assets/catnipico.png"), size=(500, 400))

    # Main container
    container = ctk.CTkFrame(app)
    container.pack(fill="both", expand=True)

    container.grid_rowconfigure(0, weight=1)
    container.grid_columnconfigure(0, weight=1)


    # ---------------- HOME SCREEN ----------------
    main_frame = ctk.CTkFrame(container, fg_color="white")
    main_frame.grid(row=0, column=0, sticky="nsew")

    main_frame.grid_columnconfigure(0, weight=1)
    main_frame.grid_columnconfigure(1, weight=1)
    main_frame.grid_rowconfigure(0, weight=1)

    left_frame = ctk.CTkFrame(main_frame, fg_color="#ffde59", width=300, height=300)
    left_frame.grid(row=0, column=0, sticky="nsew", padx=40, pady=40)

    right_frame = ctk.CTkFrame(main_frame, fg_color="#ffffff", width=200, height=300)
    right_frame.grid(row=0, column=1, sticky="nsew", padx=40, pady=40)

    img_label = ctk.CTkLabel(left_frame, text="",image=Icon, fg_color="#ffde59")
    img_label.image = Icon
    img_label.place(x=120, y=230)

    ctk.CTkLabel(
        left_frame,
        text="Cat-Nip",
        text_color="black",
        fg_color="#ffde59",
        font=("Arial", 84, "bold")
    ).place(x=210, y=100)


    # ---------------- LOGIN SCREEN ----------------
    login = ctk.CTkFrame(container, fg_color="white", width=800, height=600)
    login.grid(row=0, column=0, sticky="nsew")

    login.grid_columnconfigure(0, weight=1)
    login.grid_columnconfigure(1, weight=1)
    login.grid_rowconfigure(0, weight=1)

    login_lframe = ctk.CTkFrame(login, fg_color="#ffde59",width=200, height=300)
    login_lframe.grid(row=0, column=0, sticky="nsew",padx=40, pady=40)

    login_rframe = ctk.CTkFrame(login, fg_color="#ffe683", width=300, height=600)
    login_rframe.grid(row=0, column=1, sticky="nsew",padx=40, pady=40)

    ctk.CTkLabel(login_lframe, text="Login", fg_color="#ffde59", text_color="black", font=("Arial", 64, "bold")).place(x=220, y=100)

    # User type radio buttons
    loginch = ctk.StringVar()
    loginch.set("user")
    ctk.CTkRadioButton(
        login_lframe, text="User",
        variable=loginch, value="user",
        fg_color="#f9b746",
        text_color="black",
        font=("Arial", 24, "bold")
    ).place(x=250, y=250)

    ctk.CTkRadioButton(
        login_lframe, text="Employee",
        variable=loginch, value="employee",
        fg_color="#f9b746",
        text_color="black",
        font=("Arial", 24, "bold")
    ).place(x=250, y=350)

    ctk.CTkRadioButton(
        login_lframe, text="Admin",
        variable=loginch, value="admin",
        fg_color="#f9b746",
        text_color="black",
        font=("Arial", 24, "bold")
    ).place(x=250, y=450)

    # Login fields
    ctk.CTkLabel(login_rframe, text="Username:",text_color="black", fg_color="#ffe683", font=("Arial", 34, "bold")).place(x=180, y=250)
    login_uname_entry = ctk.CTkEntry(login_rframe, width=150)
    login_uname_entry.place(x=420, y=257)

    ctk.CTkLabel(login_rframe, text="Password:",text_color="black", fg_color="#ffe683", font=("Arial", 34, "bold")).place(x=180, y=320)
    login_pwd_entry = ctk.CTkEntry(login_rframe, show="*", width=150)
    login_pwd_entry.place(x=420, y=327)

    def log_submit():
        username = login_uname_entry.get()
        password = login_pwd_entry.get()
        user_type = loginch.get()
        if not username or not password or not user_type:
            ctk.CTkLabel(login_rframe, text="Please fill all fields!", fg_color="#DCE9DC").pack(pady=5)
            return
        else:
            logged_In = db.login(user_type, username, password)
            if logged_In:
                ctk.CTkLabel(login_rframe, text="Logged in!", fg_color="#DCE9DC").pack(pady=5)

    ctk.CTkButton(
        login_rframe,
        text="Submit",
        command=log_submit,
        fg_color="#7ed957",
        text_color="black",
        hover_color="#99D980",
        font=("Arial", 16, "bold")
    ).place(x=280, y=400)   

    ctk.CTkButton(
        login,
        text="Back",
        command=lambda: show_frame(main_frame),
        width=100,
        height=40,
        fg_color="tomato",
        text_color="black",
        hover_color="#FC846F",
        bg_color="#ffde59",
        font=("Arial", 16, "bold")
    ).place(x=80,y=80)


    
    
    # ---------------- REGISTER SCREEN ----------------

    register_frame = ctk.CTkFrame(container, fg_color="#ffde59", bg_color="white", width=800, height=600)
    register_frame.grid(row=0, column=0, sticky="nsew",padx=40, pady=40)
    register_frame.grid_rowconfigure(0, weight=1)
    register_frame.grid_columnconfigure(0, weight=1)


    ctk.CTkLabel(
        register_frame,
        text="User Registration",
        font=("Arial",56,"bold"),
        text_color="black"
    ).place(x=800,y=80)

    ctk.CTkLabel(register_frame, text="Username:", text_color="black",font=("Arial",29)).place(x=200,y=150)
    register_uname_entry = ctk.CTkEntry(register_frame, width=250)
    register_uname_entry.place(x=370,y=153)

    ctk.CTkLabel(register_frame, text="Password:", text_color="black",font=("Arial",29)).place(x=200,y=230)
    register_pwd_entry = ctk.CTkEntry(register_frame, show="*", width=250)
    register_pwd_entry.place(x=370,y=233)

    ctk.CTkLabel(register_frame,text="Confirm Password:", text_color="black",font=("Arial",29)).place(x=670,y=230)
    confirm_entry = ctk.CTkEntry(register_frame,show="*", width=250)
    confirm_entry.place(x=920,y=233)

    ctk.CTkLabel(register_frame,text="Email:", text_color="black",font=("Arial",29)).place(x=200,y=310)
    email_entry = ctk.CTkEntry(register_frame, width=250)
    email_entry.place(x=370,y=313)

    ctk.CTkLabel(register_frame,text="Phone:", text_color="black",font=("Arial",29)).place(x=670,y=310)
    phone_entry = ctk.CTkEntry(register_frame, width=100)
    phone_entry.place(x=780,y=313)

    ctk.CTkLabel(register_frame,text="Address:", text_color="black",font=("Arial",29)).place(x=200,y=390)
    address_entry = ctk.CTkEntry(register_frame, width=800)
    address_entry.place(x=370,y=393)

    ctk.CTkLabel(register_frame,text="Date of Birth:", text_color="black",font=("Arial",29)).place(x=200,y=470)
    dob_entry = ctk.CTkEntry(register_frame, width=80)
    dob_entry.place(x=370,y=473)
    ctk.CTkLabel(register_frame,text="(YYYY-MM-DD)", text_color="black",font=("Arial",22)).place(x=200,y=510)

    ctk.CTkLabel(register_frame,text="Gender:", text_color="black",font=("Arial",29)).place(x=200,y=570)
    gender_entry = ctk.CTkEntry(register_frame, width=250)
    gender_entry.place(x=370,y=573)

    

    def reg_submit():
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
        if pwd_check:
            ctk.CTkLabel(register_frame, text="Passwords do not match!", fg_color="#b3e6d8").place(x=100,y=280)
        elif email_check:
            ctk.CTkLabel(register_frame, text="Invalid email!", fg_color="#b3e6d8").place(x=100,y=280)
        elif phone_check:
            ctk.CTkLabel(register_frame, text="Invalid phone number!", fg_color="#b3e6d8").place(x=100,y=280)
        else:
            registered = db.register(username, password, email, phone, address, gender, dob)
            if registered:
                ctk.CTkLabel(register_frame, text="Registered!", fg_color="#b3e6d8").place(x=100,y=280)
            else:
                ctk.CTkLabel(register_frame, text="Username already exists!", fg_color="#b3e6d8").place(x=100,y=280)

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
    ).place(x=800,y=500)

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

    # Home buttons               - WHY ARE THESE HERE?
    ctk.CTkButton(
        right_frame,
        text="Login",
        width=300,
        height=80,
        fg_color="#fbe58c",
        hover_color="#FCCD77",
        text_color="black",
        font=("Arial", 41),
        command=lambda: show_frame(login)
    ).place(x=150,y=200)

    ctk.CTkButton(
        right_frame,
        text="Register",
        width=300,
        height=80,
        fg_color="#fbe58c",
        hover_color="#FCCD77",
        text_color="black",
        font=("Arial", 41),
        command=lambda: show_frame(register_frame)
    ).place(x=150,y=350)

    # Start on home
    show_frame(main_frame)
    
    

    app.mainloop()


if __name__ == "__main__":
    main()