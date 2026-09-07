import customtkinter as ctk
from PIL import Image

import db
import login
import register
import user
import admin


def main():

    # ================= APP SETUP =================

    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()

    app.title("Cat-Nip")

    app.geometry("800x600")

    app.after(0, lambda: app.state("zoomed"))


    # ================= ICON =================

    icon = ctk.CTkImage(
        Image.open("assets/catnipico.png"),
        size=(500, 400)
    )


    # ================= MAIN CONTAINER =================

    container = ctk.CTkFrame(app)

    container.pack(
        fill="both",
        expand=True
    )

    container.grid_rowconfigure(0, weight=1)
    container.grid_columnconfigure(0, weight=1)


    # ================= FRAMES DICTIONARY =================

    frames = {}


    def show_frame(name):

        frames[name].tkraise()


    # =====================================================
    # HOME SCREEN
    # =====================================================

    main_frame = ctk.CTkFrame(
        container,
        fg_color="#ffe7d6"
    )

    main_frame.grid(
        row=0,
        column=0,
        sticky="nsew"
    )

    frames["main"] = main_frame


    main_frame.grid_columnconfigure(0, weight=1)
    main_frame.grid_columnconfigure(1, weight=1)
    main_frame.grid_rowconfigure(0, weight=1)


    # LEFT SIDE

    left_frame = ctk.CTkFrame(
        main_frame,
        fg_color="#FA9A85",
        corner_radius=100
    )

    left_frame.grid(
        row=0,
        column=0,
        sticky="nsew",
        padx=40,
        pady=40
    )


    # RIGHT SIDE

    right_frame = ctk.CTkFrame(
        main_frame,
        fg_color="#fca265",
        corner_radius=100
    )

    right_frame.grid(
        row=0,
        column=1,
        sticky="nsew",
        padx=40,
        pady=40
    )


    # LOGO

    img_label = ctk.CTkLabel(
        left_frame,
        text="",
        image=icon,
        fg_color="#FA9A85"
    )

    img_label.image = icon

    img_label.place(
        x=120,
        y=230
    )


    # TITLE

    ctk.CTkLabel(
        left_frame,
        text="🐾 Pet Supplies",
        text_color="black",
        fg_color="#FA9A85",
        font=("Arial", 64, "bold")
    ).place(
        x=120,
        y=100
    )


    # LOGIN BUTTON

    ctk.CTkButton(
        right_frame,
        text="Login",
        width=300,
        height=80,
        corner_radius=100,
        fg_color="#fed9bf",
        hover_color="#ffd0af",
        text_color="black",
        font=("Arial", 41, "bold"),
        command=lambda: show_frame("login")
    ).place(
        x=170,
        y=220
    )


    # REGISTER BUTTON

    ctk.CTkButton(
        right_frame,
        text="Register",
        width=300,
        height=80,
        corner_radius=100,
        fg_color="#fed9bf",
        hover_color="#ffd0af",
        text_color="black",
        font=("Arial", 41, "bold"),
        command=lambda: show_frame("register")
    ).place(
        x=170,
        y=370
    )


    # =====================================================
    # CREATE LOGIN SCREEN
    # =====================================================

    login_frame = login.login_screen(
        container,
        show_frame
    )

    login_frame.grid(
        row=0,
        column=0,
        sticky="nsew"
    )

    frames["login"] = login_frame


    # =====================================================
    # CREATE REGISTER SCREEN
    # =====================================================

    register_frame = register.register_screen(
        container,
        show_frame
    )

    register_frame.grid(
        row=0,
        column=0,
        sticky="nsew"
    )

    frames["register"] = register_frame


    # =====================================================
    # CREATE USER SCREEN
    # =====================================================

    user_frame = user.user_screen(
    container,
    show_frame
    )

    user_frame.grid(
        row=0,
        column=0,
        sticky="nsew"
    )

    frames["user"] = user_frame


    # =====================================================
    # CREATE ADMIN SCREEN
    # =====================================================

    admin_frame = admin.create_admin_frame(
        container,
        show_frame
    )

    admin_frame.grid(
        row=0,
        column=0,
        sticky="nsew"
    )

    frames["admin"] = admin_frame


    # =====================================================
    # START APPLICATION
    # =====================================================

    show_frame("main")

    app.mainloop()


if __name__ == "__main__":
    main()