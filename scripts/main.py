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
    main_frame = ctk.CTkFrame(container, fg_color="#003566")
    main_frame.grid(row=0, column=0, sticky="nsew")

    main_frame.grid_columnconfigure(0, weight=1)
    main_frame.grid_columnconfigure(1, weight=1)
    main_frame.grid_rowconfigure(0, weight=1)

    left_frame = ctk.CTkFrame(main_frame, fg_color="#69dfff", width=300, height=300, corner_radius=100)
    left_frame.grid(row=0, column=0, sticky="nsew", padx=40, pady=40)

    right_frame = ctk.CTkFrame(main_frame, fg_color="#003566", width=200, height=300)
    right_frame.grid(row=0, column=1, sticky="nsew", padx=40, pady=40)

    img_label = ctk.CTkLabel(left_frame, text="",image=Icon, fg_color="#69dfff")
    img_label.image = Icon
    img_label.place(x=120, y=230)

    ctk.CTkLabel(
        left_frame,
        text="Cat-Nip",
        text_color="black",
        fg_color="#69dfff",
        font=("Arial", 84, "bold")
    ).place(x=210, y=100)

    # Home buttons 
    ctk.CTkButton(
        right_frame,
        text="Login",
        width=300,
        height=80,
        corner_radius=100,
        fg_color="#fbe58c",
        hover_color="#FCCD77",
        text_color="black",
        font=("Arial", 41),
        command=lambda: show_frame(login_frame)
    ).place(x=150,y=220)

    ctk.CTkButton(
        right_frame,
        text="Register",
        width=300,
        height=80,
        corner_radius=100,
        fg_color="#fbe58c",
        hover_color="#FCCD77",
        text_color="black",
        font=("Arial", 41),
        command=lambda: show_frame(register_frame)
    ).place(x=150,y=370)


    # Login Screen
    login_frame = login.login_screen(container, main_frame, show_frame)

    # Register Screen
    register_frame = register.register_screen(container, main_frame, show_frame)

    # User Screen
    user_frame = user.user_screen(container)

    # Admin Screen
    admin_frame = admin.admin_screen(container)

    # Start on home
    show_frame(admin_frame)

    app.mainloop()


if __name__ == "__main__":
    main()