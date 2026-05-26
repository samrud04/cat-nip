# Beautified Cat-Nip Structure


import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image

import re
import db


# ---------------- APP CONFIG ----------------

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


# ---------------- COLORS ----------------

WHITE = "#ffffff"
YELLOW = "#ffe683"
LIGHT_YELLOW = "#feefb5"
BUTTON_YELLOW = "#fbe58c"

GREEN = "#7ed957"
GREEN_HOVER = "#99D980"

RED = "tomato"
RED_HOVER = "#FC846F"

TEXT = "black"


# ---------------- HELPERS ----------------


def show_frame(frame):
    frame.tkraise()


# ---------------- MAIN APP ----------------


def main():

    app = ctk.CTk()
    app.title("Cat-Nip")
    app.geometry("800x600")
    app.after(0, lambda: app.state("zoomed"))

    # ---------------- ICONS ----------------

    logo_image = ctk.CTkImage(
        Image.open("assets/catnipico.png"),
        size=(500, 400)
    )

    order_icon = ctk.CTkImage(
        Image.open("assets/order_icon.png"),
        size=(20, 20)
    )

    book_icon = ctk.CTkImage(
        Image.open("assets/book_icon.png"),
        size=(20, 20)
    )

    settings_icon = ctk.CTkImage(
        Image.open("assets/settings_icon.png"),
        size=(20, 20)
    )

    # ---------------- CONTAINER ----------------

    container = ctk.CTkFrame(app)
    container.pack(fill="both", expand=True)

    container.grid_rowconfigure(0, weight=1)
    container.grid_columnconfigure(0, weight=1)

    # ============================================================
    # HOME SCREEN
    # ============================================================

    home_screen = ctk.CTkFrame(container, fg_color=WHITE)
    home_screen.grid(row=0, column=0, sticky="nsew")

    home_screen.grid_columnconfigure(0, weight=1)
    home_screen.grid_columnconfigure(1, weight=1)
    home_screen.grid_rowconfigure(0, weight=1)

    left_frame = ctk.CTkFrame(
        home_screen,
        fg_color=YELLOW
    )

    left_frame.grid(
        row=0,
        column=0,
        sticky="nsew",
        padx=40,
        pady=40
    )

    right_frame = ctk.CTkFrame(
        home_screen,
        fg_color=WHITE
    )

    right_frame.grid(
        row=0,
        column=1,
        sticky="nsew",
        padx=40,
        pady=40
    )

    ctk.CTkLabel(
        left_frame,
        text="",
        image=logo_image,
        fg_color=YELLOW
    ).place(x=120, y=230)

    ctk.CTkLabel(
        left_frame,
        text="Cat-Nip",
        text_color=TEXT,
        fg_color=YELLOW,
        font=("Arial", 84, "bold")
    ).place(x=210, y=100)

    # ============================================================
    # LOGIN SCREEN
    # ============================================================

    login_screen = ctk.CTkFrame(container, fg_color=WHITE)
    login_screen.grid(row=0, column=0, sticky="nsew")

    login_screen.grid_columnconfigure(0, weight=1)
    login_screen.grid_columnconfigure(1, weight=1)
    login_screen.grid_rowconfigure(0, weight=1)

    login_left = ctk.CTkFrame(
        login_screen,
        fg_color=YELLOW
    )

    login_left.grid(
        row=0,
        column=0,
        sticky="nsew",
        padx=40,
        pady=40
    )

    login_right = ctk.CTkFrame(
        login_screen,
        fg_color=LIGHT_YELLOW
    )

    login_right.grid(
        row=0,
        column=1,
        sticky="nsew",
        padx=(0, 40),
        pady=40
    )

    ctk.CTkLabel(
        login_left,
        text="Login",
        fg_color=YELLOW,
        text_color=TEXT,
        font=("Arial", 64, "bold")
    ).place(x=220, y=100)

    # ---------------- USER TYPE ----------------

    user_type = tk.StringVar(value="user")

    ctk.CTkRadioButton(
        login_left,
        text="User",
        variable=user_type,
        value="user",
        text_color=TEXT,
        font=("Arial", 24, "bold")
    ).place(x=250, y=250)

    ctk.CTkRadioButton(
        login_left,
        text="Employee",
        variable=user_type,
        value="employee",
        text_color=TEXT,
        font=("Arial", 24, "bold")
    ).place(x=250, y=350)

    ctk.CTkRadioButton(
        login_left,
        text="Admin",
        variable=user_type,
        value="admin",
        text_color=TEXT,
        font=("Arial", 24, "bold")
    ).place(x=250, y=450)

    # ---------------- LOGIN FIELDS ----------------

    ctk.CTkLabel(
        login_right,
        text="Username:",
        text_color=TEXT,
        fg_color=LIGHT_YELLOW,
        font=("Arial", 34, "bold")
    ).place(x=180, y=250)

    username_entry = ctk.CTkEntry(
        login_right,
        width=150,
        fg_color=WHITE,
        text_color=TEXT
    )

    username_entry.place(x=420, y=257)

    ctk.CTkLabel(
        login_right,
        text="Password:",
        text_color=TEXT,
        fg_color=LIGHT_YELLOW,
        font=("Arial", 34, "bold")
    ).place(x=180, y=320)

    password_entry = ctk.CTkEntry(
        login_right,
        show="*",
        width=150,
        fg_color=WHITE,
        text_color=TEXT
    )

    password_entry.place(x=420, y=327)

    # ============================================================
    # REGISTER SCREEN
    # ============================================================

    register_screen = ctk.CTkFrame(
        container,
        fg_color=YELLOW
    )

    register_screen.grid(
        row=0,
        column=0,
        sticky="nsew",
        padx=40,
        pady=40
    )

    ctk.CTkLabel(
        register_screen,
        text="User Registration",
        font=("Arial", 56, "bold"),
        text_color=TEXT
    ).place(x=800, y=80)

    # ---------------- REGISTER FORM ----------------

    labels = [
        ("Username:", 150),
        ("Password:", 230),
        ("Email:", 310),
        ("Address:", 390),
        ("Date of Birth:", 470),
        ("Gender:", 570)
    ]

    for text, y in labels:
        ctk.CTkLabel(
            register_screen,
            text=text,
            text_color=TEXT,
            font=("Arial", 29)
        ).place(x=200, y=y)

    register_username = ctk.CTkEntry(
        register_screen,
        width=250,
        fg_color=WHITE,
        text_color=TEXT
    )

    register_username.place(x=370, y=153)

    register_password = ctk.CTkEntry(
        register_screen,
        show="*",
        width=250,
        fg_color=WHITE,
        text_color=TEXT
    )

    register_password.place(x=370, y=233)

    confirm_password = ctk.CTkEntry(
        register_screen,
        show="*",
        width=250,
        fg_color=WHITE,
        text_color=TEXT
    )

    confirm_password.place(x=920, y=233)

    email_entry = ctk.CTkEntry(
        register_screen,
        width=250,
        fg_color=WHITE,
        text_color=TEXT
    )

    email_entry.place(x=370, y=313)

    phone_entry = ctk.CTkEntry(
        register_screen,
        width=100,
        fg_color=WHITE,
        text_color=TEXT
    )

    phone_entry.place(x=780, y=313)

    address_entry = ctk.CTkEntry(
        register_screen,
        width=800,
        fg_color=WHITE,
        text_color=TEXT
    )

    address_entry.place(x=370, y=393)

    dob_entry = ctk.CTkEntry(
        register_screen,
        width=100,
        fg_color=WHITE,
        text_color=TEXT
    )

    dob_entry.place(x=370, y=473)

    gender_entry = ctk.CTkEntry(
        register_screen,
        width=250,
        fg_color=WHITE,
        text_color=TEXT
    )

    gender_entry.place(x=370, y=573)

    # ============================================================
    # USER SCREEN
    # ============================================================

    user_screen = ctk.CTkFrame(container, fg_color=WHITE)
    user_screen.grid(row=0, column=0, sticky="nsew")

    user_screen.grid_rowconfigure(0, weight=1)
    user_screen.grid_columnconfigure(0, weight=1)

    user_main = ctk.CTkScrollableFrame(
        user_screen,
        fg_color=LIGHT_YELLOW
    )

    user_main.grid(
        row=0,
        column=0,
        sticky="nsew",
        padx=40,
        pady=(40, 10)
    )

    user_nav = ctk.CTkFrame(
        user_screen,
        fg_color=BUTTON_YELLOW,
        height=80
    )

    user_nav.grid(
        row=1,
        column=0,
        sticky="nsew",
        padx=40,
        pady=(0, 40)
    )

    # ---------------- SEARCH ----------------

    ctk.CTkLabel(
        user_main,
        text="Search:",
        font=("Arial", 24),
        text_color=TEXT,
        fg_color=LIGHT_YELLOW
    ).grid(row=0, column=0, padx=20, pady=100)

    search_entry = ctk.CTkEntry(
        user_main,
        placeholder_text="eg: Cat Food",
        width=400,
        height=35,
        fg_color=WHITE,
        text_color=TEXT,
        font=("Arial", 16)
    )

    search_entry.grid(row=0, column=1, pady=100)

    # ---------------- CATEGORY ----------------

    ctk.CTkLabel(
        user_main,
        text="CATEGORY:",
        font=("Arial", 16),
        text_color=TEXT,
        fg_color=LIGHT_YELLOW
    ).grid(row=1, column=0, padx=20, pady=20)

    category_box = ttk.Combobox(
        user_main,
        values=["Food", "Toys", "Accessories"],
        width=20,
        state="readonly"
    )

    category_box.grid(row=1, column=1, sticky="w")
    category_box.current(0)

    def update_placeholder(event=None):

        selected = category_box.get()

        if selected == "Food":
            search_entry.configure(
                placeholder_text="eg: Whiskas, Meow Mix"
            )

        elif selected == "Toys":
            search_entry.configure(
                placeholder_text="eg: Catnip Mouse, Feather Wand"
            )

        elif selected == "Accessories":
            search_entry.configure(
                placeholder_text="eg: Cat Bed, Scratching Post"
            )

    category_box.bind("<<ComboboxSelected>>", update_placeholder)

    # ---------------- LOGIN FUNCTION ----------------

    def login_submit():

        username = username_entry.get()
        password = password_entry.get()
        selected_user_type = user_type.get()

        if not username or not password:
            messagebox.showerror(
                "Error",
                "Please fill all fields!"
            )
            return

        logged_in = db.login(
            selected_user_type,
            username,
            password
        )

        if logged_in:
            show_frame(user_screen)

        else:
            messagebox.showerror(
                "Error",
                "Invalid credentials!"
            )

    # ---------------- REGISTER FUNCTION ----------------

    def register_submit():

        username = register_username.get()
        password = register_password.get()
        confirm = confirm_password.get()
        email = email_entry.get()
        phone = phone_entry.get()
        address = address_entry.get()
        gender = gender_entry.get()
        dob = dob_entry.get()

        if (
            not username or
            not password or
            not confirm or
            not email or
            not phone or
            not address or
            not gender or
            not dob
        ):

            messagebox.showerror(
                "Error",
                "Please fill all fields!"
            )

            return

        if password != confirm:

            messagebox.showerror(
                "Error",
                "Passwords do not match!"
            )

            return

        if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email) is None:

            messagebox.showerror(
                "Error",
                "Invalid email address!"
            )

            return

        if re.match(r'^[6-9]\d{9}$', phone) is None:

            messagebox.showerror(
                "Error",
                "Invalid phone number!"
            )

            return

        registered = db.register(
            username,
            password,
            email,
            phone,
            address,
            gender,
            dob
        )

        if registered:

            messagebox.showinfo(
                "Success",
                "Registration successful!"
            )

            show_frame(login_screen)

        else:

            messagebox.showerror(
                "Error",
                "Username already exists!"
            )

    # ============================================================
    # BUTTONS
    # ============================================================

    ctk.CTkButton(
        right_frame,
        text="Login",
        width=300,
        height=80,
        fg_color=BUTTON_YELLOW,
        hover_color="#FCCD77",
        text_color=TEXT,
        font=("Arial", 41),
        command=lambda: show_frame(login_screen)
    ).place(x=150, y=220)

    ctk.CTkButton(
        right_frame,
        text="Register",
        width=300,
        height=80,
        fg_color=BUTTON_YELLOW,
        hover_color="#FCCD77",
        text_color=TEXT,
        font=("Arial", 41),
        command=lambda: show_frame(register_screen)
    ).place(x=150, y=370)

    ctk.CTkButton(
        login_right,
        text="Submit",
        command=login_submit,
        fg_color=GREEN,
        hover_color=GREEN_HOVER,
        text_color=TEXT,
        font=("Arial", 16, "bold")
    ).place(x=280, y=400)

    ctk.CTkButton(
        register_screen,
        text="Submit",
        command=register_submit,
        text_color=TEXT,
        fg_color=GREEN,
        hover_color=GREEN_HOVER,
        width=200,
        height=40,
        font=("Arial", 26, "bold")
    ).place(x=800, y=500)

    ctk.CTkButton(
        user_nav,
        text="Order",
        image=order_icon,
        compound="left",
        width=250,
        height=60,
        fg_color="#f9b746",
        text_color=TEXT,
        hover_color="#e0a73d",
        font=("Arial", 16, "bold")
    ).place(x=50, y=10)

    ctk.CTkButton(
        user_nav,
        text="Book",
        image=book_icon,
        compound="left",
        width=250,
        height=60,
        fg_color="#f9b746",
        text_color=TEXT,
        hover_color="#e0a73d",
        font=("Arial", 16, "bold")
    ).place(x=620, y=10)

    ctk.CTkButton(
        user_nav,
        text="Settings",
        image=settings_icon,
        compound="left",
        width=250,
        height=60,
        fg_color="#f9b746",
        text_color=TEXT,
        hover_color="#e0a73d",
        font=("Arial", 16, "bold")
    ).place(x=1200, y=10)

    # ---------------- BACK BUTTONS ----------------

    ctk.CTkButton(
        login_screen,
        text="Back",
        command=lambda: show_frame(home_screen),
        width=100,
        height=40,
        fg_color=RED,
        hover_color=RED_HOVER,
        text_color=TEXT
    ).place(x=80, y=80)

    ctk.CTkButton(
        register_screen,
        text="Back",
        command=lambda: show_frame(home_screen),
        width=100,
        height=40,
        fg_color=RED,
        hover_color=RED_HOVER,
        text_color=TEXT
    ).place(x=50, y=50)

    ctk.CTkButton(
        user_screen,
        text="Back",
        command=lambda: show_frame(login_screen),
        width=100,
        height=40,
        fg_color=RED,
        hover_color=RED_HOVER,
        text_color=TEXT
    ).place(x=80, y=80)

    # ============================================================
    # START APP
    # ============================================================

    show_frame(home_screen)

    app.mainloop()


if __name__ == "__main__":
    main()


# Improvements Made

