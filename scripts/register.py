import customtkinter as ctk
import re
import tkinter as tk
from tkinter import messagebox
import db
from datetime import datetime
from datetime import date
from date_picker import attach_date_picker


def register_screen(container, show_frame):

    # =====================================================
    # REGISTER FRAME  (matches main.py peach theme)
    # =====================================================

    register_frame = ctk.CTkFrame(
        container,
        fg_color="#ffe7d6"
    )

    # Center content card
    card = ctk.CTkFrame(
        register_frame,
        fg_color="#FA9A85",
        corner_radius=40
    )
    card.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.88, relheight=0.88)

    # Inner content area
    content = ctk.CTkFrame(card, fg_color="transparent")
    content.pack(fill="both", expand=True, padx=50, pady=30)

    # =====================================================
    # HEADER
    # =====================================================

    header = ctk.CTkFrame(content, fg_color="transparent")
    header.pack(fill="x", pady=(10, 20))

    ctk.CTkButton(
        header,
        text="← Back",
        command=lambda: show_frame("main"),
        width=110,
        height=40,
        fg_color="#fed9bf",
        hover_color="#ffc9a3",
        text_color="#2b1d14",
        font=("Segoe UI", 16, "bold"),
        corner_radius=20
    ).pack(side="left")

    ctk.CTkLabel(
        header,
        text="🐾 Create Account",
        font=("Segoe UI", 36, "bold"),
        text_color="#2b1d14"
    ).pack(side="left", padx=30)

    # =====================================================
    # FORM GRID
    # =====================================================

    form = ctk.CTkFrame(content, fg_color="transparent")
    form.pack(fill="both", expand=True)

    form.grid_columnconfigure(0, weight=1)
    form.grid_columnconfigure(1, weight=1)
    form.grid_columnconfigure(2, weight=1)
    form.grid_columnconfigure(3, weight=1)

    # ---------- Username ----------
    ctk.CTkLabel(
        form,
        text="Username",
        text_color="#2b1d14",
        font=("Segoe UI", 16, "bold"),
        anchor="w"
    ).grid(row=0, column=0, columnspan=2, sticky="w", padx=(0, 15), pady=(0, 4))

    register_uname_entry = ctk.CTkEntry(
        form,
        height=42,
        fg_color="#fff8f2",
        border_color="#fca265",
        border_width=2,
        text_color="#2b1d14",
        font=("Segoe UI", 15),
        corner_radius=12
    )
    register_uname_entry.grid(row=1, column=0, columnspan=2, sticky="ew", padx=(0, 15), pady=(0, 16))

    # ---------- Password ----------
    ctk.CTkLabel(
        form,
        text="Password",
        text_color="#2b1d14",
        font=("Segoe UI", 16, "bold"),
        anchor="w"
    ).grid(row=0, column=2, sticky="w", padx=(15, 8), pady=(0, 4))

    register_pwd_entry = ctk.CTkEntry(
        form,
        show="*",
        height=42,
        fg_color="#fff8f2",
        border_color="#fca265",
        border_width=2,
        text_color="#2b1d14",
        font=("Segoe UI", 15),
        corner_radius=12
    )
    register_pwd_entry.grid(row=1, column=2, sticky="ew", padx=(15, 8), pady=(0, 16))

    # ---------- Confirm Password ----------
    ctk.CTkLabel(
        form,
        text="Confirm Password",
        text_color="#2b1d14",
        font=("Segoe UI", 16, "bold"),
        anchor="w"
    ).grid(row=0, column=3, sticky="w", padx=(8, 0), pady=(0, 4))

    confirm_entry = ctk.CTkEntry(
        form,
        show="*",
        height=42,
        fg_color="#fff8f2",
        border_color="#fca265",
        border_width=2,
        text_color="#2b1d14",
        font=("Segoe UI", 15),
        corner_radius=12
    )
    confirm_entry.grid(row=1, column=3, sticky="ew", padx=(8, 0), pady=(0, 16))

    # ---------- Email ----------
    ctk.CTkLabel(
        form,
        text="Email",
        text_color="#2b1d14",
        font=("Segoe UI", 16, "bold"),
        anchor="w"
    ).grid(row=2, column=0, columnspan=2, sticky="w", padx=(0, 15), pady=(0, 4))

    email_row = ctk.CTkFrame(form, fg_color="transparent")
    email_row.grid(row=3, column=0, columnspan=2, sticky="ew", padx=(0, 15), pady=(0, 4))
    email_row.grid_columnconfigure(0, weight=1)

    email_entry = ctk.CTkEntry(
        email_row,
        height=42,
        fg_color="#fff8f2",
        border_color="#fca265",
        border_width=2,
        text_color="#2b1d14",
        font=("Segoe UI", 15),
        corner_radius=12
    )
    email_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))

    

    # ---------- Phone ----------
    ctk.CTkLabel(
        form,
        text="Phone",
        text_color="#2b1d14",
        font=("Segoe UI", 16, "bold"),
        anchor="w"
    ).grid(row=2, column=2, columnspan=2, sticky="w", padx=(15, 0), pady=(0, 4))

    phone_entry = ctk.CTkEntry(
        form,
        height=42,
        fg_color="#fff8f2",
        border_color="#fca265",
        border_width=2,
        text_color="#2b1d14",
        font=("Segoe UI", 15),
        corner_radius=12,
        placeholder_text="10-digit number"
    )
    phone_entry.grid(row=3, column=2, columnspan=2, sticky="ew", padx=(15, 0), pady=(0, 4))

    # spacer under phone to align with email status
    ctk.CTkLabel(form, text="", height=20).grid(row=4, column=2, columnspan=2)

    # ---------- Address (full width) ----------
    ctk.CTkLabel(
        form,
        text="Address",
        text_color="#2b1d14",
        font=("Segoe UI", 16, "bold"),
        anchor="w"
    ).grid(row=5, column=0, columnspan=4, sticky="w", pady=(0, 4))

    address_entry = ctk.CTkEntry(
        form,
        height=42,
        fg_color="#fff8f2",
        border_color="#fca265",
        border_width=2,
        text_color="#2b1d14",
        font=("Segoe UI", 15),
        corner_radius=12
    )
    address_entry.grid(row=6, column=0, columnspan=4, sticky="ew", pady=(0, 16))

    # ---------- DOB + Gender ----------
    ctk.CTkLabel(
        form,
        text="Date of Birth",
        text_color="#2b1d14",
        font=("Segoe UI", 16, "bold"),
        anchor="w"
    ).grid(row=7, column=0, columnspan=2, sticky="w", padx=(0, 15), pady=(0, 4))

    dob_row = ctk.CTkFrame(form, fg_color="transparent")
    dob_row.grid(row=8, column=0, columnspan=2, sticky="ew", padx=(0, 15), pady=(0, 20))
    dob_row.grid_columnconfigure(0, weight=1)

    dob_entry = ctk.CTkEntry(
        dob_row,
        height=42,
        fg_color="#fff8f2",
        border_color="#fca265",
        border_width=2,
        text_color="#2b1d14",
        font=("Segoe UI", 15),
        corner_radius=12,
        placeholder_text="DD-MM-YYYY"
    )
    dob_entry.grid(row=0, column=0, sticky="ew", padx=(0, 8))

    dob_calendar_button = ctk.CTkButton(
        dob_row,
        text="📅",
        width=48,
        height=42,
        fg_color="#fca265",
        hover_color="#e8904f",
        text_color="#2b1d14",
        font=("Segoe UI", 18),
        corner_radius=12,
        command=attach_date_picker(
            dob_entry,
            register_frame,
            date_format="%d-%m-%Y",
            min_date=date(1900, 1, 1),
            max_date=date.today(),
            initial_date=date(2000, 1, 1)
        )
    )
    dob_calendar_button.grid(row=0, column=1)

    ctk.CTkLabel(
        form,
        text="Gender",
        text_color="#2b1d14",
        font=("Segoe UI", 16, "bold"),
        anchor="w"
    ).grid(row=7, column=2, columnspan=2, sticky="w", padx=(15, 0), pady=(0, 4))

    gender_entry = ctk.CTkComboBox(
        form,
        values=["Male", "Female", "Other"],
        height=42,
        fg_color="#fff8f2",
        border_color="#fca265",
        border_width=2,
        button_color="#fca265",
        button_hover_color="#e8904f",
        dropdown_fg_color="#fff8f2",
        dropdown_hover_color="#fed9bf",
        text_color="#2b1d14",
        font=("Segoe UI", 15),
        corner_radius=12
    )
    gender_entry.set("Select Gender")
    gender_entry.grid(row=8, column=2, columnspan=2, sticky="ew", padx=(15, 0), pady=(0, 20))

    # =====================================================
    # SUBMIT BUTTON
    # =====================================================

    def reg_submit():

        username = register_uname_entry.get().strip()
        password = register_pwd_entry.get()
        confirm = confirm_entry.get()

        email = email_entry.get().strip()
        phone = phone_entry.get().strip()

        address = address_entry.get().strip()
        gender = gender_entry.get()

        dob = dob_entry.get().strip()

        # =================================================
        # EMPTY FIELDS
        # =================================================

        if (
            not username
            or not password
            or not confirm
            or not email
            or not phone
            or not address
            or not dob
            or gender == "Select Gender"
        ):
            messagebox.showerror(
                "Error",
                "Please fill all fields!"
            )
            return

        # =================================================
        # PASSWORD CHECK
        # =================================================

        if password != confirm:
            messagebox.showerror(
                "Error",
                "Passwords do not match!"
            )
            return

        # =================================================
        # EMAIL CHECK
        # =================================================

        email_check = re.match(
            r'^[\w\.-]+@[\w\.-]+\.\w+$',
            email
        )

        if email_check is None:
            messagebox.showerror(
                "Error",
                "Invalid email address!"
            )
            return


        # =================================================
        # PHONE CHECK
        # =================================================

        phone_check = re.match(
            r'^[6-9]\d{9}$',
            phone
        )

        if phone_check is None:
            messagebox.showerror(
                "Error",
                "Invalid phone number! Enter a valid 10 digit number."
            )
            return

        # =================================================
        # DATE OF BIRTH CHECK
        # =================================================

        try:
            dob_date = datetime.strptime(
                dob,
                "%d-%m-%Y"
            )

            if (
                dob_date.year < 1900
                or dob_date.date() > datetime.now().date()
            ):
                messagebox.showerror(
                    "Error",
                    "Enter a valid birth year!"
                )
                return

            # DATABASE FORMAT
            dob = dob_date.strftime(
                "%Y-%m-%d"
            )

        except ValueError:
            messagebox.showerror(
                "Error",
                "Invalid DOB! Use DD-MM-YYYY format."
            )
            return

        # =================================================
        # DATABASE REGISTRATION
        # =================================================

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
                "Registration successful! You can now log in."
            )

            # CLEAR FIELDS
            register_uname_entry.delete(0, "end")
            register_pwd_entry.delete(0, "end")
            confirm_entry.delete(0, "end")

            email_entry.delete(0, "end")
            phone_entry.delete(0, "end")

            address_entry.delete(0, "end")
            dob_entry.delete(0, "end")

            gender_entry.set(
                "Select Gender"
            )

            # GO TO LOGIN
            show_frame("login")

        else:
            messagebox.showerror(
                "Error",
                "Username already exists! Please choose another one."
            )

    # Submit button centered at bottom
    btn_frame = ctk.CTkFrame(content, fg_color="transparent")
    btn_frame.pack(fill="x", pady=(5, 10))

    ctk.CTkButton(
        btn_frame,
        text="Create Account",
        command=reg_submit,
        width=260,
        height=52,
        fg_color="#fed9bf",
        hover_color="#ffc9a3",
        text_color="#2b1d14",
        font=("Segoe UI", 20, "bold"),
        corner_radius=26
    ).pack()

    return register_frame
