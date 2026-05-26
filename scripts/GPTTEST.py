import customtkinter as ctk
from PIL import Image

# ---------- FRAME SWITCHING ----------
def show_frame(frame):
    frame.tkraise()


# ---------- HOME SCREEN ----------
def create_home_screen(container, login_frame, register_frame):

    home_frame = ctk.CTkFrame(
        container,
        fg_color="#fffdf6"
    )

    home_frame.grid(row=0, column=0, sticky="nsew")

    # Responsive layout
    home_frame.grid_columnconfigure(0, weight=1)
    home_frame.grid_columnconfigure(1, weight=1)
    home_frame.grid_rowconfigure(0, weight=1)

    # ---------- LEFT SECTION ----------
    left_section = ctk.CTkFrame(
        home_frame,
        fg_color="#ffe683",
        corner_radius=30
    )

    left_section.grid(
        row=0,
        column=0,
        sticky="nsew",
        padx=(40, 20),
        pady=40
    )

    left_section.grid_rowconfigure((0, 1, 2), weight=1)
    left_section.grid_columnconfigure(0, weight=1)

    # App Logo
    logo_image = ctk.CTkImage(
        light_image=Image.open("assets/catnipico.png"),
        size=(280, 280)
    )

    logo_label = ctk.CTkLabel(
        left_section,
        image=logo_image,
        text=""
    )

    logo_label.grid(row=0, column=0, pady=(60, 10))

    # Title
    title_label = ctk.CTkLabel(
        left_section,
        text="Cat-Nip",
        font=("Arial", 64, "bold"),
        text_color="#2b2b2b"
    )

    title_label.grid(row=1, column=0, pady=(0, 10))

    # Subtitle
    subtitle_label = ctk.CTkLabel(
        left_section,
        text="Everything your cat deserves 🐾",
        font=("Arial", 22),
        text_color="#4a4a4a"
    )

    subtitle_label.grid(row=2, column=0, pady=(0, 60))

    # ---------- RIGHT SECTION ----------
    right_section = ctk.CTkFrame(
        home_frame,
        fg_color="#ffffff",
        corner_radius=30
    )

    right_section.grid(
        row=0,
        column=1,
        sticky="nsew",
        padx=(20, 40),
        pady=40
    )

    right_section.grid_columnconfigure(0, weight=1)

    # Welcome text
    welcome_label = ctk.CTkLabel(
        right_section,
        text="Welcome",
        font=("Arial", 48, "bold"),
        text_color="#2b2b2b"
    )

    welcome_label.pack(pady=(120, 20))

    desc_label = ctk.CTkLabel(
        right_section,
        text="Login or create an account to continue",
        font=("Arial", 20),
        text_color="#666666"
    )

    desc_label.pack(pady=(0, 60))

    # ---------- LOGIN BUTTON ----------
    login_button = ctk.CTkButton(
        right_section,
        text="Login",
        width=320,
        height=65,
        corner_radius=18,
        fg_color="#f9c74f",
        hover_color="#f4b942",
        text_color="black",
        font=("Arial", 28, "bold"),
        command=lambda: show_frame(login_frame)
    )

    login_button.pack(pady=20)

    # ---------- REGISTER BUTTON ----------
    register_button = ctk.CTkButton(
        right_section,
        text="Create Account",
        width=320,
        height=65,
        corner_radius=18,
        fg_color="#ffffff",
        border_width=3,
        border_color="#f9c74f",
        hover_color="#fff4cc",
        text_color="black",
        font=("Arial", 28, "bold"),
        command=lambda: show_frame(register_frame)
    )

    register_button.pack(pady=10)

    # Footer
    footer_label = ctk.CTkLabel(
        right_section,
        text="Cat-Nip © 2026",
        font=("Arial", 14),
        text_color="#999999"
    )

    footer_label.pack(side="bottom", pady=30)

    return home_frame

container = ctk.CTk()
container.geometry("1200x800")
container.title("Cat-Nip")

login_frame = ctk.CTkFrame(container)
register_frame = ctk.CTkFrame(container)

home_frame = create_home_screen(
    container,
    login_frame,
    register_frame
)

show_frame(home_frame)