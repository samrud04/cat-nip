import tkinter as tk
import db
import re
from PIL import Image, ImageTk

def show_frame(frame):
    frame.tkraise()


def main():
    root = tk.Tk()
    root.title("Cat-Nip")
    root.geometry("800x600")
    root.state("zoomed")

    # App icon
    photo = tk.PhotoImage(file="assets/catnipico.png")
    soto = photo.subsample(4,4)

    root.iconphoto(False, soto)

    # Main container
    container = tk.Frame(root)
    container.pack(fill="both", expand=True)

    container.grid_rowconfigure(0, weight=1)
    container.grid_columnconfigure(0, weight=1)


    # ---------------- HOME SCREEN ----------------
    main_frame = tk.Frame(container, bg="white")
    main_frame.grid(row=0, column=0, sticky="nsew")

    main_frame.grid_columnconfigure(0, weight=1)
    main_frame.grid_columnconfigure(1, weight=1)
    main_frame.grid_rowconfigure(0, weight=1)

    left_frame = tk.Frame(main_frame, bg="#ffde59", width=600, height=600, bd=20, pady=30, highlightbackground="white", highlightthickness=20)
    left_frame.grid(row=0, column=0, sticky="nsew")

    right_frame = tk.Frame(main_frame, bg="#ffe683", width=400, height=600, bd=20, pady=30, highlightbackground="white", highlightthickness=20)
    right_frame.grid(row=0, column=1, sticky="nsew")

    # Keep image reference
    Icon = Image.open("assets/catnipico.png")
    Icon = Icon.resize((600, 500))
    Icon = ImageTk.PhotoImage(Icon)
    img_label = tk.Label(left_frame, image=Icon, bg="#ffde59")
    img_label.image = Icon
    img_label.place(x=80, y=160)

    tk.Label(
        left_frame,
        text="Cat-Nip",
        fg="black",
        bg="#ffde59",
        font=("Arial", 54, "bold")
    ).pack(pady=40)


    # ---------------- LOGIN SCREEN ----------------
    login = tk.Frame(container, bg="white")
    login.grid(row=0, column=0, sticky="nsew")

    login.grid_columnconfigure(0, weight=1)
    login.grid_columnconfigure(1, weight=1)
    login.grid_rowconfigure(0, weight=1)

    lframe = tk.Frame(login, bg="#ffde59",width=400, height=600, bd=20, pady=20, highlightbackground="white", highlightthickness=20)
    lframe.grid(row=0, column=0, sticky="nsew")

    rframe = tk.Frame(login, bg="white", width=400, height=600, bd=20, pady=20)
    rframe.grid(row=0, column=1, sticky="nsew")

    tk.Label(lframe, text="Cat-Nip", bg="#ffde59", font=("Arial", 54, "bold")).pack(pady=10)

    # User type radio buttons
    ch = tk.StringVar()

    tk.Radiobutton(
        lframe, text="User",
        variable=ch, value="user",
        bg="#f9b746",
        font=("Arial", 24, "bold")
    ).place(x=250, y=200)

    tk.Radiobutton(
        lframe, text="Employee",
        variable=ch, value="employee",
        bg="#f9b746",
        font=("Arial", 24, "bold")
    ).place(x=250, y=300)

    tk.Radiobutton(
        lframe, text="Admin",
        variable=ch, value="admin",
        bg="#f9b746",
        font=("Arial", 24, "bold")
    ).place(x=250, y=400)

    # Login fields
    tk.Label(rframe, text="Username:", bg="#ffe683", font=("Arial", 16, "bold")).place(x=300, y=250)
    login_uname_entry = tk.Entry(rframe, width=50)
    login_uname_entry.place(x=200, y=280)

    tk.Label(rframe, text="Password:", bg="#ffe683", font=("Arial", 16, "bold")).place(x=300, y=330)
    login_pwd_entry = tk.Entry(rframe, show="*", width=50)
    login_pwd_entry.place(x=200, y=360)

    def log_submit():
        username = login_uname_entry.get()
        password = login_pwd_entry.get()
        user_type = ch.get()
        if not username or not password or not user_type:
            tk.Label(rframe, text="Please fill all fields!", bg="#DCE9DC").pack(pady=5)
            return
        else:
            logged_In = db.login(user_type, username, password)
            if logged_In:
                tk.Label(rframe, text="Logged in!", bg="#DCE9DC").pack(pady=5)

    tk.Button(
        rframe,
        text="Submit",
        command=log_submit,
        bg="#7ed957",
        fg="black",
        font=("Arial", 16, "bold")
    ).place(x=300, y=450)   

    tk.Button(
        login,
        text="Back",
        command=lambda: show_frame(main_frame)
    ).place(x=10,y=10)


    # ---------------- REGISTER SCREEN ----------------
    register = tk.Frame(container, bg="#b3e6d8")
    register.grid(row=0, column=0, sticky="nsew")
    #registerbackground
    
    tk.Label(register, text="Username:", bg="#E6E0E0").pack(pady=5)
    register_uname_entry = tk.Entry(register)
    register_uname_entry.pack(pady=10)

    tk.Label(register, text="Password:", bg="#E6E0E0").pack(pady=5)
    register_pwd_entry = tk.Entry(register, show="*")
    register_pwd_entry.pack(pady=10)
    tk.Label(register, text="Confirm Password:", bg="#E6E0E0").pack(pady=5)
    confirm_entry = tk.Entry(register, show="*")
    confirm_entry.pack(pady=10)
    tk.Label(register, text="Email:", bg="#E6E0E0").pack(pady=5)
    email_entry = tk.Entry(register)
    email_entry.pack(pady=10)
    tk.Label(register, text="Phone:", bg="#E6E0E0").pack(pady=5)
    phone_entry = tk.Entry(register)
    phone_entry.pack(pady=10)
    tk.Label(register, text="Address:", bg="#E6E0E0").pack(pady=5)
    address_entry = tk.Entry(register)
    address_entry.pack(pady=10)
    tk.Label(register, text="Gender:", bg="#E6E0E0").pack(pady=5)
    gender_entry = tk.Entry(register)
    gender_entry.pack(pady=10)
    tk.Label(register, text="Date of Birth:", bg="#E6E0E0").pack(pady=5)
    dob_entry = tk.Entry(register)
    dob_entry.pack(pady=10)
    

    tk.Label(
        register,
        text="Register ",
        font=("Arial",24),
        bg="#b3e6d8"
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
            tk.Label(register, text="Passwords do not match!", bg="#b3e6d8").place(x=100,y=280)
        elif email_check:
            tk.Label(register, text="Invalid email!", bg="#b3e6d8").place(x=100,y=280)
        elif phone_check:
            tk.Label(register, text="Invalid phone number!", bg="#b3e6d8").place(x=100,y=280)
        else:
            registered = db.register(username, password, email, phone, address, gender, dob)
            if registered:
                tk.Label(register, text="Registered!", bg="#b3e6d8").place(x=100,y=280)
            else:
                tk.Label(register, text="Username already exists!", bg="#b3e6d8").place(x=100,y=280)
    
    tk.Button(
        register,
        text="Submit",
        command=reg_submit
    ).place(x=100,y=300)

    tk.Button(
        register,
        text="Back",
        command=lambda: show_frame(main_frame)
    ).place(x=10,y=10)

    # Home buttons               - WHY ARE THESE HERE?
    tk.Button(
        right_frame,
        text="Login",
        width=25,
        height=5,
        bg="#b3e6d8",
        command=lambda: show_frame(login)
    ).place(x=280,y=150)

    tk.Button(
        right_frame,
        text="Register",
        width=25,
        height=5,
        bg="#b3e6d8",
        command=lambda: show_frame(register)
    ).place(x=280,y=300)

    # Start on home
    show_frame(main_frame)

    root.mainloop()


if __name__ == "__main__":
    main()