import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import main, login

cart = {}

def refresh_cart(cart_frame, total_label, products):

    for widget in cart_frame.winfo_children():
        widget.destroy()

    total = 0

    ctk.CTkLabel(
        cart_frame,
        text="🛒 Cart",
        font=("Arial", 22, "bold")
    ).pack(pady=10)

    for product in products:

        pid = product[0]
        name = product[1]
        price = product[2]

        if pid in cart and cart[pid] > 0:

            qty = cart[pid]
            subtotal = qty * price

            total += subtotal

            ctk.CTkLabel(
                cart_frame,
                text=f"{name} x{qty}"
            ).pack(anchor="w", padx=10)

            ctk.CTkLabel(
                cart_frame,
                text=f"₹{subtotal}"
            ).pack(anchor="w", padx=20)

    total_label.configure(
        text=f"Total: ₹{total}"
    )


def add_to_cart(
        product_id,
        stock,
        qty_label,
        cart_frame,
        total_label,
        products):

    current_qty = cart.get(product_id, 0)

    if current_qty >= stock:
        messagebox.showwarning(
            "Stock Limit",
            "Cannot add more than available stock."
        )
        return

    cart[product_id] = current_qty + 1

    qty_label.configure(
        text=str(cart[product_id])
    )

    refresh_cart(
        cart_frame,
        total_label,
        products
    )


def remove_from_cart(
        product_id,
        qty_label,
        cart_frame,
        total_label,
        products):

    if product_id not in cart:
        return

    if cart[product_id] > 0:
        cart[product_id] -= 1

    qty_label.configure(
        text=str(cart[product_id])
    )

    refresh_cart(
        cart_frame,
        total_label,
        products
    )


def create_product_card(
        parent,
        product,
        row,
        column,
        cart_frame,
        total_label,
        products):

    pid = product[0]
    name = product[1]
    price = product[2]
    brand = product[3]
    category = product[4]
    stock = product[5]

    card = ctk.CTkFrame(
        parent,
        width=230,
        height=330,
        fg_color="white",
        corner_radius=20
    )

    card.grid(
        row=row,
        column=column,
        padx=10,
        pady=10,
        sticky="n"
    )

    card.grid_propagate(False)

    image_frame = ctk.CTkFrame(
        card,
        width=180,
        height=100,
        fg_color="#CFE7FF"
    )

    image_frame.pack(pady=10)

    image_frame.pack_propagate(False)

    if category == "Food":
        ctk.CTkLabel(
            image_frame,
            text="🍖",
            font=("Arial", 48)
        ).pack(expand=True)
    elif category == "Toy":
        ctk.CTkLabel(
            image_frame,
            text="🧸",
            font=("Arial", 48)
        ).pack(expand=True)
    elif category == "Accessory":
        ctk.CTkLabel(
            image_frame,
            text="🎀",
            font=("Arial", 48)
        ).pack(expand=True)
    else:
        ctk.CTkLabel(
            image_frame,
            text="🛍️",
            font=("Arial", 48)
        ).pack(expand=True)

    ctk.CTkLabel(
        card,
        text=name,
        font=("Arial", 18, "bold")
    ).pack()

    ctk.CTkLabel(
        card,
        text=f"Brand: {brand}"
    ).pack()

    ctk.CTkLabel(
        card,
        text=f"Type: {category}"
    ).pack()

    ctk.CTkLabel(
        card,
        text=f"₹{price}",
        font=("Arial", 18, "bold"),
        text_color="green"
    ).pack(pady=5)

    if stock <= 0:

        stock_text = "Out of Stock"
        stock_color = "red"

    elif stock <= 10:

        stock_text = f"Only {stock} left!"
        stock_color = "orange"

    else:

        stock_text = "Available"
        stock_color = "green"

    ctk.CTkLabel(
        card,
        text=stock_text,
        text_color=stock_color
    ).pack()

    qty_frame = ctk.CTkFrame(
        card,
        fg_color="transparent"
    )

    qty_frame.pack(pady=10)

    qty_label = ctk.CTkLabel(
        qty_frame,
        text="0",
        width=30
    )

    minus_btn = ctk.CTkButton(
        qty_frame,
        text="-",
        width=35,
        command=lambda:
        remove_from_cart(
            pid,
            qty_label,
            cart_frame,
            total_label,
            products
        )
    )

    plus_btn = ctk.CTkButton(
        qty_frame,
        text="+",
        width=35,
        command=lambda:
        add_to_cart(
            pid,
            stock,
            qty_label,
            cart_frame,
            total_label,
            products
        )
    )

    minus_btn.pack(side="left", padx=5)
    qty_label.pack(side="left", padx=5)
    plus_btn.pack(side="left", padx=5)


