import tkinter as tk
from db import add_data
from pillow import Image, ImageTk
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
    login = tk.Frame(container, bg="#e61f1f")
    login.grid(row=0, column=0, sticky="nsew")

    login.grid_columnconfigure(0, weight=1)
    login.grid_columnconfigure(1, weight=1)
    login.grid_rowconfigure(0, weight=1)

    lframe = tk.Frame(login, bg="#EA7A0A")
    lframe.grid(row=0, column=0, sticky="nsew")

    rframe = tk.Frame(login, bg="#040404")
    rframe.grid(row=0, column=1, sticky="nsew")

    # User type radio buttons
    ch = tk.StringVar()

    tk.Radiobutton(
        lframe, text="User",
        variable=ch, value="user"
    ).pack(pady=10)

    tk.Radiobutton(
        lframe, text="Employee",
        variable=ch, value="employee"
    ).pack(pady=10)

    tk.Radiobutton(
        lframe, text="Admin",
        variable=ch, value="admin"
    ).pack(pady=10)

    # Login fields
    tk.Label(rframe, text="Username:", bg="#E6E0E0").pack(pady=5)
    username_entry = tk.Entry(rframe)
    username_entry.pack(pady=10)

    tk.Label(rframe, text="Password:", bg="#DCE9DC").pack(pady=5)
    pwd_entry = tk.Entry(rframe, show="*")
    pwd_entry.pack(pady=10)

    def submit():
        username = username_entry.get()
        password = pwd_entry.get()

        add_data("login_det", (username, password))
        print("Saved!")

    tk.Button(
        rframe,
        text="Submit",
        command=submit
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
    bag=Image.open("assets/regbg.png")
    bag=bag.resize((800,600),Image.ANTIALIAS)
    bag=ImageTk.PhotoImage(bag)
    bg_label=tk.Label(register,image=bag)
    bg_label.place(x=0,y=0,relwidth=1,relheight=1)
    
    tk.Label(register, text="Username:", bg="#E6E0E0").pack(pady=5)
    username_entry = tk.Entry(register)
    username_entry.pack(pady=10)

    tk.Label(register, text="Password:", bg="#E6E0E0").pack(pady=5)
    password_entry = tk.Entry(register, show="*")
    password_entry.pack(pady=10)
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

    

    tk.Button(
        register,
        text="Submit"
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