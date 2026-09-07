import customtkinter as ctk
from tkinter import messagebox
import os
import db


# =====================================================
# CART
# =====================================================

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
        price = float(product[2])

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
                text=f"₹{subtotal:.2f}"
            ).pack(anchor="w", padx=20)

    total_label.configure(
        text=f"Total: ₹{total:.2f}"
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


# =====================================================
# PRODUCT CARD
# =====================================================

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
    price = float(product[2])
    brand = product[3]
    category = product[4]
    stock = int(product[5])

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


    # CATEGORY ICON

    if category == "Food":

        emoji = "🍖"

    elif category == "Toy":

        emoji = "🧸"

    elif category == "Accessory":

        emoji = "🎀"

    else:

        emoji = "🛍️"


    ctk.CTkLabel(
        image_frame,
        text=emoji,
        font=("Arial", 48)
    ).pack(expand=True)


    # PRODUCT NAME

    ctk.CTkLabel(
        card,
        text=name,
        font=("Arial", 18, "bold"),
        text_color="black"
    ).pack()


    # BRAND

    ctk.CTkLabel(
        card,
        text=f"Brand: {brand}",
        text_color="black"
    ).pack()


    # CATEGORY

    ctk.CTkLabel(
        card,
        text=f"Type: {category}",
        text_color="black"
    ).pack()


    # PRICE

    ctk.CTkLabel(
        card,
        text=f"₹{price:.2f}",
        font=("Arial", 18, "bold"),
        text_color="green"
    ).pack(pady=5)


    # STOCK STATUS

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


    # =================================================
    # QUANTITY CONTROLS
    # =================================================

    qty_frame = ctk.CTkFrame(
        card,
        fg_color="transparent"
    )

    qty_frame.pack(pady=10)


    qty_label = ctk.CTkLabel(
        qty_frame,
        text=str(cart.get(pid, 0)),
        width=30
    )


    minus_btn = ctk.CTkButton(
        qty_frame,
        text="-",
        width=35,
        command=lambda: remove_from_cart(
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
        command=lambda: add_to_cart(
            pid,
            stock,
            qty_label,
            cart_frame,
            total_label,
            products
        )
    )


    minus_btn.pack(
        side="left",
        padx=5
    )

    qty_label.pack(
        side="left",
        padx=5
    )

    plus_btn.pack(
        side="left",
        padx=5
    )


# =====================================================
# ORDER PAGE
# =====================================================

def create_order_page(
        parent,
        products,
        cart_frame,
        total_label):

    order_frame = ctk.CTkScrollableFrame(
        parent,
        fg_color="#ffe7d6"
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


# =====================================================
# SETTINGS
# =====================================================

def show_about_popup():

    popup = ctk.CTkToplevel()
    popup.focus()
    popup.grab_set()

    

    popup.geometry("400x300")

    popup.title("About")


    ctk.CTkLabel(
        popup,
        text="Pet Goods & Services",
        font=("Arial", 18, "bold")
    ).pack(pady=20)


    ctk.CTkLabel(
        popup,
        text=(
            "Version 1.0\n\n"
            "Your one-stop shop for all pet needs.\n"
            "Browse products, book services, and more!"
        ),
        font=("Arial", 11),
        justify="center"
    ).pack(pady=20)


    ctk.CTkButton(
        popup,
        text="Close",
        command=popup.destroy
    ).pack(pady=20)


def show_contact_popup():

    popup = ctk.CTkToplevel()
    popup.focus()
    popup.grab_set()

    popup.geometry("400x300")

    popup.title("Contact Support")


    ctk.CTkLabel(
        popup,
        text="Contact Support",
        font=("Arial", 18, "bold")
    ).pack(pady=20)


    ctk.CTkLabel(
        popup,
        text=(
            "Email: support@petshop.com\n"
            "Phone: +91 XXXXX XXXXX\n"
            "Support: Available during business hours"
        ),
        font=("Arial", 11),
        justify="center"
    ).pack(pady=20)


    ctk.CTkButton(
        popup,
        text="Close",
        command=popup.destroy
    ).pack(pady=20)


def show_faq_popup():

    popup = ctk.CTkToplevel()
    popup.focus()
    popup.grab_set()

    popup.geometry("450x400")

    popup.title("FAQ")


    ctk.CTkLabel(
        popup,
        text="Frequently Asked Questions",
        font=("Arial", 16, "bold")
    ).pack(pady=15)


    faq_text = """Q: How do I place an order?
A: Select products using + and add them to your cart.

Q: How do I book a service?
A: Go to the Book section.

Q: Can I change product quantity?
A: Yes, use the + and - buttons.

Q: What payment methods are accepted?
A: Contact the store for payment details."""


    ctk.CTkLabel(
        popup,
        text=faq_text,
        font=("Arial", 10),
        justify="left"
    ).pack(
        pady=15,
        padx=15
    )


    ctk.CTkButton(
        popup,
        text="Close",
        command=popup.destroy
    ).pack(pady=10)


def create_settings_page(
        parent,
        show_frame):

    settings_content = ctk.CTkScrollableFrame(
        parent,
        fg_color="#ffe7d6"
    )

    settings_content.pack(
        fill="both",
        expand=True
    )


    # TITLE

    ctk.CTkLabel(
        settings_content,
        text="Settings",
        text_color="black",
        font=("Arial", 36, "bold")
    ).pack(pady=(30, 20))


    # ACCOUNT

    account_frame = ctk.CTkFrame(
        settings_content,
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
        font=("Arial", 18, "bold")
    ).pack(
        anchor="w",
        padx=20,
        pady=(15, 10)
    )


    ctk.CTkLabel(
        account_frame,
        text="Pet Store Customer",
        text_color="#666"
    ).pack(
        anchor="w",
        padx=20,
        pady=(5, 15)
    )


    # PREFERENCES

    prefs_frame = ctk.CTkFrame(
        settings_content,
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
        font=("Arial", 18, "bold")
    ).pack(
        anchor="w",
        padx=20,
        pady=(15, 10)
    )


    notif_frame = ctk.CTkFrame(
        prefs_frame,
        fg_color="white"
    )

    notif_frame.pack(
        fill="x",
        padx=20,
        pady=10
    )


    ctk.CTkLabel(
        notif_frame,
        text="Enable Notifications",
        text_color="black"
    ).pack(side="left")


    ctk.CTkSwitch(
        notif_frame,
        text="",
        fg_color="#FA9A85",
        progress_color="#7ed957"
    ).pack(
        side="right",
        padx=10
    )


    # HELP

    help_frame = ctk.CTkFrame(
        settings_content,
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
        font=("Arial", 18, "bold")
    ).pack(
        anchor="w",
        padx=20,
        pady=(15, 10)
    )


    ctk.CTkButton(
        help_frame,
        text="About App",
        command=show_about_popup,
        fg_color="#FA9A85"
    ).pack(
        fill="x",
        padx=20,
        pady=5
    )


    ctk.CTkButton(
        help_frame,
        text="Contact Support",
        command=show_contact_popup,
        fg_color="#FA9A85"
    ).pack(
        fill="x",
        padx=20,
        pady=5
    )


    ctk.CTkButton(
        help_frame,
        text="FAQ",
        command=show_faq_popup,
        fg_color="#FA9A85"
    ).pack(
        fill="x",
        padx=20,
        pady=(5, 15)
    )


    # =================================================
    # LOGOUT
    # =================================================

    def logout():

        confirm = messagebox.askyesno(
            "Logout",
            "Are you sure you want to logout?"
        )

        if not confirm:
            return


        if os.path.exists("session.txt"):

            os.remove("session.txt")


        # Clear cart

        cart.clear()


        # Go to login screen

        show_frame("login")


    danger_frame = ctk.CTkFrame(
        settings_content,
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
        font=("Arial", 18, "bold")
    ).pack(
        anchor="w",
        padx=20,
        pady=(15, 10)
    )


    ctk.CTkButton(
        danger_frame,
        text="Logout",
        fg_color="tomato",
        hover_color="#FC846F",
        text_color="white",
        font=("Arial", 14, "bold"),
        height=45,
        command=logout
    ).pack(
        fill="x",
        padx=20,
        pady=(0, 15)
    )


# =====================================================
# PAGE SWITCHING INSIDE USER SCREEN
# =====================================================

def show_order(
        order_frame,
        book_frame,
        settings_frame):

    book_frame.pack_forget()

    settings_frame.pack_forget()

    order_frame.pack(
        fill="both",
        expand=True
    )


def show_book(
        order_frame,
        book_frame,
        settings_frame):

    order_frame.pack_forget()

    settings_frame.pack_forget()

    book_frame.pack(
        fill="both",
        expand=True
    )


def show_settings(
        order_frame,
        book_frame,
        settings_frame,
        show_frame):

    order_frame.pack_forget()

    book_frame.pack_forget()


    for widget in settings_frame.winfo_children():

        widget.destroy()


    create_settings_page(
        settings_frame,
        show_frame
    )


    settings_frame.pack(
        fill="both",
        expand=True
    )


# =====================================================
# NAVBAR
# =====================================================

def create_navbar(
        parent,
        order_frame,
        book_frame,
        settings_frame,
        show_frame):

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
        command=lambda: show_order(
            order_frame,
            book_frame,
            settings_frame
        )
    ).pack(
        side="left",
        padx=5
    )


    ctk.CTkButton(
        btn_frame,
        text="Book",
        fg_color="white",
        text_color="#FA9A85",
        hover_color="#f9d8d1",
        font=("Arial", 20, "bold"),
        command=lambda: show_book(
            order_frame,
            book_frame,
            settings_frame
        )
    ).pack(
        side="left",
        padx=5
    )


    ctk.CTkButton(
        btn_frame,
        text="Settings",
        fg_color="white",
        text_color="#FA9A85",
        hover_color="#f9d8d1",
        font=("Arial", 20, "bold"),
        command=lambda: show_settings(
            order_frame,
            book_frame,
            settings_frame,
            show_frame
        )
    ).pack(
        side="left",
        padx=5
    )


# =====================================================
# CART SIDEBAR
# =====================================================

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


    def checkout():

        if not cart or sum(cart.values()) == 0:

            messagebox.showwarning(
                "Cart Empty",
                "Please add products to your cart first."
            )

            return


        messagebox.showinfo(
            "Checkout",
            "Your order has been placed successfully!"
        )

        cart.clear()


    ctk.CTkButton(
        sidebar,
        text="Checkout",
        height=40,
        command=checkout
    ).pack(
        fill="x",
        padx=10,
        pady=10
    )


    return cart_items_frame, total_label


# =====================================================
# MAIN USER SCREEN
# =====================================================

def user_screen(container, show_frame):

    # Get latest products from database

    products = db.get_products()


    page = ctk.CTkFrame(
        container,
        fg_color="white"
    )


    page.grid(
        row=0,
        column=0,
        sticky="nsew"
    )


    # NAVBAR FIRST

    body = ctk.CTkFrame(
        page,
        fg_color="transparent"
    )

    body.pack(
        fill="both",
        expand=True
    )


    # CART

    cart_frame, total_label = create_cart_sidebar(
        body
    )


    # PRODUCTS AREA

    products_container = ctk.CTkFrame(
        body,
        fg_color="transparent"
    )

    products_container.pack(
        side="left",
        fill="both",
        expand=True
    )


    # ORDER PAGE

    order_frame = create_order_page(
        products_container,
        products,
        cart_frame,
        total_label
    )


    # BOOK PAGE

    book_frame = ctk.CTkFrame(
        products_container,
        fg_color="#ffe7d6"
    )


    ctk.CTkLabel(
        book_frame,
        text="Services Coming Soon",
        font=("Arial", 24, "bold"),
        text_color="black"
    ).pack(pady=50)


    # SETTINGS PAGE

    settings_frame = ctk.CTkFrame(
        products_container,
        fg_color="#ffe7d6"
    )


    # SHOW ORDER FIRST

    order_frame.pack(
        fill="both",
        expand=True
    )


    # REFRESH CART

    refresh_cart(
        cart_frame,
        total_label,
        products
    )


    # NAVBAR

    create_navbar(
        page,
        order_frame,
        book_frame,
        settings_frame,
        show_frame
    )


    return page