def create_order_page(
        parent,
        products,
        cart_frame,
        total_label):

    order_frame = ctk.CTkScrollableFrame(
        parent,
        fg_color="#ffe7d6"
    )

    order_frame.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

    for col in range(4):
        order_frame.grid_columnconfigure(
            col,
            weight=1
        )

    for index, product in enumerate(products):

        row = index // 4
        column = index % 4

        create_product_card(
            order_frame,
            product,
            row,
            column,
            cart_frame,
            total_label,
            products
        )

    return order_frame

def logout(show_frame, login_screen, container, main_frame):
    """Delete session and go back to login"""
    import os
    if os.path.exists("session.txt"):
        os.remove("session.txt")
    
    show_frame(login_screen(container, main_frame, show_frame))


def create_settings_page(parent, show_frame, login_screen, container, main_frame, user_id):
    """
    Create settings page with user info and logout button
    parent: container to pack into
    show_frame: function to switch frames
    login_screen: login screen function
    container: main container
    main_frame: main frame reference
    user_id: current logged in user's ID
    """
    
    settings_frame = ctk.CTkScrollableFrame(
        parent,
        fg_color="#ffe7d6"
    )
    
    settings_frame.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )
    
    # ============ TITLE ============
    ctk.CTkLabel(
        settings_frame,
        text="Settings",
        text_color="black",
        fg_color="#ffe7d6",
        font=("Arial", 36, "bold")
    ).pack(pady=(30, 20))
    
    # ============ ACCOUNT SECTION ============
    account_frame = ctk.CTkFrame(
        settings_frame,
        fg_color="white",
        corner_radius=15
    )
    account_frame.pack(
        fill="x",
        padx=20,
        pady=15
    )
    
    ctk.CTkLabel(
        account_frame,
        text="Account Information",
        text_color="black",
        fg_color="white",
        font=("Arial", 18, "bold")
    ).pack(anchor="w", padx=20, pady=(15, 10))
    
    # User ID display
    ctk.CTkLabel(
        account_frame,
        text=f"User ID: {user_id}",
        text_color="#666",
        fg_color="white",
        font=("Arial", 12)
    ).pack(anchor="w", padx=20, pady=5)
    
    # Username (you can fetch from DB if needed)
    ctk.CTkLabel(
        account_frame,
        text="Username: (Your username here)",
        text_color="#666",
        fg_color="white",
        font=("Arial", 12)
    ).pack(anchor="w", padx=20, pady=(5, 15))
    
    # ============ PREFERENCES SECTION ============
    prefs_frame = ctk.CTkFrame(
        settings_frame,
        fg_color="white",
        corner_radius=15
    )
    prefs_frame.pack(
        fill="x",
        padx=20,
        pady=15
    )
    
    ctk.CTkLabel(
        prefs_frame,
        text="Preferences",
        text_color="black",
        fg_color="white",
        font=("Arial", 18, "bold")
    ).pack(anchor="w", padx=20, pady=(15, 10))
    
    # Notifications toggle
    notif_frame = ctk.CTkFrame(prefs_frame, fg_color="white")
    notif_frame.pack(fill="x", padx=20, pady=10)
    
    ctk.CTkLabel(
        notif_frame,
        text="Enable Notifications",
        text_color="black",
        fg_color="white",
        font=("Arial", 12)
    ).pack(side="left")
    
    notif_switch = ctk.CTkSwitch(
        notif_frame,
        text="",
        fg_color="#FA9A85",
        progress_color="#7ed957"
    )
    notif_switch.pack(side="right", padx=10)
    
    # Email preferences toggle
    email_frame = ctk.CTkFrame(prefs_frame, fg_color="white")
    email_frame.pack(fill="x", padx=20, pady=10)
    
    ctk.CTkLabel(
        email_frame,
        text="Email Updates",
        text_color="black",
        fg_color="white",
        font=("Arial", 12)
    ).pack(side="left")
    
    email_switch = ctk.CTkSwitch(
        email_frame,
        text="",
        fg_color="#FA9A85",
        progress_color="#7ed957"
    )
    email_switch.pack(side="right", padx=10)
    
    # ============ HELP SECTION ============
    help_frame = ctk.CTkFrame(
        settings_frame,
        fg_color="white",
        corner_radius=15
    )
    help_frame.pack(
        fill="x",
        padx=20,
        pady=15
    )
    
    ctk.CTkLabel(
        help_frame,
        text="Help & Support",
        text_color="black",
        fg_color="white",
        font=("Arial", 18, "bold")
    ).pack(anchor="w", padx=20, pady=(15, 10))
    
    # About button
    ctk.CTkButton(
        help_frame,
        text="About App",
        fg_color="#FA9A85",
        text_color="white",
        hover_color="#E67D68",
        font=("Arial", 12),
        corner_radius=10,
        height=35,
        command=lambda: show_about_popup()
    ).pack(fill="x", padx=20, pady=5)
    
    # Contact button
    ctk.CTkButton(
        help_frame,
        text="Contact Support",
        fg_color="#FA9A85",
        text_color="white",
        hover_color="#E67D68",
        font=("Arial", 12),
        corner_radius=10,
        height=35,
        command=lambda: show_contact_popup()
    ).pack(fill="x", padx=20, pady=5)
    
    # FAQ button
    ctk.CTkButton(
        help_frame,
        text="FAQ",
        fg_color="#FA9A85",
        text_color="white",
        hover_color="#E67D68",
        font=("Arial", 12),
        corner_radius=10,
        height=35,
        command=lambda: show_faq_popup()
    ).pack(fill="x", padx=20, pady=(5, 15))
    
    # ============ DANGER ZONE ============
    danger_frame = ctk.CTkFrame(
        settings_frame,
        fg_color="white",
        corner_radius=15
    )
    danger_frame.pack(
        fill="x",
        padx=20,
        pady=15
    )
    
    ctk.CTkLabel(
        danger_frame,
        text="Account",
        text_color="black",
        fg_color="white",
        font=("Arial", 18, "bold")
    ).pack(anchor="w", padx=20, pady=(15, 10))
    
    # Logout button
    ctk.CTkButton(
        danger_frame,
        text="Logout",
        fg_color="tomato",
        text_color="white",
        hover_color="#FC846F",
        font=("Arial", 14, "bold"),
        corner_radius=10,
        height=45,
        command=lambda: logout(show_frame, login_screen, container, main_frame)
    ).pack(fill="x", padx=20, pady=10)
    
    # Delete account button (optional - uncomment if you want it)
    # ctk.CTkButton(
    #     danger_frame,
    #     text="Delete Account",
    #     fg_color="#C0392B",
    #     text_color="white",
    #     hover_color="#A93226",
    #     font=("Arial", 12),
    #     corner_radius=10,
    #     height=35,
    #     command=lambda: confirm_delete_account()
    # ).pack(fill="x", padx=20, pady=(10, 15))
    
    return settings_frame


