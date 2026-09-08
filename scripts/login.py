import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import db


def login_screen(container, show_frame, refresh_user_screen):

    # =====================================================
    # LOGIN FRAME
    # =====================================================

    login = ctk.CTkFrame(
        container,
        fg_color="#ffe7d6"
    )


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


        # =================================================
        # ADMIN LOGIN
        # =================================================

        if username == "admin" and password == "admin123":

            login_uname_entry.delete(0, "end")
            login_pwd_entry.delete(0, "end")

            show_frame("admin")

            return


        # =================================================
        # NORMAL USER LOGIN
        # =================================================

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
    # LEFT FRAME - FEATURES
    # =====================================================

    left_frame = ctk.CTkFrame(
        login,
        fg_color="#FA9A85",
        corner_radius=100
    )

    left_frame.grid(
        row=0,
        column=0,
        sticky="nsew",
        padx=(40, 20),
        pady=40
    )


    # LOGO

    ctk.CTkLabel(
        left_frame,
        text="🐾",
        text_color="black",
        font=("Arial", 80)
    ).pack(
        pady=(30, 10)
    )


    # BRAND NAME

    ctk.CTkLabel(
        left_frame,
        text="Pet Goods &\nServices",
        text_color="black",
        font=("Arial", 40, "bold"),
        justify="center"
    ).pack(
        pady=(0, 30)
    )


    # FEATURES

    features = [

        "✓ Browse Pet Products",
        "✓ Book Grooming Services",
        "✓ Track Your Orders",
        "✓ Manage Your Pets"

    ]


    for feature in features:

        ctk.CTkLabel(
            left_frame,
            text=feature,
            text_color="black",
            font=("Arial", 25)
        ).pack(
            pady=8,
            anchor="w",
            padx=30
        )


    # TAGLINE

    ctk.CTkLabel(
        left_frame,
        text="Join thousands of happy\npet owners today!",
        text_color="#fff5f0",
        font=("Arial", 28),
        justify="center"
    ).pack(
        pady=(50, 30)
    )


    # =====================================================
    # RIGHT FRAME - LOGIN FORM
    # =====================================================

    right_frame = ctk.CTkFrame(
        login,
        fg_color="#ffe7d6",
        corner_radius=30
    )

    right_frame.grid(
        row=0,
        column=1,
        sticky="nsew",
        padx=(20, 40),
        pady=40
    )


    # TITLE

    ctk.CTkLabel(
        right_frame,
        text="Login",
        text_color="black",
        font=("Arial", 48, "bold")
    ).pack(
        pady=(40, 30)
    )


    # =====================================================
    # USERNAME
    # =====================================================

    ctk.CTkLabel(
        right_frame,
        text="Username:",
        text_color="black",
        font=("Arial", 16, "bold")
    ).pack(
        anchor="w",
        padx=40,
        pady=(10, 0)
    )


    login_uname_entry = ctk.CTkEntry(
        right_frame,
        width=250,
        fg_color="white",
        text_color="black",
        border_color="#FA9A85",
        border_width=2,
        font=("Arial", 13)
    )

    login_uname_entry.pack(
        padx=40,
        pady=(5, 20)
    )


    # =====================================================
    # PASSWORD
    # =====================================================

    ctk.CTkLabel(
        right_frame,
        text="Password:",
        text_color="black",
        font=("Arial", 16, "bold")
    ).pack(
        anchor="w",
        padx=40
    )


    login_pwd_entry = ctk.CTkEntry(
        right_frame,
        width=250,
        show="*",
        fg_color="white",
        text_color="black",
        border_color="#FA9A85",
        border_width=2,
        font=("Arial", 13)
    )

    login_pwd_entry.pack(
        padx=40,
        pady=(5, 30)
    )


    # =====================================================
    # LOGIN BUTTON
    # =====================================================

    ctk.CTkButton(
        right_frame,
        text="Login",
        command=log_submit,
        fg_color="#7ed957",
        text_color="black",
        hover_color="#99D980",
        font=("Arial", 16, "bold"),
        width=250,
        height=45,
        corner_radius=10
    ).pack(
        pady=20
    )


    # =====================================================
    # REGISTER LINK
    # =====================================================

    link_frame = ctk.CTkFrame(
        right_frame,
        fg_color="#ffe7d6"
    )

    link_frame.pack(
        pady=(10, 40)
    )


    ctk.CTkLabel(
        link_frame,
        text="Don't have an account? ",
        text_color="black",
        font=("Arial", 11)
    ).pack(
        side="left"
    )


    ctk.CTkButton(
        link_frame,
        text="Register",
        fg_color="#ffe7d6",
        text_color="#FA9A85",
        hover_color="white",
        font=("Arial", 11, "bold"),
        border_width=0,
        command=lambda: show_frame("register")
    ).pack(
        side="left"
    )


    # =====================================================
    # BACK BUTTON
    # =====================================================

    ctk.CTkButton(
        left_frame,
        text="←",
        command=lambda: show_frame("main"),
        width=50,
        height=50,
        fg_color="tomato",
        text_color="black",
        hover_color="#FC846F",
        font=("Arial", 30, "bold"),
        corner_radius=50
    ).place(
        x=50,
        y=50
    )


    return login