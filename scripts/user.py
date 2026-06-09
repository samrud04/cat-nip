import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox

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

    ctk.CTkLabel(
        image_frame,
        text="Product Image"
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


def create_navbar(parent):

    navbar = ctk.CTkFrame(
        parent,
        height=70,
        fg_color="#ff6b29",
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
        text_color="#ff6b29",
        font=("Arial", 24, "bold")
    ).pack(side="left", padx=5)

    ctk.CTkButton(
        btn_frame,
        text="Book",
        fg_color="white",
        text_color="#ff6b29"
    ).pack(side="left", padx=5)

    ctk.CTkButton(
        btn_frame,
        text="Settings",
        fg_color="white",
        text_color="#ff6b29"
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


def user_screen(container, products):

    page = ctk.CTkFrame(
        container,
        fg_color="white"
    )

    page.grid(
        row=0,
        column=0,
        sticky="nsew"
    )

    create_navbar(page)

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

    create_order_page(
        products_container,
        products,
        cart_frame,
        total_label
    )

    refresh_cart(
        cart_frame,
        total_label,
        products
    )

    return page