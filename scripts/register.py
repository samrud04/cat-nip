import customtkinter as ctk
import re
import tkinter as tk
from tkinter import messagebox
import db
from datetime import datetime
from PIL import Image
from datetime import date
from date_picker import attach_date_picker


def register_screen(container, show_frame):

    # =====================================================
    # REGISTER FRAME
    # =====================================================

    register_frame = ctk.CTkFrame(
        container
    )


    bg_image = ctk.CTkImage(
        light_image=Image.open("assets/register_bg.png"),
        dark_image=Image.open("assets/register_bg.png"),
        size=(1400, 750)
    )

    bg_label = ctk.CTkLabel(
        register_frame,
        text="",
        image=bg_image
    )
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    


    # =====================================================
    # TITLE
    # =====================================================

    ctk.CTkLabel(
        register_frame,
        text="User Registration",
        font=("Arial", 40, "bold"),
        text_color="black"
    ).place(
        x=650,
        y=70
    )


    # =====================================================
    # USERNAME
    # =====================================================

    ctk.CTkLabel(
        register_frame,
        text="Username:",
        text_color="black",
        font=("Arial", 24)
    ).place(
        x=200,
        y=180
    )

    register_uname_entry = ctk.CTkEntry(
        register_frame,
        width=250,
        fg_color="white",
        text_color="black"
    )

    register_uname_entry.place(
        x=370,
        y=185
    )


    # =====================================================
    # PASSWORD
    # =====================================================

    ctk.CTkLabel(
        register_frame,
        text="Password:",
        text_color="black",
        font=("Arial", 24)
    ).place(
        x=200,
        y=260
    )

    register_pwd_entry = ctk.CTkEntry(
        register_frame,
        show="*",
        width=250,
        fg_color="white",
        text_color="black"
    )

    register_pwd_entry.place(
        x=370,
        y=265
    )


    # =====================================================
    # CONFIRM PASSWORD
    # =====================================================

    ctk.CTkLabel(
        register_frame,
        text="Confirm Password:",
        text_color="black",
        font=("Arial", 24)
    ).place(
        x=700,
        y=260
    )

    confirm_entry = ctk.CTkEntry(
        register_frame,
        show="*",
        width=250,
        fg_color="white",
        text_color="black"
    )

    confirm_entry.place(
        x=950,
        y=265
    )


    # =====================================================
    # EMAIL
    # =====================================================

    ctk.CTkLabel(
        register_frame,
        text="Email:",
        text_color="black",
        font=("Arial", 24)
    ).place(
        x=200,
        y=340
    )

    email_entry = ctk.CTkEntry(
        register_frame,
        width=250,
        fg_color="white",
        text_color="black"
    )

    email_entry.place(
        x=370,
        y=345
    )


    # =====================================================
    # PHONE
    # =====================================================

    ctk.CTkLabel(
        register_frame,
        text="Phone:",
        text_color="black",
        font=("Arial", 24)
    ).place(
        x=750,
        y=340
    )

    phone_entry = ctk.CTkEntry(
        register_frame,
        width=180,
        fg_color="white",
        text_color="black"
    )

    phone_entry.place(
        x=850,
        y=345
    )


    # =====================================================
    # ADDRESS
    # =====================================================

    ctk.CTkLabel(
        register_frame,
        text="Address:",
        text_color="black",
        font=("Arial", 24)
    ).place(
        x=200,
        y=420
    )

    address_entry = ctk.CTkEntry(
        register_frame,
        width=800,
        fg_color="white",
        text_color="black"
    )

    address_entry.place(
        x=370,
        y=425
    )


    # =====================================================
    # DATE OF BIRTH
    # =====================================================

    ctk.CTkLabel(
        register_frame,
        text="Date of Birth:",
        text_color="black",
        font=("Arial", 24)
    ).place(
        x=200,
        y=500
    )

    dob_entry = ctk.CTkEntry(
        register_frame,
        width=150,
        fg_color="white",
        text_color="black",
        placeholder_text="DD-MM-YYYY"
    )

    dob_entry.place(
        x=400,
        y=505
    )

    dob_calendar_button = ctk.CTkButton(
        register_frame,
        text="📅",
        width=42,
        height=32,
        fg_color="#F4B183",
        hover_color="#D98958",
        text_color="black",
        command=attach_date_picker(
            dob_entry,
            register_frame,
            date_format="%d-%m-%Y",
            min_date=date(1900, 1, 1),
            max_date=date.today(),
            initial_date=date(2000, 1, 1)
        )
    )
    dob_calendar_button.place(x=555, y=505)


    # =====================================================
    # GENDER
    # =====================================================

    ctk.CTkLabel(
        register_frame,
        text="Gender:",
        text_color="black",
        font=("Arial", 24)
    ).place(
        x=650,
        y=500
    )

    gender_entry = ctk.CTkComboBox(
        register_frame,
        values=[
            "Male",
            "Female",
            "Other"
        ],
        width=200
    )

    gender_entry.set("Select Gender")

    gender_entry.place(
        x=760,
        y=505
    )


    # =====================================================
    # REGISTER FUNCTION
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


            current_year = datetime.now().year


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


    # =====================================================
    # SUBMIT BUTTON
    # =====================================================

    ctk.CTkButton(
        register_frame,
        text="Submit",
        command=reg_submit,
        text_color="black",
        fg_color="#7ed957",
        hover_color="#99D980",
        width=220,
        height=50,
        font=("Arial", 24, "bold")
    ).place(
        x=900,
        y=600
    )


    # =====================================================
    # BACK BUTTON
    # =====================================================

    ctk.CTkButton(
        register_frame,
        text="← Back",
        command=lambda: show_frame("main"),
        width=120,
        height=45,
        fg_color="tomato",
        text_color="black",
        hover_color="#FC846F",
        font=("Arial", 18, "bold"),
        corner_radius=20
    ).place(
        x=50,
        y=50
    )


    return register_frame