import tkinter as tk
from db import add_data

def show_frame(frame):
    frame.tkraise()

def main():
    root = tk.Tk()
    root.title("Cat-Nip")
    root.geometry("800x600")

    # Main container holding all screens
    container = tk.Frame(root)
    container.pack(fill="both", expand=True)

    container.grid_rowconfigure(0, weight=1)
    container.grid_columnconfigure(0, weight=1)


    # ---------------- HOME SCREEN ----------------
    main_frame = tk.Frame(container, bg="white")
    main_frame.grid(row=0, column=0, sticky="nsew")

    # Use grid instead of pack
    main_frame.grid_columnconfigure(0, weight=1)
    main_frame.grid_columnconfigure(1, weight=1)
    main_frame.grid_rowconfigure(0, weight=1)

    left_frame = tk.Frame(main_frame, bg="#804000")
    left_frame.grid(row=0, column=0, sticky="nsew")

    right_frame = tk.Frame(main_frame, bg="#e6ccb3")
    right_frame.grid(row=0, column=1, sticky="nsew")

    tk.Label(
        left_frame,
        text="Cat-Nip",
        fg="white",
        bg="#804000",
        font=("Arial", 24)
    ).pack(pady=40)

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
    ch=tk.StringVar()
    tk.Radiobutton(lframe, text="User", variable=ch, value="user").pack(pady=10)
    tk.Radiobutton(lframe, text="Employee", variable=ch, value="employee").pack(pady=10)
    tk.Radiobutton(lframe, text="Admin", variable=ch, value="admin").pack(pady=10)
   
    tk.Button(
        login,
        text="Back",
        command=lambda: show_frame(main_frame)
    ).place(x=10,y=10)


    # ---------------- REGISTER SCREEN ----------------
    register = tk.Frame(container, bg="#b3e6d8")
    register.grid(row=0,column=0,sticky="nsew")

    tk.Label(
        register,
        text="Register",
        font=("Arial",24),
        bg="#b3e6d8"
    ).pack(pady=50)

    tk.Button(
        register,
        text="Back",
        command=lambda: show_frame(main_frame)
    ).place(x=10,y=10)


    # ---------------- USER SCREEN ----------------
    

    def submit():
        username = username_entry.get()
        password = pwd_entry.get()
        add_data("login_det", (username, password))

    

    

    tk.Label(
        rframe,
        text="Username:",
        bg="#E90B0B"
    ).place(x=270,y=160)

    username_entry = tk.Entry(rframe)
    username_entry.pack(pady=20)

    tk.Label(
        rframe,
        text="Password:",
        bg="#e61a1a"
    ).place(x=270,y=220)
    pwd_entry = tk.Entry(rframe, show="*")
    pwd_entry.pack(pady=20)
    
    tk.Button(
        rframe, 
        text="Submit", 
        command=submit
        ).pack()




    # ---------------- EMPLOYEE SCREEN ----------------
    
    
    


    

    
    # ---------------- ADMIN SCREEN ----------------
    

    
    

    

    # Start with home page
    show_frame(main_frame)

    root.mainloop()


if __name__ == "__main__":
    main()