# ============ POPUP HELPER FUNCTIONS ============

def show_about_popup():
    """Show about app popup"""
    popup = ctk.CTkToplevel()
    popup.geometry("400x300")
    popup.title("About")
    
    ctk.CTkLabel(
        popup,
        text="Pet Goods & Services",
        text_color="black",
        font=("Arial", 18, "bold")
    ).pack(pady=20)
    
    ctk.CTkLabel(
        popup,
        text="Version 1.0\n\nYour one-stop shop for all pet needs.\nBrowse products, book services, and more!",
        text_color="#666",
        font=("Arial", 11),
        justify="center"
    ).pack(pady=20)
    
    ctk.CTkButton(
        popup,
        text="Close",
        command=popup.destroy
    ).pack(pady=20)


def show_contact_popup():
    """Show contact support popup"""
    popup = ctk.CTkToplevel()
    popup.geometry("400x300")
    popup.title("Contact Support")
    
    ctk.CTkLabel(
        popup,
        text="Contact Support",
        text_color="black",
        font=("Arial", 18, "bold")
    ).pack(pady=20)
    
    ctk.CTkLabel(
        popup,
        text="Email: support@petshop.com\nPhone: +1 (800) PET-SHOP\nLive Chat: Available 9AM-6PM",
        text_color="#666",
        font=("Arial", 11),
        justify="center"
    ).pack(pady=20)
    
    ctk.CTkButton(
        popup,
        text="Close",
        command=popup.destroy
    ).pack(pady=20)


def show_faq_popup():
    """Show FAQ popup"""
    popup = ctk.CTkToplevel()
    popup.geometry("450x400")
    popup.title("FAQ")
    
    ctk.CTkLabel(
        popup,
        text="Frequently Asked Questions",
        text_color="black",
        font=("Arial", 16, "bold")
    ).pack(pady=15)
    
    faq_text = """Q: How do I place an order?
A: Click on any product, select quantity, and add to cart.

Q: How do I book a service?
A: Go to Services tab, select service, and choose date.

Q: Can I cancel my order?
A: Yes, within 24 hours of placing it.

Q: What payment methods do you accept?
A: We accept all major credit/debit cards.

Q: How long does delivery take?
A: 3-5 business days for most orders."""
    
    ctk.CTkLabel(
        popup,
        text=faq_text,
        text_color="#666",
        font=("Arial", 10),
        justify="left"
    ).pack(pady=15, padx=15)
    
    ctk.CTkButton(
        popup,
        text="Close",
        command=popup.destroy
    ).pack(pady=10)

