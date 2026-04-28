import customtkinter as ctk
import db
import re
from PIL import Image, ImageTk

def show_frame(frame):
    frame.tkraise()


def main():
    root = ctk.CTk()
    root.title("Cat-Nip")
    root.geometry("800x600")
    root.state("zoomed")

    # App icon
    Icon = ctk.CTkImage(Image.open("assets/catnipico.png"), size=(600, 500))
    img_label = ctk.CTkLabel(root, image=Icon, text="")

    # Main container
    container = ctk.CTkFrame(root)
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
    left_frame.grid(row=0, column=0, sticky="nsew", pady=30)

    right_frame = ctk.CTkFrame(main_frame, fg_color="#ffe683", width=400, height=600)
    right_frame.grid(row=0, column=1, sticky="nsew", pady=30)

    # Keep image reference
    Icon = Image.open("assets/catnipico.png")
    Icon = Icon.resize((600, 500))
    Icon = ImageTk.PhotoImage(Icon)
    img_label = ctk.CTkLabel(left_frame, image=Icon, fg_color="#ffde59")
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

    lframe = ctk.CTkFrame(login, fg_color="#ffde59",width=400, height=600)
    lframe.grid(row=0, column=0, sticky="nsew", pady=20)

    rframe = ctk.CTkFrame(login, fg_color="white", width=400, height=600)
    rframe.grid(row=0, column=1, sticky="nsew", pady=20)

    ctk.CTkLabel(lframe, text="Cat-Nip", fg_color="#ffde59", font=("Arial", 54, "bold")).pack(pady=10)

    # User type radio buttons
    ch = ctk.StringVar()
    ch.set("user")
    ctk.CTkRadioButton(
        lframe, text="User",
        variable=ch, value="user",
        fg_color="#f9b746",
        font=("Arial", 24, "bold")
    ).place(x=250, y=200)

    ctk.CTkRadioButton(
        lframe, text="Employee",
        variable=ch, value="employee",
        fg_color="#f9b746",
        font=("Arial", 24, "bold")
    ).place(x=250, y=300)

    ctk.CTkRadioButton(
        lframe, text="Admin",
        variable=ch, value="admin",
        fg_color="#f9b746",
        font=("Arial", 24, "bold")
    ).place(x=250, y=400)

    # Login fields
    ctk.CTkLabel(rframe, text="Username:", fg_color="#ffe683", font=("Arial", 16, "bold")).place(x=300, y=250)
    login_uname_entry = ctk.CTkEntry(rframe, width=50)
    login_uname_entry.place(x=200, y=280)

    ctk.CTkLabel(rframe, text="Password:", fg_color="#ffe683", font=("Arial", 16, "bold")).place(x=300, y=330)
    login_pwd_entry = ctk.CTkEntry(rframe, show="*", width=50)
    login_pwd_entry.place(x=200, y=360)

    def log_submit():
        username = login_uname_entry.get()
        password = login_pwd_entry.get()
        user_type = ch.get()
        if not username or not password or not user_type:
            ctk.CTkLabel(rframe, text="Please fill all fields!", fg_color="#DCE9DC").pack(pady=5)
            return
        else:
            logged_In = db.login(user_type, username, password)
            if logged_In:
                ctk.CTkLabel(rframe, text="Logged in!", fg_color="#DCE9DC").pack(pady=5)

    ctk.CTkButton(
        rframe,
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
        fg_color="tomato",
        font=("Arial", 16, "bold"),
        
    ).place(x=30,y=30)


    # ---------------- REGISTER SCREEN ----------------
    

    register_frame = ctk.CTkFrame(container, fg_color="#b3e6d8")
    register_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
    #registerbackground
    
    ctk.CTkLabel(register_frame, text="User Registration", fg_color="#b3e6d8", font=("Arial", 56, "bold")).place(x=750, y=50)

    ctk.CTkLabel(register_frame, text="Username:", fg_color="#E6E0E0").place(x=500, y=150)
    register_uname_entry = ctk.CTkEntry(register_frame)
    register_uname_entry.place(x=500, y=180)

    ctk.CTkLabel(register_frame, text="Password:", fg_color="#E6E0E0").place(x=500, y=230)
    register_pwd_entry = ctk.CTkEntry(register_frame, show="*")
    register_pwd_entry.place(x=500, y=260)
    
    ctk.CTkLabel(register_frame, text="Confirm Password:", fg_color="#E6E0E0").place(x=500, y=310)
    confirm_entry = ctk.CTkEntry(register_frame, show="*")
    confirm_entry.place(x=500, y=340)
    ctk.CTkLabel(register_frame, text="Email:", fg_color="#E6E0E0").place(x=500, y=390)
    email_entry = ctk.CTkEntry(register_frame)
    email_entry.place(x=500, y=420)
    ctk.CTkLabel(register_frame, text="Phone:", fg_color="#E6E0E0").place(x=500, y=470)
    phone_entry = ctk.CTkEntry(register_frame)
    phone_entry.place(x=500, y=500)
    ctk.CTkLabel(register_frame, text="Address:", fg_color="#E6E0E0").place(x=500, y=550)
    address_entry = ctk.CTkEntry(register_frame)
    address_entry.place(x=500, y=580)
    ctk.CTkLabel(register_frame, text="Gender:", fg_color="#E6E0E0").place(x=500, y=620)
    gender_entry = ctk.CTkEntry(register_frame)
    gender_entry.place(x=500, y=650)
    ctk.CTkLabel(register_frame, text="Date of Birth:", fg_color="#E6E0E0").place(x=500, y=520)
    dob_entry = ctk.CTkEntry(register_frame)
    dob_entry.place(x=500, y=500)
    

    ctk.CTkLabel(
        register_frame,
        text="Register ",
        font=("Arial",24),
        fg_color="#b3e6d8"
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
        command=reg_submit
    ).place(x=100,y=300)

    ctk.CTkButton(
        register_frame,
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

    root.mainloop()


if __name__ == "__main__":
    main()