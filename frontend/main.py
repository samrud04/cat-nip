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
        text="Start",
        width=15,
        height=2,
        command=lambda: show_frame(secondscreen)
    ).pack(pady=20)

    # ---------------- Second Screen ----------------
    secondscreen = tk.Frame(container, bg="#b3e6d8")
    secondscreen.grid(row=0, column=0, sticky="nsew")

    tk.Label(
        secondscreen,
        text="Second Screen",
        bg="#b3e6d8",
        font=("Arial", 24)
    ).pack(pady=50)

    tk.Button(
        secondscreen,
        text="Back",
        command=lambda: show_frame(main_frame)
    ).pack()

    # Start on first screen
    show_frame(main_frame)

    root.mainloop()

if __name__ == "__main__":
    main()