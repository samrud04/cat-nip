import tkinter as tk
from tkcalendar import DateEntry
import db
import re

def show_frame(frame):
    frame.tkraise()


def main():
    root = tk.Tk()
    root.title("Cat-Nip")
    root.geometry("800x600")

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

    left_frame = tk.Frame(main_frame, bg="#804000")
    left_frame.grid(row=0, column=0, sticky="nsew")

    right_frame = tk.Frame(main_frame, bg="#e6ccb3")
    right_frame.grid(row=0, column=1, sticky="nsew")

    # Keep image reference
    img_label = tk.Label(left_frame, image=soto, bg="#804000")
    img_label.image = soto
    img_label.place(x=100, y=200)

    tk.Label(
        left_frame,
        text="Cat-Nip",
        fg="white",
        bg="#804000",
        font=("Arial",24)
    ).pack(pady=40)

    # ---------------- LOGIN SCREEN ----------------
    login = tk.Frame(container, bg="white")
    login.grid(row=0, column=0, sticky="nsew")

    login.grid_columnconfigure(0, weight=1)
    login.grid_columnconfigure(1, weight=1)
    login.grid_rowconfigure(0, weight=1)

    lframe = tk.Frame(login, bg="#ffde59", bd=20, pady=20, highlightbackground="white", highlightthickness=20)
    lframe.grid(row=0, column=0, sticky="nsew")

    rframe = tk.Frame(login, bg="#ffe683", bd=20, pady=20, highlightbackground="white", highlightthickness=20)
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
    tk.Label(rframe, text="Username:", bg="#E6E0E0").pack(pady=5)
    login_uname_entry = tk.Entry(rframe)
    login_uname_entry.pack(pady=10)

    tk.Label(rframe, text="Password:", bg="#DCE9DC").pack(pady=5)
    login_pwd_entry = tk.Entry(rframe, show="*")
    login_pwd_entry.pack(pady=10)

    def log_submit():
        username = login_uname_entry.get()
        password = login_pwd_entry.get()
        user_type = ch.get()
        logged_In = db.login(user_type, username, password)
        if logged_In:
            tk.Label(rframe, text="Logged in!", bg="#DCE9DC").pack(pady=5)

    tk.Button(
        rframe,
        text="Submit",
        command=log_submit
    ).pack(pady=20)

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

    # Home buttons
    tk.Button(
        right_frame,
        text="Login",
        width=15,
        height=2,
        command=lambda: show_frame(login)
    ).pack(pady=30)

    tk.Button(
        right_frame,
        text="Register",
        width=15,
        height=2,
        command=lambda: show_frame(register)
    ).pack(pady=30)

    # Start on home
    show_frame(main_frame)

    root.mainloop()


if __name__ == "__main__":
    main()