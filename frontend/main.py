import tkinter as tk

def show_frame(frame):
    frame.tkraise()

def main():
    root = tk.Tk()
    root.title("Cat-Nip")
    root.geometry("800x600")

    # Container for all screens
    container = tk.Frame(root)
    container.pack(fill="both", expand=True)

    # Make grid expand to fill window
    container.grid_rowconfigure(0, weight=1)
    container.grid_columnconfigure(0, weight=1)

    # ---------------- First Screen ----------------
    main_frame = tk.Frame(container, bg="white")
    main_frame.grid(row=0, column=0, sticky="nsew")

    left_frame = tk.Frame(main_frame, bg="#804000", width=400)
    left_frame.pack(side="left", fill="both")
    left_frame.pack_propagate(False)

    right_frame = tk.Frame(main_frame, bg="#e6ccb3")
    right_frame.pack(side="right", fill="both", expand=True)

    tk.Label(
        left_frame,
        text="Cat-Nip",
        fg="white",
        bg="#804000",
        font=("Arial", 24)
    ).pack(pady=40)

    tk.Button(
        main_frame,
        text="login",
        width=15,
        height=2,
        command=lambda: show_frame(login)
    ).pack(pady=20)

    tk.Button(
        main_frame,
        text="register",
        width=15,
        height=2,
        command=lambda: show_frame(register)
    ).pack(pady=20)


    # ---------------- Second Screen ----------------
    login  = tk.Frame(container, bg="#b3e6d8")
    login.grid(row=0, column=0, sticky="nsew")
    left_frame = tk.Frame(login, bg="#804000", width=400)
    left_frame.pack(side="left", fill="both")
    left_frame.pack_propagate(False)

    right_frame = tk.Frame(login, bg="#e6ccb3")
    right_frame.pack(side="right", fill="both", expand=True)

    tk.Label(
        login,
        text="Login",
        bg="#b3e6d8",
        font=("Arial", 24)
    ).pack(pady=50)

    tk.Button(
        login,
        text="Back",
        command=lambda: show_frame(main_frame)
    ).pack(pady=20)
    register = tk.Frame(container, bg="#b3e6d8")
    register.grid(row=0, column=0, sticky="nsew")
    left_frame = tk.Frame(register, bg="#804000", width=400)
    left_frame.pack(side="left", fill="both")
    left_frame.pack_propagate(False)

    right_frame = tk.Frame(register, bg="#e6ccb3")
    right_frame.pack(side="right", fill="both", expand=True)
    tk.Label(
        register,
        text="Register",
        bg="#b3e6d8",
        font=("Arial", 24)
    ).pack(pady=50)
    tk.Button(
        register,
        text="Back",
        command=lambda: show_frame(main_frame)
    ).pack(pady=20)

     # Start on first screen

    show_frame(main_frame)

    root.mainloop()

if __name__ == "__main__":
    main()