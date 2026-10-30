import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import db


def login_screen(container, show_frame, refresh_user_screen):

    # =====================================================
    # LOGIN FRAME
    # =====================================================

    login = ctk.CTkFrame(container, fg_color="#ffe7d6")
    login.grid_columnconfigure(0, weight=1)
    login.grid_columnconfigure(1, weight=1)
    login.grid_rowconfigure(0, weight=1)

    # =====================================================
    # LOGIN HANDLER
    # =====================================================

    def log_submit():
        username = login_uname_entry.get().strip()
        password = login_pwd_entry.get()

        if not username or not password:
            messagebox.showerror(
                "Error",
                "Please fill all fields!"
            )
            return

        # ADMIN LOGIN
        if username == "admin" and password == "admin123":
            login_uname_entry.delete(0, "end")
            login_pwd_entry.delete(0, "end")
            show_frame("admin")
            return

        # NORMAL USER LOGIN
        logged_in = db.login(
            "user",
            username,
            password
        )

        if logged_in:
            user_id = db.get_user_id(username)

            # SAVE CURRENT USER ID
            with open("session.txt", "w") as f:
                f.write(str(user_id))

            # CLEAR LOGIN FIELDS
            login_uname_entry.delete(0, "end")
            login_pwd_entry.delete(0, "end")

            # OPEN USER SCREEN
            refresh_user_screen()

        else:
            messagebox.showerror(
                "Error",
                "Invalid credentials!"
            )

    # =====================================================
    # LEFT PANEL — BRAND / FEATURES
    # =====================================================

    left_frame = ctk.CTkFrame(
        login,
        fg_color="#FA9A85",
        corner_radius=40
    )
    left_frame.grid(
        row=0,
        column=0,
        sticky="nsew",
        padx=(60, 24),
        pady=80
    )
    left_frame.grid_columnconfigure(0, weight=1)

    ctk.CTkButton(
        left_frame,
        text="←",
        command=lambda: show_frame("main"),
        width=48,
        height=48,
        fg_color="#fed9bf",
        text_color="#2b1d14",
        hover_color="#ffc9a3",
        font=("Segoe UI", 25, "bold"),
        corner_radius=24
    ).place(x=24, y=24)

    ctk.CTkLabel(
        left_frame,
        text="🐾",
        text_color="#2b1d14",
        font=("Segoe UI Emoji", 76),
        fg_color="transparent"
    ).pack(pady=(70, 8))

    ctk.CTkLabel(
        left_frame,
        text="Pet Supplies\n& Care",
        text_color="#2b1d14",
        font=("Segoe UI", 38, "bold"),
        justify="center",
        fg_color="transparent"
    ).pack(pady=(0, 26))

    ctk.CTkFrame(
        left_frame,
        width=90,
        height=4,
        fg_color="#fed9bf",
        corner_radius=2
    ).pack(pady=(0, 22))

    features = [
        "✓  Browse Pet Products",
        "✓  Book Grooming Services",
        "✓  Track Your Orders",
        "✓  Manage Your Pets"
    ]

    for feature in features:
        ctk.CTkLabel(
            left_frame,
            text=feature,
            text_color="#2b1d14",
            font=("Segoe UI", 18, "bold"),
            anchor="w",
            fg_color="transparent"
        ).pack(fill="x", padx=42, pady=9)

    ctk.CTkLabel(
        left_frame,
        text="A little care goes a long way.\nWelcome back! 🐾",
        text_color="#fff5f0",
        font=("Segoe UI", 18),
        justify="center",
        fg_color="transparent"
    ).pack(pady=(35, 25))

    # =====================================================
    # RIGHT PANEL — LOGIN FORM
    # =====================================================

    right_frame = ctk.CTkFrame(
        login,
        fg_color="#fca265",
        corner_radius=40
    )
    right_frame.grid(
        row=0,
        column=1,
        sticky="nsew",
        padx=(24, 60),
        pady=80
    )
    right_frame.grid_columnconfigure(0, weight=1)

    ctk.CTkLabel(
        right_frame,
        text="Welcome Back!",
        text_color="#2b1d14",
        font=("Segoe UI", 36, "bold"),
        fg_color="transparent"
    ).pack(pady=(75, 8))

    ctk.CTkLabel(
        right_frame,
        text="Log in to continue to Cat-Nip",
        text_color="#5c4033",
        font=("Segoe UI", 15),
        fg_color="transparent"
    ).pack(pady=(0, 38))

    ctk.CTkLabel(
        right_frame,
        text="Username",
        text_color="#2b1d14",
        font=("Segoe UI", 15, "bold"),
        fg_color="transparent"
    ).pack(anchor="w", padx=55, pady=(8, 7))

    login_uname_entry = ctk.CTkEntry(
        right_frame,
        width=320,
        height=48,
        fg_color="#fffaf6",
        text_color="#2b1d14",
        placeholder_text="Enter your username",
        placeholder_text_color="#9b8172",
        border_color="#e98970",
        border_width=2,
        corner_radius=14,
        font=("Segoe UI", 15)
    )
    login_uname_entry.pack(padx=55, pady=(0, 22), fill="x")

    ctk.CTkLabel(
        right_frame,
        text="Password",
        text_color="#2b1d14",
        font=("Segoe UI", 15, "bold"),
        fg_color="transparent"
    ).pack(anchor="w", padx=55, pady=(0, 7))

    login_pwd_entry = ctk.CTkEntry(
        right_frame,
        width=320,
        height=48,
        show="*",
        fg_color="#fffaf6",
        text_color="#2b1d14",
        placeholder_text="Enter your password",
        placeholder_text_color="#9b8172",
        border_color="#e98970",
        border_width=2,
        corner_radius=14,
        font=("Segoe UI", 15)
    )
    login_pwd_entry.pack(padx=55, pady=(0, 28), fill="x")

    ctk.CTkButton(
        right_frame,
        text="Login",
        command=log_submit,
        fg_color="#fed9bf",
        text_color="#2b1d14",
        hover_color="#ffc9a3",
        font=("Segoe UI", 18, "bold"),
        width=320,
        height=54,
        corner_radius=27
    ).pack(padx=55, pady=(8, 22), fill="x")

    link_frame = ctk.CTkFrame(
        right_frame,
        fg_color="transparent"
    )
    link_frame.pack(pady=(8, 20))

    ctk.CTkLabel(
        link_frame,
        text="Don't have an account?",
        text_color="#5c4033",
        font=("Segoe UI", 13),
        fg_color="transparent"
    ).pack(side="left")

    ctk.CTkButton(
        link_frame,
        text="Register",
        fg_color="transparent",
        text_color="#2b1d14",
        hover_color="#ffc9a3",
        font=("Segoe UI", 13, "bold"),
        border_width=0,
        width=78,
        command=lambda: show_frame("register")
    ).pack(side="left", padx=(4, 0))

    return login
