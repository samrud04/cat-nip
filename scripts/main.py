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

    left_frame = ctk.CTkFrame(main_frame, fg_color="#ffde59", width=600, height=600)
    left_frame.grid(row=0, column=0, sticky="nsew", padx=30, pady=30)

    right_frame = ctk.CTkFrame(main_frame, fg_color="#ffffff", width=100, height=600)
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
    login = ctk.CTkFrame(container, fg_color="white", width=800, height=600)
    login.grid(row=0, column=0, sticky="nsew")

    login.grid_columnconfigure(0, weight=1)
    login.grid_columnconfigure(1, weight=1)
    login.grid_rowconfigure(0, weight=1)

    login_lframe = ctk.CTkFrame(login, fg_color="#ffde59",width=400, height=300)
    login_lframe.grid(row=0, column=0, sticky="nsew",padx=40, pady=40)

    login_rframe = ctk.CTkFrame(login, fg_color="#ffea00", width=100, height=600)
    login_rframe.grid(row=0, column=1, sticky="nsew",padx=40, pady=40)

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
    ctk.CTkLabel(login_rframe, text="Username:", fg_color="#ffea00", font=("Arial", 16, "bold")).place(x=150, y=180)
    login_uname_entry = ctk.CTkEntry(login_rframe, width=150)
    login_uname_entry.place(x=250, y=180)

    ctk.CTkLabel(login_rframe, text="Password:", fg_color="#ffea00", font=("Arial", 16, "bold")).place(x=150, y=260)
    login_pwd_entry = ctk.CTkEntry(login_rframe, show="*", width=150)
    login_pwd_entry.place(x=250, y=260)

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
        
    ).place(x=200, y=350)   

    ctk.CTkButton(
        login,
        text="Back",
        command=lambda: show_frame(main_frame),
        fg_color="green",
        font=("Arial", 16, "bold")
    ).place(x=30,y=30)


    
    
    # ---------------- REGISTER SCREEN ----------------

    register_frame = ctk.CTkFrame(container, fg_color="#ffea00", width=800, height=600)
    register_frame.grid(row=0, column=0, sticky="nsew")
    register_frame.grid_rowconfigure(0, weight=1)
    register_frame.grid_columnconfigure(0, weight=1)


    
    ctk.CTkLabel(
        register_frame,
        text="User Registration",
        font=("Arial",56,"bold")
    ).place(x=350,y=50)

    ctk.CTkLabel(register_frame, text="Username:", text_color="black").place(x=100,y=150)
    register_uname_entry = ctk.CTkEntry(register_frame)
    register_uname_entry.place(x=250,y=150)

    ctk.CTkLabel(register_frame, text="Password:", text_color="black").place(x=100,y=200)
    register_pwd_entry = ctk.CTkEntry(register_frame, show="*")
    register_pwd_entry.place(x=250,y=200)

    ctk.CTkLabel(register_frame,text="Confirm Password:", text_color="black").place(x=400,y=200)
    confirm_entry = ctk.CTkEntry(register_frame,show="*")
    confirm_entry.place(x=450,y=200)

    ctk.CTkLabel(register_frame,text="Email:", text_color="black").place(x=100,y=250)
    email_entry = ctk.CTkEntry(register_frame)
    email_entry.place(x=250,y=250)

    ctk.CTkLabel(register_frame,text="Phone:", text_color="black").place(x=400,y=250)
    phone_entry = ctk.CTkEntry(register_frame)
    phone_entry.place(x=450,y=250)

    ctk.CTkLabel(register_frame,text="Address:", text_color="black").place(x=100,y=300)
    address_entry = ctk.CTkEntry(register_frame, width=400)
    address_entry.place(x=250,y=300)

    ctk.CTkLabel(register_frame,text="Date of Birth:", text_color="black").place(x=100,y=350)
    dob_entry = ctk.CTkEntry(register_frame)
    dob_entry.place(x=250,y=350)
    ctk.CTkLabel(register_frame,text="(YYYY-MM-DD)", text_color="black").place(x=400,y=350)

    ctk.CTkLabel(register_frame,text="Gender:", text_color="black").place(x=100,y=400)
    gender_entry = ctk.CTkEntry(register_frame)
    gender_entry.place(x=250,y=400)

    

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
        command=reg_submit,fg_color="#7ed957",font=("Arial", 16, "bold")    
    ).place(x=450,y=400)

    ctk.CTkButton(
        register_frame,
        text="Back",
        command=lambda: show_frame(main_frame)
    ).place(x=10,y=10)

    # Home buttons               - WHY ARE THESE HERE?
    ctk.CTkButton(
        right_frame,
        text="Login",
        width=200,
        height=70,
        fg_color="#f9b746",
        command=lambda: show_frame(login)
    ).place(x=200,y=150)

    ctk.CTkButton(
        right_frame,
        text="Register",
        width=200,
        height=70,
        fg_color="#f9b746",
        command=lambda: show_frame(register_frame)
    ).place(x=200,y=300)

    # Start on home
    show_frame(main_frame)
    
    

    app.mainloop()


if __name__ == "__main__":
    main()