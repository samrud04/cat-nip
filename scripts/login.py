import customtkinter as ctk
import tkinter as tk
import db
import user, register

def login_screen(container, main_frame, show_frame, app):
    login = ctk.CTkFrame(container, fg_color="#ffe7d6", width=800, height=600)
    login.grid(row=0, column=0, sticky="nsew")

    register_frame = register.register_screen(container, main_frame, show_frame)

    login.grid_columnconfigure(0, weight=1)
    login.grid_columnconfigure(1, weight=1)
    login.grid_rowconfigure(0, weight=1)

    # ============ LEFT FRAME - FEATURES ============
    left_frame = ctk.CTkFrame(login, fg_color="#FA9A85", corner_radius=100)
    left_frame.grid(row=0, column=0, sticky="nsew", padx=(40, 20), pady=40)

    # Logo/Emoji
    ctk.CTkLabel(
        left_frame, 
        text="🐾", 
        text_color="black", 
        fg_color="#FA9A85", 
        font=("Arial", 80)
    ).pack(pady=(30, 10))

    # Brand Name
    ctk.CTkLabel(
        left_frame,
        text="Pet Goods &\nServices",
        text_color="black",
        fg_color="#FA9A85",
        font=("Arial", 40, "bold"),
        justify="center"
    ).pack(pady=(0, 30))

    # Features List
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
            fg_color="#FA9A85",
            font=("Arial", 25),
            justify="center"
        ).pack(pady=8, anchor="w", padx=30)

    # Tagline at bottom
    ctk.CTkLabel(
        left_frame,
        text="Join thousands of happy\npet owners today!",
        text_color="#fff5f0",
        fg_color="#FA9A85",
        font=("Arial", 28),
        justify="center"
    ).pack(pady=(50, 30))

    # ============ RIGHT FRAME - LOGIN FORM ============
    right_frame = ctk.CTkFrame(login, fg_color="#ffe7d6", corner_radius=30)
    right_frame.grid(row=0, column=1, sticky="nsew", padx=(20, 40), pady=40)

    # Title
    ctk.CTkLabel(
        right_frame,
        text="Login",
        text_color="black",
        fg_color="#ffe7d6",
        font=("Arial", 48, "bold")
    ).pack(pady=(40, 30))

    # Username Label
    ctk.CTkLabel(
        right_frame,
        text="Username:",
        text_color="black",
        fg_color="#ffe7d6",
        font=("Arial", 16, "bold")
    ).pack(anchor="w", padx=40, pady=(10, 0))

    # Username Entry
    login_uname_entry = ctk.CTkEntry(
        right_frame,
        width=250,
        fg_color="white",
        text_color="black",
        border_color="#FA9A85",
        border_width=2,
        font=("Arial", 13)
    )
    login_uname_entry.pack(padx=40, pady=(5, 20))

    # Password Label
    ctk.CTkLabel(
        right_frame,
        text="Password:",
        text_color="black",
        fg_color="#ffe7d6",
        font=("Arial", 16, "bold")
    ).pack(anchor="w", padx=40, pady=(0, 0))

    # Password Entry
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
    login_pwd_entry.pack(padx=40, pady=(5, 30))

    # Login handler
    def log_submit():
        username = login_uname_entry.get()
        password = login_pwd_entry.get()

        if not username or not password:
            tk.messagebox.showerror("Error", "Please fill all fields!")
        else:
            logged_In = db.login("user", username, password)
            
            if logged_In:
                user_id = db.get_user_id(username)
                
                # SAVE LOGIN
                with open("session.txt", "w") as f:
                    f.write(str(user_id))
                
                user_frame = user.user_screen(container, db.get_products(), app)
                show_frame(user_frame)
            else:
                tk.messagebox.showerror("Error", "Invalid credentials!")

    # Submit Button
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
    ).pack(pady=20)

    # Register Link
    link_frame = ctk.CTkFrame(right_frame, fg_color="#ffe7d6")
    link_frame.pack(pady=(10, 40))

    ctk.CTkLabel(
        link_frame,
        text="Don't have an account? ",
        text_color="black",
        fg_color="#ffe7d6",
        font=("Arial", 11)
    ).pack(side="left", padx=0)

    ctk.CTkButton(
        link_frame,
        text="Register",
        fg_color="#ffe7d6",
        text_color="#FA9A85",
        hover_color="white",
        font=("Arial", 11, "bold"),
        border_width=0,
        bg_color="#ffe7d6",
        command=lambda: show_frame(register_frame) # Go to register
    ).pack(side="left", padx=0)

    # ============ BACK BUTTON ============
    ctk.CTkButton(
        left_frame,
        text="←",
        command=lambda: show_frame(main_frame),
        width=50,
        height=50,
        fg_color="tomato",
        text_color="black",
        hover_color="#FC846F",
        font=("Arial", 40, "bold"),
        corner_radius=50
    ).place(x=50, y=50)

    return login
