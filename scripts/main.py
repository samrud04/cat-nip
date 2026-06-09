from turtle import color
import customtkinter as ctk
import db
import re
from PIL import Image, ImageTk
import login
import register
import user
import admin
def show_frame(frame):
    frame.tkraise()

def main():
    # Setup
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
    app = ctk.CTk()
    app.title("Cat-Nip")
    app.geometry("800x600")
    app.after(0, lambda: app.state('zoomed'))
    
    # App icon
    Icon = ctk.CTkImage(Image.open("assets/catnipico.png"), size=(500, 400))

    # Main container
    container = ctk.CTkFrame(app)
    container.pack(fill="both", expand=True)

    container.grid_rowconfigure(0, weight=1)
    container.grid_columnconfigure(0, weight=1)

    # Home Screen
    main_frame = ctk.CTkFrame(container, fg_color="#ffe7d6")
    main_frame.grid(row=0, column=0, sticky="nsew")

    main_frame.grid_columnconfigure(0, weight=1)
    main_frame.grid_columnconfigure(1, weight=1)
    main_frame.grid_rowconfigure(0, weight=1)

    left_frame = ctk.CTkFrame(main_frame, fg_color="#FA9A85", width=300, height=300, corner_radius=100)
    left_frame.grid(row=0, column=0, sticky="nsew", padx=40, pady=40)

    right_frame = ctk.CTkFrame(main_frame, fg_color="#fca265", width=200, height=300, corner_radius=100)
    right_frame.grid(row=0, column=1, sticky="nsew", padx=40, pady=40)

    img_label = ctk.CTkLabel(left_frame, text="",image=Icon, fg_color="#FA9A85")
    img_label.image = Icon
    img_label.place(x=120, y=230)

    ctk.CTkLabel(
        left_frame,
        text="🐾 Pet Supplies",
        text_color="black",
        fg_color="#FA9A85",
        font=("Arial", 64, "bold")
    ).place(x=120, y=100)

    # Home buttons 
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
        command=lambda: show_frame(login_frame)
    ).place(x=170,y=220)

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
        command=lambda: show_frame(register_frame)
    ).place(x=170,y=370)


    # Login Screen
    login_frame = login.login_screen(container, main_frame, show_frame)

    # Register Screen
    register_frame = register.register_screen(container, main_frame, show_frame)

    # User Screen
    user_frame = user.user_screen(container, db.get_products())

    # Admin Screen
    # admin_frame = admin.admin_screen(container)   THIS HAS A LOT OF ERRORS. FIX ADMIN SCREEN FIRST.

    # Start on home
    show_frame(user_frame)

    app.mainloop()


if __name__ == "__main__":
    main()