def show_order(order_frame, book_frame, settings_frame):

    book_frame.pack_forget()
    settings_frame.pack_forget()

    order_frame.pack(
        fill="both",
        expand=True
    )

def show_settings(page, app, order_frame, book_frame, settings_frame, products, cart_frame, total_label):

    order_frame.pack_forget()
    book_frame.pack_forget()

    # Clear old settings content if any
    for widget in settings_frame.winfo_children():
        widget.destroy()

    user_id = main.check_logged_in()

    settings_content = create_settings_page(
        parent=settings_frame,
        show_frame=main.show_frame,
        login_screen=login.login_screen,
        container=app,
        main_frame=page,
        user_id=user_id
    )

    settings_frame.pack(
        fill="both",
        expand=True
    )

def show_book(order_frame, book_frame, settings_frame):

    order_frame.pack_forget()
    settings_frame.pack_forget()

    book_frame.pack(
        fill="both",
        expand=True
    )

def create_navbar(parent, app, order_frame, book_frame, settings_frame, products, cart_frame, total_label):

    navbar = ctk.CTkFrame(
        parent,
        height=70,
        fg_color="#FA9A85",
        corner_radius=0
    )

    navbar.pack(fill="x")

    ctk.CTkLabel(
        navbar,
        text="🐾 Pet Supplies",
        font=("Arial", 28, "bold"),
        text_color="white"
    ).pack(
        side="left",
        padx=20,
        pady=15
    )

    btn_frame = ctk.CTkFrame(
        navbar,
        fg_color="transparent"
    )

    btn_frame.pack(
        side="right",
        padx=20
    )

    ctk.CTkButton(
        btn_frame,
        text="Order",
        fg_color="white",
        text_color="#FA9A85",
        hover_color="#f9d8d1",
        font=("Arial", 20, "bold"),
        command=lambda: show_order(order_frame, book_frame, settings_frame)
    ).pack(side="left", padx=5)

    ctk.CTkButton(
        btn_frame,
        text="Book",
        fg_color="white",
        text_color="#FA9A85",
        hover_color="#f9d8d1",
        font=("Arial", 20, "bold"),
        command=lambda: show_book(order_frame, book_frame, settings_frame)
    ).pack(side="left", padx=5)

    ctk.CTkButton(
        btn_frame,
        text="Settings",
        fg_color="white",
        text_color="#FA9A85",
        hover_color="#f9d8d1",
        font=("Arial", 20, "bold"),
        command=lambda: show_settings(parent, app, order_frame, book_frame, settings_frame, products, cart_frame, total_label)
    ).pack(side="left", padx=5)


def create_cart_sidebar(parent):

    sidebar = ctk.CTkFrame(
        parent,
        width=280,
        fg_color="white"
    )

    sidebar.pack(
        side="right",
        fill="y",
        padx=10,
        pady=10
    )

    cart_items_frame = ctk.CTkScrollableFrame(
        sidebar,
        width=240,
        height=500
    )

    cart_items_frame.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

    total_label = ctk.CTkLabel(
        sidebar,
        text="Total: ₹0",
        font=("Arial", 20, "bold")
    )

    total_label.pack(pady=10)

    ctk.CTkButton(
        sidebar,
        text="Checkout",
        height=40
    ).pack(
        fill="x",
        padx=10,
        pady=10
    )

    return cart_items_frame, total_label


def user_screen(container, products, app):

    page = ctk.CTkFrame(
        container,
        fg_color="white"
    )

    page.grid(
        row=0,
        column=0,
        sticky="nsew"
    )

    body = ctk.CTkFrame(
        page,
        fg_color="transparent"
    )

    body.pack(
        fill="both",
        expand=True
    )

    cart_frame, total_label = create_cart_sidebar(
        body
    )

    products_container = ctk.CTkFrame(
        body,
        fg_color="transparent"
    )

    products_container.pack(
        side="left",
        fill="both",
        expand=True
    )

    order_frame = create_order_page(
        products_container,
        products,
        cart_frame,
        total_label
    )

    # Create book frame (services booking page - placeholder for now)
    book_frame = ctk.CTkFrame(
        body,
        fg_color="#ffe7d6"
    )
    
    ctk.CTkLabel(
        book_frame,
        text="Services Coming Soon",
        font=("Arial", 24, "bold"),
        text_color="black"
    ).pack(pady=50)

    # Create settings frame (will be filled by show_settings)
    settings_frame = ctk.CTkFrame(
        body,
        width=1300,
        fg_color="#ffe7d6"
    )

    refresh_cart(
        cart_frame,
        total_label,
        products
    )

    # Create navbar FIRST so it's on top
    create_navbar(page, app, order_frame, book_frame, settings_frame, products, cart_frame, total_label)

    return page