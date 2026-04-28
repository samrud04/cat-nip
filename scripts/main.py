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
    Icon = ctk.CTkImage(Image.open("assets/catnipico.png"), size=(600, 500))

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

    left_frame = ctk.CTkFrame(main_frame, fg_color="#ffde59", width=600, height=600)
    left_frame.grid(row=0, column=0, sticky="nsew", padx=30, pady=30)

    right_frame = ctk.CTkFrame(main_frame, fg_color="#ffe683", width=100, height=600)
    right_frame.grid(row=0, column=1, sticky="nsew", padx=30, pady=30)

    img_label = ctk.CTkLabel(left_frame, text="",image=Icon, fg_color="#ffde59")
    img_label.image = Icon
    img_label.place(x=80, y=160)

    ctk.CTkLabel(
        left_frame,
        text="Cat-Nip",
        text_color="black",
        fg_color="#ffde59",
        font=("Arial", 54, "bold")
    ).pack(pady=40)


    # ---------------- LOGIN SCREEN ----------------
    login = ctk.CTkFrame(container, fg_color="white")
    login.grid(row=0, column=0, sticky="nsew")

    login.grid_columnconfigure(0, weight=1)
    login.grid_columnconfigure(1, weight=1)
    login.grid_rowconfigure(0, weight=1)

    login_lframe = ctk.CTkFrame(login, fg_color="#ffde59",width=400, height=600)
    login_lframe.grid(row=0, column=0, sticky="nsew", pady=20)

    login_rframe = ctk.CTkFrame(login, fg_color="white", width=400, height=600)
    login_rframe.grid(row=0, column=1, sticky="nsew", pady=20)

    ctk.CTkLabel(login_lframe, text="Cat-Nip", fg_color="#ffde59", font=("Arial", 54, "bold")).pack(pady=10)

    # User type radio buttons
    loginch = ctk.StringVar()
    loginch.set("user")
    ctk.CTkRadioButton(
        login_lframe, text="User",
        variable=loginch, value="user",
        fg_color="#f9b746",
        text_color="black",
        font=("Arial", 24, "bold")
    ).place(x=250, y=200)

    ctk.CTkRadioButton(
        login_lframe, text="Employee",
        variable=loginch, value="employee",
        fg_color="#f9b746",
        text_color="black",
        font=("Arial", 24, "bold")
    ).place(x=250, y=300)

    ctk.CTkRadioButton(
        login_lframe, text="Admin",
        variable=loginch, value="admin",
        fg_color="#f9b746",
        text_color="black",
        font=("Arial", 24, "bold")
    ).place(x=250, y=400)

    # Login fields
    ctk.CTkLabel(login_rframe, text="Username:", fg_color="#ffe683", font=("Arial", 16, "bold")).place(x=300, y=250)
    login_uname_entry = ctk.CTkEntry(login_rframe, width=50)
    login_uname_entry.place(x=200, y=280)

    ctk.CTkLabel(login_rframe, text="Password:", fg_color="#ffe683", font=("Arial", 16, "bold")).place(x=300, y=330)
    login_pwd_entry = ctk.CTkEntry(login_rframe, show="*", width=50)
    login_pwd_entry.place(x=200, y=360)

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
        font=("Arial", 16, "bold"),
        
    ).place(x=300, y=450)   

    ctk.CTkButton(
        login,
        text="Back",
        command=lambda: show_frame(main_frame),
        fg_color="green",
        font=("Arial", 16, "bold")
    ).place(x=30,y=30)


    
    
    # ---------------- REGISTER SCREEN ----------------

    register_frame = ctk.CTkFrame(container, fg_color="#b3e6d8")
    register_frame.grid(row=0, column=0, sticky="nsew")
    register_frame.grid_rowconfigure(0, weight=1)
    register_frame.grid_columnconfigure(0, weight=1)


    scrollable_frame = ctk.CTkScrollableFrame(
        register_frame,
        fg_color="#b3e6d8"
    )
    scrollable_frame.grid(row=0,column=0,sticky="nsew")
    ctk.CTkLabel(
        scrollable_frame,
        text="User Registration",
        font=("Arial",56,"bold")
    ).pack(pady=40)

    ctk.CTkLabel(scrollable_frame, text="Username:", text_color="black").pack(pady=5)
    register_uname_entry = ctk.CTkEntry(scrollable_frame)
    register_uname_entry.pack(pady=5)

    ctk.CTkLabel(scrollable_frame, text="Password:", text_color="black").pack(pady=5)
    register_pwd_entry = ctk.CTkEntry(scrollable_frame, show="*")
    register_pwd_entry.pack(pady=5)

    ctk.CTkLabel(scrollable_frame,text="Confirm Password:", text_color="black").pack(pady=5)
    confirm_entry = ctk.CTkEntry(scrollable_frame,show="*")
    confirm_entry.pack(pady=5)

    ctk.CTkLabel(scrollable_frame,text="Email:", text_color="black").pack(pady=5)
    email_entry = ctk.CTkEntry(scrollable_frame)
    email_entry.pack(pady=5)

    ctk.CTkLabel(scrollable_frame,text="Phone:", text_color="black").pack(pady=5)
    phone_entry = ctk.CTkEntry(scrollable_frame)
    phone_entry.pack(pady=5)

    ctk.CTkLabel(scrollable_frame,text="Address:", text_color="black").pack(pady=5)
    address_entry = ctk.CTkEntry(scrollable_frame)
    address_entry.pack(pady=5)

    ctk.CTkLabel(scrollable_frame,text="Date of Birth:", text_color="black").pack(pady=5)
    dob_entry = ctk.CTkEntry(scrollable_frame)
    dob_entry.pack(pady=5)

    ctk.CTkLabel(scrollable_frame,text="Gender:", text_color="black").pack(pady=5)
    gender_entry = ctk.CTkEntry(scrollable_frame)
    gender_entry.pack(pady=5)

    ctk.CTkLabel(
        scrollable_frame,
        text="Register ",
        font=("Arial",24),
        fg_color="#b3e6d8",
        text_color="black"
    ).place(x=100,y=50)

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
            ctk.CTkLabel(scrollable_frame, text="Passwords do not match!", fg_color="#b3e6d8").place(x=100,y=280)
        elif email_check:
            ctk.CTkLabel(scrollable_frame, text="Invalid email!", fg_color="#b3e6d8").place(x=100,y=280)
        elif phone_check:
            ctk.CTkLabel(scrollable_frame, text="Invalid phone number!", fg_color="#b3e6d8").place(x=100,y=280)
        else:
            registered = db.register(username, password, email, phone, address, gender, dob)
            if registered:
                ctk.CTkLabel(scrollable_frame, text="Registered!", fg_color="#b3e6d8").place(x=100,y=280)
            else:
                ctk.CTkLabel(scrollable_frame, text="Username already exists!", fg_color="#b3e6d8").place(x=100,y=280)

    ctk.CTkButton(
        scrollable_frame,
        text="Submit",
        command=reg_submit
    ).place(x=100,y=300)

    ctk.CTkButton(
        scrollable_frame,
        text="Back",
        command=lambda: show_frame(main_frame)
    ).place(x=10,y=10)

    # Home buttons               - WHY ARE THESE HERE?
    ctk.CTkButton(
        right_frame,
        text="Login",
        width=25,
        height=5,
        fg_color="#f9b746",
        command=lambda: show_frame(login)
    ).place(x=280,y=150)

    ctk.CTkButton(
        right_frame,
        text="Register",
        width=25,
        height=5,
        fg_color="#f9b746",
        command=lambda: show_frame(register_frame)
    ).place(x=280,y=300)

    # Start on home
    show_frame(main_frame)
    
    

    app.mainloop()


if __name__ == "__main__":
    main()