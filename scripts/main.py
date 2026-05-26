from turtle import color
import customtkinter as ctk
import tkinter as tk
import db
import re
from PIL import Image, ImageTk

def show_frame(frame):
    frame.tkraise()


def main():
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


    # ---------------- HOME SCREEN ----------------
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
        command=lambda: show_frame(login)
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


    # ---------------- LOGIN SCREEN ----------------
    login = ctk.CTkFrame(container, fg_color="white", width=800, height=600)
    login.grid(row=0, column=0, sticky="nsew")

    login.grid_columnconfigure(0, weight=1)
    login.grid_columnconfigure(1, weight=1)
    login.grid_rowconfigure(0, weight=1)

    login_lframe = ctk.CTkFrame(login, fg_color="#ffe683",width=200, height=300)
    login_lframe.grid(row=0, column=0, sticky="nsew",padx=(40,40), pady=40)

    login_rframe = ctk.CTkFrame(login, fg_color="#feefb5", width=300, height=600)
    login_rframe.grid(row=0, column=1, sticky="nsew",padx=(0,40), pady=40)

    ctk.CTkLabel(login_lframe, text="Login", fg_color="#ffe683", text_color="black", font=("Arial", 64, "bold")).place(x=220, y=100)

    # User type radio buttons
    loginch = ctk.StringVar()
    loginch.set("user")
    ctk.CTkRadioButton(
        login_lframe, text="User",
        variable=loginch, value="user",
        fg_color="light blue",
        text_color="black",
        font=("Arial", 24, "bold")
    ).place(x=250, y=250)

    ctk.CTkRadioButton(
        login_lframe, text="Employee",
        variable=loginch, value="employee",
        fg_color="light blue",
        text_color="black",
        font=("Arial", 24, "bold")
    ).place(x=250, y=350)

    ctk.CTkRadioButton(
        login_lframe, text="Admin",
        variable=loginch, value="admin",
        fg_color="light blue",
        text_color="black",
        font=("Arial", 24, "bold")
    ).place(x=250, y=450)

    # Login fields
    ctk.CTkLabel(login_rframe, text="Username:",text_color="black", fg_color="#feefb5", font=("Arial", 34, "bold")).place(x=180, y=250)
    login_uname_entry = ctk.CTkEntry(login_rframe, width=150, fg_color="white", text_color="black")
    login_uname_entry.place(x=420, y=257)

    ctk.CTkLabel(login_rframe, text="Password:",text_color="black", fg_color="#feefb5", font=("Arial", 34, "bold")).place(x=180, y=320)
    login_pwd_entry = ctk.CTkEntry(login_rframe, show="*", width=150, fg_color="white", text_color="black")
    login_pwd_entry.place(x=420, y=327)

    def log_submit():
        username = login_uname_entry.get()
        password = login_pwd_entry.get()
        user_type = loginch.get()
        if not username or not password or not user_type:
            tk.messagebox.showerror("Error", "Please fill all fields!")
            return
        else:
            logged_In = db.login(user_type, username, password)
            if logged_In:
                show_frame(user_screen)
            else:
                tk.messagebox.showerror("Error", "Invalid credentials!")

    ctk.CTkButton(
        login_rframe,
        text="Submit",
        command=log_submit,
        fg_color="#7ed957",
        text_color="black",
        hover_color="#99D980",
        font=("Arial", 16, "bold")
    ).place(x=280, y=400)   

    ctk.CTkButton(
        login,
        text="Back",
        command=lambda: show_frame(main_frame),
        width=100,
        height=40,
        fg_color="tomato",
        text_color="black",
        hover_color="#FC846F",
        bg_color="#ffde59",
        font=("Arial", 16, "bold")
    ).place(x=80,y=80)

    ctk.CTkButton(
        login_rframe,  
        text="user screen",
        command=lambda: show_frame(user_screen),
        width=150,
        height=40,
        fg_color="#7ed957",
        text_color="black",
        hover_color="#99D980",
        font=("Arial", 16, "bold")
    ).place(x=280, y=450)


    # ---------------- REGISTER SCREEN ----------------

    register_frame = ctk.CTkFrame(container, fg_color="#ffe683", bg_color="white", width=800, height=600)
    register_frame.grid(row=0, column=0, sticky="nsew",padx=40, pady=40)
    register_frame.grid_rowconfigure(0, weight=1)
    register_frame.grid_columnconfigure(0, weight=1)


    ctk.CTkLabel(
        register_frame,
        text="User Registration",
        font=("Arial",56,"bold"),
        text_color="black"
    ).place(x=800,y=80)

    ctk.CTkLabel(register_frame, text="Username:", text_color="black",font=("Arial",29)).place(x=200,y=150)
    register_uname_entry = ctk.CTkEntry(register_frame, width=250, fg_color="white", text_color="black")
    register_uname_entry.place(x=370,y=153)

    ctk.CTkLabel(register_frame, text="Password:", text_color="black",font=("Arial",29)).place(x=200,y=230)
    register_pwd_entry = ctk.CTkEntry(register_frame, show="*", width=250, fg_color="white", text_color="black")
    register_pwd_entry.place(x=370,y=233)

    ctk.CTkLabel(register_frame,text="Confirm Password:", text_color="black",font=("Arial",29)).place(x=670,y=230)
    confirm_entry = ctk.CTkEntry(register_frame,show="*", width=250, fg_color="white", text_color="black")
    confirm_entry.place(x=920,y=233)

    ctk.CTkLabel(register_frame,text="Email:", text_color="black",font=("Arial",29)).place(x=200,y=310)
    email_entry = ctk.CTkEntry(register_frame, width=250, fg_color="white", text_color="black")
    email_entry.place(x=370,y=313)

    ctk.CTkLabel(register_frame,text="Phone:", text_color="black",font=("Arial",29)).place(x=670,y=310)
    phone_entry = ctk.CTkEntry(register_frame, width=100, fg_color="white", text_color="black")
    phone_entry.place(x=780,y=313)

    ctk.CTkLabel(register_frame,text="Address:", text_color="black",font=("Arial",29)).place(x=200,y=390)
    address_entry = ctk.CTkEntry(register_frame, width=800, fg_color="white", text_color="black")
    address_entry.place(x=370,y=393)

    ctk.CTkLabel(register_frame,text="Date of Birth:", text_color="black",font=("Arial",29)).place(x=200,y=470)
    dob_entry = ctk.CTkEntry(register_frame, width=80, fg_color="white", text_color="black")
    dob_entry.place(x=370,y=473)
    ctk.CTkLabel(register_frame,text="(YYYY-MM-DD)", text_color="black",font=("Arial",22)).place(x=200,y=510)

    ctk.CTkLabel(register_frame,text="Gender:", text_color="black",font=("Arial",29)).place(x=200,y=570)
    gender_entry = ctk.CTkEntry(register_frame, width=250, fg_color="white", text_color="black")
    gender_entry.place(x=370,y=573)

    textbox = ctk.CTkTextbox(register_frame, width=200, height=50, text_color="tomato", fg_color="white", border_color="tomato")

    def reg_submit():
        textbox.delete("0.0", "end")
        username = register_uname_entry.get()
        password = register_pwd_entry.get()
        confirm = confirm_entry.get()
        email = email_entry.get()
        phone = phone_entry.get()
        address = address_entry.get()
        gender = gender_entry.get()
        dob = dob_entry.get()
        pwd_check = password != confirm
        email_check = re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email) is None
        phone_check = re.match(r'^[6-9]\d{9}$', phone) is None
        if not username or not password or not confirm or not email or not phone or not address or not gender or not dob:
            tk.messagebox.showerror("Error", "Please fill all fields!")
        elif pwd_check:
            tk.messagebox.showerror("Error", "Passwords do not match!")
        elif email_check:
            textbox.insert("0.0", "Invalid email!\n")
        elif phone_check:   
            tk.messagebox.showerror("Error", "Invalid phone number! Must be 10 digits starting with 6-9.")
        else:
            registered = db.register(username, password, email, phone, address, gender, dob)
            if registered:
                tk.messagebox.showinfo("Success", "Registration successful! You can now log in.")
            else:
                tk.messagebox.showerror("Error", "Username already exists! Please choose a different one.")
        

    ctk.CTkButton(
        register_frame,
        text="Submit",
        command=reg_submit,
        text_color="black",
        fg_color="#7ed957",
        hover_color="#99D980",
        width=200,
        height=40,
        font=("Arial", 26, "bold")    
    ).place(x=800,y=500)

    ctk.CTkButton(
        register_frame,
        text="Back",
        command=lambda: show_frame(main_frame),
        width=100,
        height=40,
        fg_color="tomato",
        text_color="black",
        hover_color="#FC846F",
        bg_color="#ffea00",
        font=("Arial", 16, "bold")
    ).place(x=50,y=50)
    

    #----------------user screen----------------
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.geometry("1600x900")
    app.title("Pet Shop")

    # =========================
    # PRODUCT DATA
    # =========================

    products = [
        {"name": "Cat Food", "price": 250, "category": "Food"},
        {"name": "Fish Food", "price": 180, "category": "Food"},
        {"name": "Dog Collar", "price": 350, "category": "Accessories"},
        {"name": "Cat Treats", "price": 120, "category": "Food"},
        {"name": "Feather Toy", "price": 90, "category": "Toys"},
        {"name": "Scratching Post", "price": 550, "category": "Accessories"},
        {"name": "Dog Biscuits", "price": 200, "category": "Food"},
        {"name": "Cat Bed", "price": 700, "category": "Accessories"},
    ]

    cart = {}

    # =========================
    # MAIN USER SCREEN
    # =========================

    user_screen = ctk.CTkFrame(app, fg_color="white")
    user_screen.pack(fill="both", expand=True)

    user_screen.grid_rowconfigure(0, weight=1)
    user_screen.grid_columnconfigure(0, weight=1)

    # =========================
    # CONTENT FRAME
    # =========================

    content_frame = ctk.CTkFrame(
        user_screen,
        fg_color="#feefb5"
    )

    content_frame.grid(
        row=0,
        column=0,
        sticky="nsew",
        padx=40,
        pady=(40, 10)
    )

    content_frame.grid_rowconfigure(0, weight=1)
    content_frame.grid_columnconfigure(0, weight=1)

    # =========================
    # DIFFERENT SCREENS
    # =========================

    order_frame = ctk.CTkScrollableFrame(
        content_frame,
        fg_color="#feefb5"
    )

    book_frame = ctk.CTkFrame(
        content_frame,
        fg_color="#feefb5"
    )

    settings_frame = ctk.CTkFrame(
        content_frame,
        fg_color="#feefb5"
    )

    order_frame.grid(row=0, column=0, sticky="nsew")

    # =========================
    # NAVIGATION BAR
    # =========================

    user_screen_nav = ctk.CTkFrame(
        user_screen,
        fg_color="#fbe58c",
        height=80
    )

    user_screen_nav.grid(
        row=1,
        column=0,
        sticky="ew",
        padx=40,
        pady=(0, 40)
    )

    # =========================
    # NAVIGATION FUNCTION
    # =========================

    def show_screen(screen):

        order_frame.grid_forget()
        book_frame.grid_forget()
        settings_frame.grid_forget()

        screen.grid(row=0, column=0, sticky="nsew")

    # =========================
    # NAV BUTTONS
    # =========================

    order_button = ctk.CTkButton(
        user_screen_nav,
        text="Order",
        font=("Arial", 18, "bold"),
        width=250,
        height=60,
        fg_color="#f9b746",
        text_color="black",
        hover_color="#e0a73d",
        command=lambda: show_screen(order_frame)
    )

    order_button.pack(side="left", padx=40, pady=10)

    book_button = ctk.CTkButton(
        user_screen_nav,
        text="Book",
        font=("Arial", 18, "bold"),
        width=250,
        height=60,
        fg_color="#f9b746",
        text_color="black",
        hover_color="#e0a73d",
        command=lambda: show_screen(book_frame)
    )

    book_button.pack(side="left", padx=40, pady=10)

    settings_button = ctk.CTkButton(
        user_screen_nav,
        text="Settings",
        font=("Arial", 18, "bold"),
        width=250,
        height=60,
        fg_color="#f9b746",
        text_color="black",
        hover_color="#e0a73d",
        command=lambda: show_screen(settings_frame)
    )

    settings_button.pack(side="left", padx=40, pady=10)

    # =========================
    # SEARCH SECTION
    # =========================

    top_section = ctk.CTkFrame(
        order_frame,
        fg_color="#feefb5"
    )

    top_section.pack(fill="x", pady=20)

    search_label = ctk.CTkLabel(
        top_section,
        text="Search:",
        font=("Arial", 24, "bold"),
        text_color="black"
    )

    search_label.pack(side="left", padx=10)

    search_entry = ctk.CTkEntry(
        top_section,
        placeholder_text="Search products...",
        width=400,
        height=40,
        font=("Arial", 16)
    )

    search_entry.pack(side="left", padx=20)

    # =========================
    # MAIN SHOP AREA
    # =========================

    shop_container = ctk.CTkFrame(
        order_frame,
        fg_color="#feefb5"
    )

    shop_container.pack(fill="both", expand=True)

    # =========================
    # PRODUCTS AREA
    # =========================

    products_frame = ctk.CTkFrame(
        shop_container,
        fg_color="#feefb5"
    )

    products_frame.pack(side="left", fill="both", expand=True)

    # =========================
    # CART AREA
    # =========================

    cart_frame = ctk.CTkFrame(
        shop_container,
        width=350,
        fg_color="#fff4cc",
        corner_radius=20
    )

    cart_frame.pack(side="right", fill="y", padx=20, pady=20)

    cart_title = ctk.CTkLabel(
        cart_frame,
        text="Your Cart",
        font=("Arial", 28, "bold"),
        text_color="black"
    )

    cart_title.pack(pady=20)

    cart_items_frame = ctk.CTkScrollableFrame(
        cart_frame,
        width=300,
        height=500,
        fg_color="#fff4cc"
    )

    cart_items_frame.pack(padx=10, pady=10)

    total_label = ctk.CTkLabel(
        cart_frame,
        text="Total: ₹0",
        font=("Arial", 22, "bold"),
        text_color="green"
    )

    total_label.pack(pady=20)

    # =========================
    # CART FUNCTIONS
    # =========================

    def update_cart():

        for widget in cart_items_frame.winfo_children():
            widget.destroy()

        total = 0

        for product_name, details in cart.items():

            qty = details["qty"]
            price = details["price"]

            subtotal = qty * price
            total += subtotal

            item_frame = ctk.CTkFrame(
                cart_items_frame,
                fg_color="white",
                corner_radius=10
            )

            item_frame.pack(fill="x", pady=5, padx=5)

            item_label = ctk.CTkLabel(
                item_frame,
                text=f"{product_name}\n₹{price} x {qty} = ₹{subtotal}",
                font=("Arial", 14),
                text_color="black",
                justify="left"
            )

            item_label.pack(anchor="w", padx=10, pady=10)

        total_label.configure(text=f"Total: ₹{total}")

    # =========================
    # ADD / REMOVE FUNCTIONS
    # =========================

    def add_to_cart(product):

        name = product["name"]

        if name not in cart:
            cart[name] = {
                "price": product["price"],
                "qty": 1
            }
        else:
            cart[name]["qty"] += 1

        update_cart()

    def remove_from_cart(product):

        name = product["name"]

        if name in cart:

            cart[name]["qty"] -= 1

            if cart[name]["qty"] <= 0:
                del cart[name]

        update_cart()

    # =========================
    # PRODUCT CARD FUNCTION
    # =========================

    def create_product_card(parent, product):

        card = ctk.CTkFrame(
            parent,
            width=320,
            height=220,
            fg_color="white",
            corner_radius=20
        )

        card.pack(padx=20, pady=20)

        # PRODUCT NAME
        name_label = ctk.CTkLabel(
            card,
            text=product["name"],
            font=("Arial", 24, "bold"),
            text_color="black"
        )

        name_label.pack(pady=(20, 10))

        # CATEGORY
        category_label = ctk.CTkLabel(
            card,
            text=product["category"],
            font=("Arial", 16),
            text_color="gray"
        )

        category_label.pack()

        # PRICE
        price_label = ctk.CTkLabel(
            card,
            text=f"₹{product['price']}",
            font=("Arial", 22, "bold"),
            text_color="green"
        )

        price_label.pack(pady=10)

        # BUTTON AREA
        button_frame = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        button_frame.pack(pady=20)

        minus_button = ctk.CTkButton(
            button_frame,
            text="-",
            width=50,
            height=40,
            font=("Arial", 20, "bold"),
            fg_color="tomato",
            hover_color="#ff5c5c",
            command=lambda: remove_from_cart(product)
        )

        minus_button.pack(side="left", padx=10)

        plus_button = ctk.CTkButton(
            button_frame,
            text="+",
            width=50,
            height=40,
            font=("Arial", 20, "bold"),
            fg_color="green",
            hover_color="#009933",
            command=lambda: add_to_cart(product)
        )

        plus_button.pack(side="left", padx=10)

    # =========================
    # DISPLAY PRODUCTS
    # =========================

    for item in products:
        create_product_card(products_frame, item)

    # =========================
    # BOOK SCREEN
    # =========================

    book_label = ctk.CTkLabel(
        book_frame,
        text="BOOK SCREEN",
        font=("Arial", 42, "bold"),
        text_color="black"
    )

    book_label.pack(pady=300)

    # =========================
    # SETTINGS SCREEN
    # =========================

    settings_label = ctk.CTkLabel(
        settings_frame,
        text="SETTINGS SCREEN",
        font=("Arial", 42, "bold"),
        text_color="black"
    )

    settings_label.pack(pady=300)

    # Start on home
    show_frame(main_frame)

    app.mainloop()


if __name__ == "__main__":
    main()