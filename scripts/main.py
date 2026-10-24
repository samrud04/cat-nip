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
    app.title("Cat-Nip 🐾")
    app.geometry("1200x750")
    app.after(100, lambda: app.state("zoomed"))

    # Soft peach background
    app.configure(fg_color="#ffe7d6")

    # ================= ICON =================
    try:
        icon = ctk.CTkImage(
            Image.open("assets/catnipico.png"),
            size=(280, 220)
        )
    except Exception as e:
        print("Icon error:", e)
        icon = None

    # ================= CONTAINER =================
    container = ctk.CTkFrame(app, fg_color="transparent")
    container.pack(fill="both", expand=True)

    container.grid_rowconfigure(0, weight=1)
    container.grid_columnconfigure(0, weight=1)

    frames = {}

    def show_frame(name):
        frames[name].tkraise()

    def refresh_user_screen():
        if "user" in frames:
            frames["user"].destroy()
        user_frame = user.user_screen(container, show_frame)
        user_frame.grid(row=0, column=0, sticky="nsew")
        frames["user"] = user_frame
        show_frame("user")

    # =====================================================
    # HOME SCREEN
    # =====================================================
    main_frame = ctk.CTkFrame(container, fg_color="transparent")
    main_frame.grid(row=0, column=0, sticky="nsew")
    frames["main"] = main_frame

    main_frame.grid_columnconfigure(0, weight=1)
    main_frame.grid_columnconfigure(1, weight=1)
    main_frame.grid_rowconfigure(0, weight=1)

    # ---------- LEFT CARD ----------
    left_frame = ctk.CTkFrame(
        main_frame,
        fg_color="#FA9A85",
        corner_radius=40
    )
    left_frame.grid(row=0, column=0, sticky="nsew", padx=(60, 30), pady=80)

    left_frame.grid_rowconfigure(0, weight=1)
    left_frame.grid_rowconfigure(1, weight=0)
    left_frame.grid_rowconfigure(2, weight=1)
    left_frame.grid_columnconfigure(0, weight=1)

    ctk.CTkLabel(
        left_frame,
        text="🐾 Cat-Nip",
        text_color="#2b1d14",
        font=("Segoe UI", 52, "bold"),
        fg_color="transparent"
    ).grid(row=0, column=0, pady=(60, 10))

    if icon:
        img_label = ctk.CTkLabel(
            left_frame,
            text="",
            image=icon,
            fg_color="transparent"
        )
        img_label.grid(row=1, column=0, pady=10)

    ctk.CTkLabel(
        left_frame,
        text="Pet Supplies & Care",
        text_color="#4a3428",
        font=("Segoe UI", 22),
        fg_color="transparent"
    ).grid(row=2, column=0, pady=(10, 60))

    # ---------- RIGHT CARD ----------
    right_frame = ctk.CTkFrame(
        main_frame,
        fg_color="#fca265",
        corner_radius=40    
    )
    right_frame.grid(row=0, column=1, sticky="nsew", padx=(30, 60), pady=80)

    right_frame.grid_rowconfigure((0, 1, 2, 3), weight=1)
    right_frame.grid_columnconfigure(0, weight=1)

    ctk.CTkLabel(
        right_frame,
        text="Welcome!",
        text_color="#2b1d14",
        font=("Segoe UI", 36, "bold"),
        fg_color="transparent"
    ).grid(row=0, column=0, pady=(50, 0))

    ctk.CTkButton(
        right_frame,
        text="Login",
        width=280,
        height=70,
        corner_radius=35,
        fg_color="#fed9bf",
        hover_color="#ffc9a3",
        text_color="#2b1d14",
        font=("Segoe UI", 26, "bold"),
        command=lambda: show_frame("login")
    ).grid(row=1, column=0, pady=15)

    ctk.CTkButton(
        right_frame,
        text="Register",
        width=280,
        height=70,
        corner_radius=35,
        fg_color="#fed9bf",
        hover_color="#ffc9a3",
        text_color="#2b1d14",
        font=("Segoe UI", 26, "bold"),
        command=lambda: show_frame("register")
    ).grid(row=2, column=0, pady=15)

    ctk.CTkLabel(
        right_frame,
        text="Your one-stop pet shop 🐱🐶",
        text_color="#5c4033",
        font=("Segoe UI", 16),
        fg_color="transparent"
    ).grid(row=3, column=0, pady=(0, 40))

    # =====================================================
    # CREATE OTHER SCREENS
    # =====================================================
    login_frame = login.login_screen(container, show_frame, refresh_user_screen)
    login_frame.grid(row=0, column=0, sticky="nsew")
    frames["login"] = login_frame

    register_frame = register.register_screen(container, show_frame)
    register_frame.grid(row=0, column=0, sticky="nsew")
    frames["register"] = register_frame

    user_frame = user.user_screen(container, show_frame)
    user_frame.grid(row=0, column=0, sticky="nsew")
    frames["user"] = user_frame

    admin_frame = admin.create_admin_frame(container, show_frame)
    admin_frame.grid(row=0, column=0, sticky="nsew")
    frames["admin"] = admin_frame

    # Start
    show_frame("main")
    app.mainloop()


if __name__ == "__main__":
    main()