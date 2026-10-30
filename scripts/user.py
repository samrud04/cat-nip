import customtkinter as ctk
from tkinter import messagebox
import os
import html
import webbrowser
from pathlib import Path
import db
from adoption import open_adoption_window
from playdates import open_playdates_user
from chatbot import create_chatbot_page


# =====================================================
# GLOBAL VARIABLES
# =====================================================

cart = {}
current_user_id = None


# =====================================================
# LOAD USER CART
# =====================================================

def load_user_cart(user_id):

    global cart

    cart.clear()

    cart_items = db.get_cart(user_id)

    for item in cart_items:

        product_id = item[0]
        quantity = item[1]

        cart[product_id] = quantity


# =====================================================
# REFRESH CART
# =====================================================

def refresh_cart(cart_frame, total_label, products):

    for widget in cart_frame.winfo_children():
        widget.destroy()

    total = 0


    # Cart Title

    ctk.CTkLabel(
        cart_frame,
        text="🛒 Your Cart",
        font=("Arial", 22, "bold"),
        text_color="black"
    ).pack(pady=10)


    # Show Cart Items

    for product in products:

        product_id = product[0]
        name = product[1]
        price = float(product[2])

        if product_id in cart:

            quantity = cart[product_id]

            if quantity > 0:

                subtotal = quantity * price

                total += subtotal


                item_frame = ctk.CTkFrame(
                    cart_frame,
                    fg_color="#F5F5F5",
                    corner_radius=10
                )

                item_frame.pack(
                    fill="x",
                    padx=5,
                    pady=5
                )


                ctk.CTkLabel(
                    item_frame,
                    text=name,
                    text_color="black",
                    font=("Arial", 14, "bold")
                ).pack(
                    anchor="w",
                    padx=10,
                    pady=(5, 0)
                )


                ctk.CTkLabel(
                    item_frame,
                    text=f"Qty: {quantity}",
                    text_color="#555555"
                ).pack(
                    anchor="w",
                    padx=10
                )


                ctk.CTkLabel(
                    item_frame,
                    text=f"₹{subtotal:.2f}",
                    text_color="green",
                    font=("Arial", 14, "bold")
                ).pack(
                    anchor="w",
                    padx=10,
                    pady=(0, 5)
                )


    # Empty Cart

    if not cart:

        ctk.CTkLabel(
            cart_frame,
            text="Your cart is empty",
            text_color="gray"
        ).pack(pady=30)


    # Update Total

    total_label.configure(
        text=f"Total: ₹{total:.2f}"
    )


# =====================================================
# ADD TO CART
# =====================================================

def add_to_cart(
        product_id,
        stock,
        qty_label,
        cart_frame,
        total_label,
        products):

    global current_user_id


    current_quantity = cart.get(
        product_id,
        0
    )


    # Stock Check

    if stock <= 0:

        messagebox.showwarning(
            "Out of Stock",
            "This product is currently out of stock."
        )

        return


    if current_quantity >= stock:

        messagebox.showwarning(
            "Stock Limit",
            "Cannot add more than available stock."
        )

        return


    # Add to Database

    db.add_to_cart(
        current_user_id,
        product_id
    )


    # Update Local Cart

    cart[product_id] = current_quantity + 1


    # Update Label

    qty_label.configure(
        text=str(cart[product_id])
    )


    # Refresh Cart

    refresh_cart(
        cart_frame,
        total_label,
        products
    )


# =====================================================
# REMOVE FROM CART
# =====================================================

def remove_from_cart(
        product_id,
        qty_label,
        cart_frame,
        total_label,
        products):

    global current_user_id


    if product_id not in cart:
        return


    if cart[product_id] <= 0:
        return


    # Remove from Database

    db.remove_from_cart(
        current_user_id,
        product_id
    )


    # Update Local Cart

    cart[product_id] -= 1


    if cart[product_id] <= 0:

        del cart[product_id]

        qty_label.configure(
            text="0"
        )

    else:

        qty_label.configure(
            text=str(cart[product_id])
        )


    # Refresh Cart

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

    product_id = product[0]
    name = product[1]
    price = float(product[2])
    brand = product[3]
    category = product[4]
    stock = int(product[5])


    # PRODUCT CARD

    card = ctk.CTkFrame(
        parent,
        width=230,
        height=360,
        fg_color="white",
        corner_radius=20,
        border_width=1,
        border_color="#f0d9c8"
    )

    card.grid(
        row=row,
        column=column,
        padx=12,
        pady=12,
        sticky="n"
    )

    card.grid_propagate(False)


    # IMAGE AREA

    image_frame = ctk.CTkFrame(
        card,
        width=190,
        height=110,
        fg_color="#FFF0E6",
        corner_radius=16
    )

    image_frame.pack(
        pady=(18, 10)
    )

    image_frame.pack_propagate(False)


    # PRODUCT ICON

    name_lower = name.lower()
    category_lower = category.lower() if category else ""


    if "collar" in name_lower or "leash" in name_lower or "harness" in name_lower:

        emoji = "🦮"

    elif "food" in name_lower or category_lower == "food":

        emoji = "🍖"

    elif "toy" in name_lower or "ball" in name_lower or category_lower == "toy":

        emoji = "🎾"

    elif "bed" in name_lower or "cushion" in name_lower:

        emoji = "🛏️"

    elif "bowl" in name_lower or "feeder" in name_lower:

        emoji = "🥣"

    elif "shampoo" in name_lower or "groom" in name_lower or "brush" in name_lower:

        emoji = "🧴"

    elif "treat" in name_lower or "snack" in name_lower:

        emoji = "🦴"

    elif "cage" in name_lower or "carrier" in name_lower:

        emoji = "🏠"

    elif category_lower == "accessory":

        emoji = "🎀"

    else:

        emoji = "🛍️"


    ctk.CTkLabel(
        image_frame,
        text=emoji,
        font=("Segoe UI Emoji", 52)
    ).pack(expand=True)


    # PRODUCT NAME

    ctk.CTkLabel(
        card,
        text=name,
        font=("Segoe UI", 16, "bold"),
        text_color="#2b1d14",
        wraplength=200
    ).pack(
        pady=(5, 2)
    )


    # BRAND AND CATEGORY

    ctk.CTkLabel(
        card,
        text=f"{brand}  •  {category}",
        font=("Segoe UI", 12),
        text_color="#666666"
    ).pack()


    # PRICE

    ctk.CTkLabel(
        card,
        text=f"₹{price:.2f}",
        font=("Segoe UI", 18, "bold"),
        text_color="#2e7d32"
    ).pack(
        pady=6
    )


    # STOCK STATUS

    if stock <= 0:

        stock_text = "Out of Stock"
        stock_color = "#e53935"

    elif stock <= 10:

        stock_text = f"Only {stock} left!"
        stock_color = "#fb8c00"

    else:

        stock_text = f"In Stock ({stock})"
        stock_color = "#43a047"


    ctk.CTkLabel(
        card,
        text=stock_text,
        font=("Segoe UI", 13),
        text_color=stock_color
    ).pack()


    # QUANTITY CONTROLS

    quantity_frame = ctk.CTkFrame(
        card,
        fg_color="transparent"
    )

    quantity_frame.pack(
        pady=12
    )


    qty_label = ctk.CTkLabel(
        quantity_frame,
        text=str(cart.get(product_id, 0)),
        width=40,
        font=("Segoe UI", 16, "bold"),
        text_color="#2b1d14"
    )


    # MINUS BUTTON

    minus_button = ctk.CTkButton(
        quantity_frame,
        text="−",
        width=36,
        height=36,
        corner_radius=10,
        fg_color="#FA9A85",
        hover_color="#f08b75",
        text_color="white",
        font=("Segoe UI", 18, "bold"),
        command=lambda: remove_from_cart(
            product_id,
            qty_label,
            cart_frame,
            total_label,
            products
        )
    )


    # PLUS BUTTON

    plus_button = ctk.CTkButton(
        quantity_frame,
        text="+",
        width=36,
        height=36,
        corner_radius=10,
        fg_color="#7ed957",
        hover_color="#6bc84a",
        text_color="#1b1b1b",
        font=("Segoe UI", 18, "bold"),
        command=lambda: add_to_cart(
            product_id,
            stock,
            qty_label,
            cart_frame,
            total_label,
            products
        )
    )


    minus_button.pack(
        side="left",
        padx=4
    )

    qty_label.pack(
        side="left",
        padx=6
    )

    plus_button.pack(
        side="left",
        padx=4
    )


# =====================================================
# CREATE ORDER PAGE
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


    # Configure Grid

    for column in range(4):

        order_frame.grid_columnconfigure(
            column,
            weight=1
        )


    # REFRESH PRODUCTS

    def refresh_products():

        # Remove old cards

        for widget in order_frame.winfo_children():

            widget.destroy()


        # Get latest products

        latest_products = db.get_products()


        # Create cards again

        for index, product in enumerate(latest_products):

            row = index // 4

            column = index % 4


            create_product_card(
                order_frame,
                product,
                row,
                column,
                cart_frame,
                total_label,
                latest_products
            )


    # INITIAL PRODUCT CARDS

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


    return order_frame, refresh_products


# =====================================================
# BOOK SERVICES PAGE
# =====================================================

def create_book_page(parent):

    book_frame = ctk.CTkScrollableFrame(
        parent,
        fg_color="#ffe7d6"
    )


    # TITLE

    ctk.CTkLabel(
        book_frame,
        text="🐾 Book Pet Services",
        font=("Segoe UI", 32, "bold"),
        text_color="#2b1d14"
    ).pack(
        pady=(30, 10)
    )


    ctk.CTkLabel(
        book_frame,
        text="Choose a service for your furry friend",
        font=("Segoe UI", 16),
        text_color="#666666"
    ).pack(
        pady=(0, 25)
    )


    services = [

        {
            "title": "Pet Grooming",
            "emoji": "✂️",
            "description": "Full grooming service including bath, haircut, nail trimming and ear cleaning.",
            "price": "₹499 onwards"
        },

        {
            "title": "Vet Consultation",
            "emoji": "🩺",
            "description": "Professional veterinary check-up and health consultation for your pet.",
            "price": "₹299"
        },

        {
            "title": "Pet Boarding",
            "emoji": "🏠",
            "description": "Safe and comfortable temporary stay for your pet while you're away.",
            "price": "₹799 / night"
        },

        {
            "title": "Nail Trimming",
            "emoji": "💅",
            "description": "Quick and gentle nail trimming service by trained staff.",
            "price": "₹149"
        },

        {
            "title": "Pet Training",
            "emoji": "🎓",
            "description": "Basic obedience and behavior training sessions for dogs.",
            "price": "₹999 / session"
        },

        {
            "title": "Dental Care",
            "emoji": "🦷",
            "description": "Teeth cleaning and oral health check for cats and dogs.",
            "price": "₹599"
        }

    ]


    for service in services:


        # SERVICE CARD

        card = ctk.CTkFrame(
            book_frame,
            fg_color="white",
            corner_radius=18,
            border_width=1,
            border_color="#f0d9c8"
        )

        card.pack(
            fill="x",
            padx=40,
            pady=10
        )


        left = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        left.pack(
            side="left",
            fill="both",
            expand=True,
            padx=20,
            pady=18
        )


        title_frame = ctk.CTkFrame(
            left,
            fg_color="transparent"
        )

        title_frame.pack(
            anchor="w"
        )


        ctk.CTkLabel(
            title_frame,
            text=service["emoji"],
            font=("Segoe UI Emoji", 28)
        ).pack(
            side="left",
            padx=(0, 12)
        )


        ctk.CTkLabel(
            title_frame,
            text=service["title"],
            font=("Segoe UI", 20, "bold"),
            text_color="#2b1d14"
        ).pack(
            side="left"
        )


        ctk.CTkLabel(
            left,
            text=service["description"],
            font=("Segoe UI", 14),
            text_color="#555555",
            wraplength=520,
            justify="left"
        ).pack(
            anchor="w",
            pady=(8, 6)
        )


        ctk.CTkLabel(
            left,
            text=service["price"],
            font=("Segoe UI", 15, "bold"),
            text_color="#e67e22"
        ).pack(
            anchor="w"
        )


        # BOOKING POPUP

        def open_booking_popup(
                service_name=service["title"]):


            if current_user_id is None:

                messagebox.showerror(
                    "Error",
                    "Please login first."
                )

                return


            popup = ctk.CTkToplevel()

            popup.title(
                f"Book {service_name}"
            )

            popup.geometry(
                "420x500"
            )

            popup.grab_set()

            popup.resizable(
                False,
                False
            )


            ctk.CTkLabel(
                popup,
                text=f"Book: {service_name}",
                font=("Segoe UI", 22, "bold"),
                text_color="#2b1d14"
            ).pack(
                pady=(25, 20)
            )


            # PET NAME

            ctk.CTkLabel(
                popup,
                text="Pet Name",
                anchor="w"
            ).pack(
                fill="x",
                padx=40
            )


            pet_entry = ctk.CTkEntry(
                popup,
                height=38,
                placeholder_text="e.g. Bruno, Milo..."
            )

            pet_entry.pack(
                fill="x",
                padx=40,
                pady=(5, 15)
            )


            # DATE

            ctk.CTkLabel(
                popup,
                text="Preferred Date (YYYY-MM-DD)",
                anchor="w"
            ).pack(
                fill="x",
                padx=40
            )


            date_entry = ctk.CTkEntry(
                popup,
                height=38,
                placeholder_text="2026-09-10"
            )

            date_entry.pack(
                fill="x",
                padx=40,
                pady=(5, 15)
            )


            # NOTES

            ctk.CTkLabel(
                popup,
                text="Additional Notes (optional)",
                anchor="w"
            ).pack(
                fill="x",
                padx=40
            )


            notes_entry = ctk.CTkTextbox(
                popup,
                height=90
            )

            notes_entry.pack(
                fill="x",
                padx=40,
                pady=(5, 25)
            )


            def confirm_booking():

                pet_name = pet_entry.get().strip()

                booking_date = date_entry.get().strip()

                notes = notes_entry.get(
                    "1.0",
                    "end"
                ).strip()


                if not pet_name or not booking_date:

                    messagebox.showwarning(
                        "Missing Info",
                        "Please enter Pet Name and Date."
                    )

                    return


                success = db.create_booking(
                    current_user_id,
                    service_name,
                    pet_name,
                    booking_date,
                    notes
                )


                if success:

                    messagebox.showinfo(
                        "Booking Successful",
                        f"Your booking for {service_name} has been placed!\n\nWe will contact you soon."
                    )

                    popup.destroy()


                else:

                    messagebox.showerror(
                        "Error",
                        "Could not save booking. Please try again."
                    )


            ctk.CTkButton(
                popup,
                text="Confirm Booking",
                height=45,
                fg_color="#FA9A85",
                hover_color="#f08b75",
                font=("Segoe UI", 15, "bold"),
                command=confirm_booking
            ).pack(
                fill="x",
                padx=40,
                pady=5
            )


            ctk.CTkButton(
                popup,
                text="Cancel",
                height=38,
                fg_color="#e0e0e0",
                hover_color="#d0d0d0",
                text_color="#333",
                command=popup.destroy
            ).pack(
                fill="x",
                padx=40,
                pady=(5, 20)
            )


        ctk.CTkButton(
            card,
            text="Book Now",
            width=130,
            height=42,
            corner_radius=12,
            fg_color="#FA9A85",
            hover_color="#f08b75",
            text_color="white",
            font=("Segoe UI", 14, "bold"),
            command=open_booking_popup
        ).pack(
            side="right",
            padx=25,
            pady=25
        )


    return book_frame


# =====================================================
# ABOUT POPUP
# =====================================================

def show_about_popup():

    popup = ctk.CTkToplevel()

    popup.geometry(
        "400x300"
    )

    popup.title(
        "About"
    )

    popup.grab_set()


    ctk.CTkLabel(
        popup,
        text="🐾 Pet Goods & Services",
        font=("Arial", 20, "bold")
    ).pack(
        pady=25
    )


    ctk.CTkLabel(
        popup,
        text=(
            "Version 1.0\n\n"
            "Your one-stop shop for pet needs.\n\n"
            "Browse products, manage your cart,\n"
            "and explore pet services!"
        ),
        justify="center"
    ).pack(
        pady=10
    )


    ctk.CTkButton(
        popup,
        text="Close",
        command=popup.destroy
    ).pack(
        pady=20
    )


# =====================================================
# CONTACT POPUP
# =====================================================

def show_contact_popup():

    popup = ctk.CTkToplevel()

    popup.geometry(
        "400x300"
    )

    popup.title(
        "Contact Support"
    )

    popup.grab_set()


    ctk.CTkLabel(
        popup,
        text="Contact Support",
        font=("Arial", 20, "bold")
    ).pack(
        pady=25
    )


    ctk.CTkLabel(
        popup,
        text=(
            "Email: support@petshop.com\n\n"
            "Phone: +91 XXXXX XXXXX\n\n"
            "Support available during business hours."
        ),
        justify="center"
    ).pack(
        pady=20
    )


    ctk.CTkButton(
        popup,
        text="Close",
        command=popup.destroy
    ).pack(
        pady=15
    )


# =====================================================
# FAQ POPUP
# =====================================================

def show_faq_popup():

    popup = ctk.CTkToplevel()

    popup.geometry(
        "500x450"
    )

    popup.title(
        "FAQ"
    )

    popup.grab_set()


    ctk.CTkLabel(
        popup,
        text="Frequently Asked Questions",
        font=("Arial", 20, "bold")
    ).pack(
        pady=20
    )


    faq_text = """

Q: How do I add products?
A: Use the + button on a product.

Q: How do I remove products?
A: Use the - button.

Q: Will my cart be saved?
A: Yes! Your cart is saved to your account.

Q: How do I checkout?
A: Add products and press Checkout.

Q: Can other users see my cart?
A: No. Every user has their own cart.
"""


    ctk.CTkLabel(
        popup,
        text=faq_text,
        justify="left",
        font=("Arial", 13)
    ).pack(
        padx=30,
        pady=10
    )


    ctk.CTkButton(
        popup,
        text="Close",
        command=popup.destroy
    ).pack(
        pady=15
    )


# =====================================================
# SETTINGS PAGE
# =====================================================

def create_settings_page(parent, show_frame):

    global current_user_id


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
        font=("Segoe UI", 32, "bold"),
        text_color="#2b1d14"
    ).pack(
        pady=(25, 15)
    )


    user_data = db.get_user(
        current_user_id
    )


    # ACCOUNT INFORMATION

    account_frame = ctk.CTkFrame(
        settings_content,
        fg_color="white",
        corner_radius=15
    )

    account_frame.pack(
        fill="x",
        padx=30,
        pady=10
    )


    ctk.CTkLabel(
        account_frame,
        text="Account Information",
        font=("Segoe UI", 18, "bold"),
        text_color="#2b1d14"
    ).pack(
        anchor="w",
        padx=20,
        pady=(15, 10)
    )


    if user_data:

        username = user_data[1]
        email = user_data[2]
        phone = user_data[3]
        address = user_data[4]


        ctk.CTkLabel(
            account_frame,
            text=f"Username: {username}",
            text_color="#333"
        ).pack(
            anchor="w",
            padx=20,
            pady=2
        )


        ctk.CTkLabel(
            account_frame,
            text=f"Email: {email}",
            text_color="#333"
        ).pack(
            anchor="w",
            padx=20,
            pady=2
        )


        ctk.CTkLabel(
            account_frame,
            text=f"Phone: {phone}",
            text_color="#333"
        ).pack(
            anchor="w",
            padx=20,
            pady=2
        )


        ctk.CTkLabel(
            account_frame,
            text=f"Address: {address}",
            text_color="#333",
            wraplength=700
        ).pack(
            anchor="w",
            padx=20,
            pady=(2, 15)
        )


    # MY BOOKINGS

    bookings_frame = ctk.CTkFrame(
        settings_content,
        fg_color="white",
        corner_radius=15
    )

    bookings_frame.pack(
        fill="x",
        padx=30,
        pady=10
    )


    ctk.CTkLabel(
        bookings_frame,
        text="My Bookings",
        font=("Segoe UI", 18, "bold"),
        text_color="#2b1d14"
    ).pack(
        anchor="w",
        padx=20,
        pady=(15, 10)
    )


    bookings = db.get_user_bookings(
        current_user_id
    )


    if not bookings:

        ctk.CTkLabel(
            bookings_frame,
            text="You have no bookings yet.",
            text_color="#888888",
            font=("Segoe UI", 14)
        ).pack(
            pady=25
        )


    else:

        for booking in bookings:

            b_id, service, pet, date, notes, status, created = booking


            card = ctk.CTkFrame(
                bookings_frame,
                fg_color="#FFF8F3",
                corner_radius=12
            )

            card.pack(
                fill="x",
                padx=15,
                pady=6
            )


            top = ctk.CTkFrame(
                card,
                fg_color="transparent"
            )

            top.pack(
                fill="x",
                padx=15,
                pady=(12, 4)
            )


            ctk.CTkLabel(
                top,
                text=service,
                font=("Segoe UI", 15, "bold"),
                text_color="#2b1d14"
            ).pack(
                side="left"
            )


            status_color = (
                "#43a047"
                if status.lower() == "confirmed"
                else "#e67e22"
            )


            ctk.CTkLabel(
                top,
                text=status,
                font=("Segoe UI", 13, "bold"),
                text_color=status_color
            ).pack(
                side="right"
            )


            ctk.CTkLabel(
                card,
                text=f"Pet: {pet}   •   Date: {date}",
                font=("Segoe UI", 13),
                text_color="#555555"
            ).pack(
                anchor="w",
                padx=15
            )


            if notes and notes.strip():

                ctk.CTkLabel(
                    card,
                    text=f"Notes: {notes}",
                    font=("Segoe UI", 12),
                    text_color="#777777",
                    wraplength=650
                ).pack(
                    anchor="w",
                    padx=15,
                    pady=(4, 12)
                )


    # HELP AND SUPPORT

    help_frame = ctk.CTkFrame(
        settings_content,
        fg_color="white",
        corner_radius=15
    )

    help_frame.pack(
        fill="x",
        padx=30,
        pady=10
    )


    ctk.CTkLabel(
        help_frame,
        text="Help & Support",
        font=("Segoe UI", 18, "bold"),
        text_color="#2b1d14"
    ).pack(
        anchor="w",
        padx=20,
        pady=(15, 10)
    )


    ctk.CTkButton(
        help_frame,
        text="About App",
        fg_color="#FA9A85",
        command=show_about_popup
    ).pack(
        fill="x",
        padx=20,
        pady=5
    )


    ctk.CTkButton(
        help_frame,
        text="Contact Support",
        fg_color="#FA9A85",
        command=show_contact_popup
    ).pack(
        fill="x",
        padx=20,
        pady=5
    )


    ctk.CTkButton(
        help_frame,
        text="FAQ",
        fg_color="#FA9A85",
        command=show_faq_popup
    ).pack(
        fill="x",
        padx=20,
        pady=(5, 15)
    )


    # LOGOUT

    danger_frame = ctk.CTkFrame(
        settings_content,
        fg_color="white",
        corner_radius=15
    )

    danger_frame.pack(
        fill="x",
        padx=30,
        pady=10
    )


    ctk.CTkLabel(
        danger_frame,
        text="Account",
        font=("Segoe UI", 18, "bold"),
        text_color="#2b1d14"
    ).pack(
        anchor="w",
        padx=20,
        pady=(15, 10)
    )


    def logout():

        global current_user_id


        confirm = messagebox.askyesno(
            "Logout",
            "Are you sure you want to logout?"
        )


        if not confirm:
            return


        if os.path.exists("session.txt"):

            os.remove(
                "session.txt"
            )


        cart.clear()

        current_user_id = None

        show_frame(
            "login"
        )


    ctk.CTkButton(
        danger_frame,
        text="Logout",
        fg_color="tomato",
        hover_color="#e57373",
        text_color="white",
        height=42,
        font=("Segoe UI", 14, "bold"),
        command=logout
    ).pack(
        fill="x",
        padx=20,
        pady=(0, 15)
    )


# =====================================================
# MY ORDERS / ORDER HISTORY
# =====================================================

def create_order_history_page(parent):
    """Create the signed-in user's order history with reusable invoices."""
    history_frame = ctk.CTkScrollableFrame(parent, fg_color="#ffe7d6")

    header = ctk.CTkFrame(history_frame, fg_color="transparent")
    header.pack(fill="x", padx=22, pady=(20, 8))
    ctk.CTkLabel(
        header,
        text="📦 My Orders",
        font=("Segoe UI", 26, "bold"),
        text_color="#2b1d14"
    ).pack(side="left")

    body = ctk.CTkFrame(history_frame, fg_color="transparent")
    body.pack(fill="both", expand=True, padx=12, pady=(0, 18))

    def refresh_orders():
        for widget in body.winfo_children():
            widget.destroy()

        if current_user_id is None:
            ctk.CTkLabel(
                body, text="Please log in to view your orders.",
                font=("Segoe UI", 15), text_color="#6d5b52"
            ).pack(pady=28)
            return

        try:
            orders = db.get_user_orders(current_user_id)
        except Exception as exc:
            print("Could not load order history:", exc)
            ctk.CTkLabel(
                body,
                text="Couldn't load your orders. Please try again.",
                font=("Segoe UI", 15), text_color="#9b2c2c"
            ).pack(pady=28)
            return

        if not orders:
            ctk.CTkLabel(
                body,
                text="You haven't placed any orders yet. Your purchases will appear here.",
                font=("Segoe UI", 15), text_color="#6d5b52",
                wraplength=650
            ).pack(pady=36)
            return

        for order_id, total, order_date, status, item_count in orders:
            card = ctk.CTkFrame(body, fg_color="#fffaf6", corner_radius=12)
            card.pack(fill="x", padx=8, pady=7)

            date_text = (
                order_date.strftime("%d %b %Y, %I:%M %p")
                if hasattr(order_date, "strftime") else str(order_date)
            )
            status_text = str(status or "Placed")
            top = ctk.CTkFrame(card, fg_color="transparent")
            top.pack(fill="x", padx=16, pady=(13, 4))
            ctk.CTkLabel(
                top, text=f"Order #CN-{order_id}",
                font=("Segoe UI", 16, "bold"), text_color="#2b1d14"
            ).pack(side="left")
            ctk.CTkLabel(
                top, text=status_text,
                font=("Segoe UI", 13, "bold"), text_color="#b95340"
            ).pack(side="right")

            ctk.CTkLabel(
                card,
                text=f"Placed: {date_text}   •   {item_count} item(s)   •   Total: ₹{float(total):,.2f}",
                font=("Segoe UI", 13), text_color="#6d5b52"
            ).pack(anchor="w", padx=16, pady=(0, 10))

            actions = ctk.CTkFrame(card, fg_color="transparent")
            actions.pack(fill="x", padx=16, pady=(0, 13))

            ctk.CTkButton(
                actions,
                text="Track Order  →",
                width=130,
                fg_color="#f7d9c5",
                hover_color="#efc4aa",
                text_color="#30251f",
                command=lambda oid=order_id: open_order_tracking(oid)
            ).pack(side="left")
            ctk.CTkButton(
                actions,
                text="View Invoice",
                width=130,
                fg_color="#fa9a85",
                hover_color="#e98270",
                text_color="#30251f",
                command=lambda oid=order_id: open_invoice(oid)
            ).pack(side="right")

    def open_order_tracking(order_id):
        """Show a clear status timeline for one of the signed-in user's orders."""
        try:
            # Re-read the signed-in user's orders so the tracker uses the latest saved status.
            latest = next(
                (row for row in db.get_user_orders(current_user_id) if int(row[0]) == int(order_id)),
                None
            )
        except Exception as exc:
            messagebox.showerror("Tracking unavailable", f"Couldn't load tracking details.\n\n{exc}")
            return

        if latest is None:
            messagebox.showerror("Order unavailable", "This order could not be found in your account.")
            return

        _, total, latest_date, latest_status, _ = latest
        status_text = str(latest_status or "Placed")
        normalized_status = status_text.strip().lower()
        tracking = ctk.CTkToplevel(history_frame)
        tracking.title(f"Track Order — CN-{order_id}")
        tracking.geometry("560x500")
        tracking.minsize(500, 450)
        tracking.configure(fg_color="#ffe7d6")
        tracking.transient(history_frame.winfo_toplevel())
        tracking.grab_set()

        ctk.CTkLabel(
            tracking, text=f"📦 Track Order #CN-{order_id}",
            font=("Segoe UI", 23, "bold"), text_color="#2b1d14"
        ).pack(anchor="w", padx=24, pady=(22, 4))
        date_text = (
            latest_date.strftime("%d %b %Y, %I:%M %p")
            if hasattr(latest_date, "strftime") else str(latest_date)
        )
        ctk.CTkLabel(
            tracking, text=f"Placed {date_text}   •   Total ₹{float(total):,.2f}",
            font=("Segoe UI", 12), text_color="#6d5b52"
        ).pack(anchor="w", padx=26, pady=(0, 18))

        current = ctk.CTkFrame(tracking, fg_color="#fffaf6", corner_radius=14)
        current.pack(fill="x", padx=22, pady=(0, 16))
        status_color = "#b95340" if normalized_status == "cancelled" else "#7b563e"
        ctk.CTkLabel(
            current, text="CURRENT STATUS", font=("Segoe UI", 10, "bold"),
            text_color="#8a776c"
        ).pack(anchor="w", padx=16, pady=(13, 2))
        ctk.CTkLabel(
            current, text=status_text, font=("Segoe UI", 20, "bold"),
            text_color=status_color
        ).pack(anchor="w", padx=16, pady=(0, 13))

        stages = ["Placed", "Processing", "Shipped", "Delivered"]
        if normalized_status == "cancelled":
            cancel_box = ctk.CTkFrame(tracking, fg_color="#fff0ed", corner_radius=12)
            cancel_box.pack(fill="x", padx=22, pady=4)
            ctk.CTkLabel(
                cancel_box, text="✕  This order has been cancelled.",
                font=("Segoe UI", 14, "bold"), text_color="#a83232"
            ).pack(anchor="w", padx=16, pady=(13, 4))
            ctk.CTkLabel(
                cancel_box,
                text="If you have questions about this order, please contact the store.",
                font=("Segoe UI", 12), text_color="#6d5b52", wraplength=440, justify="left"
            ).pack(anchor="w", padx=16, pady=(0, 13))
        else:
            stage_index = next((i for i, stage in enumerate(stages) if stage.lower() == normalized_status), 0)
            timeline = ctk.CTkFrame(tracking, fg_color="transparent")
            timeline.pack(fill="x", padx=28, pady=(0, 12))
            for index, stage in enumerate(stages):
                done = index <= stage_index
                row = ctk.CTkFrame(timeline, fg_color="transparent")
                row.pack(fill="x", pady=4)
                dot_color = "#b85e47" if done else "#d8c6ba"
                ctk.CTkLabel(
                    row, text="●" if done else "○", width=28,
                    font=("Segoe UI", 19, "bold"), text_color=dot_color
                ).pack(side="left")
                ctk.CTkLabel(
                    row, text=stage, font=("Segoe UI", 14, "bold" if index == stage_index else "normal"),
                    text_color="#2b1d14" if done else "#9b8a80"
                ).pack(side="left", padx=(8, 0))
                if index == stage_index:
                    ctk.CTkLabel(
                        row, text="CURRENT", font=("Segoe UI", 9, "bold"),
                        text_color="#b85e47"
                    ).pack(side="right", padx=8)

        ctk.CTkLabel(
            tracking,
            text="Order updates are provided by the Cat Nip team. Use Refresh in My Orders to check for changes.",
            font=("Segoe UI", 11), text_color="#766b65", wraplength=490, justify="left"
        ).pack(anchor="w", padx=25, pady=(4, 12))
        ctk.CTkButton(
            tracking, text="Done", width=110, fg_color="#fa9a85",
            hover_color="#e98270", text_color="#30251f",
            command=tracking.destroy
        ).pack(anchor="e", padx=22, pady=(0, 18))

    def open_invoice(order_id):
        try:
            generate_order_bill(order_id, current_user_id)
        except Exception as exc:
            messagebox.showerror("Invoice unavailable", f"Couldn't open this invoice.\n\n{exc}")

    ctk.CTkButton(
        header,
        text="Refresh",
        width=100,
        fg_color="#fa9a85",
        hover_color="#e98270",
        text_color="#30251f",
        command=refresh_orders
    ).pack(side="right")

    refresh_orders()
    return history_frame, refresh_orders


# =====================================================
# PAGE SWITCHING
# =====================================================

def show_user_page(target, pages, refresh_orders=None):
    for frame in pages.values():
        frame.pack_forget()
    if target == "history" and refresh_orders:
        refresh_orders()
    pages[target].pack(fill="both", expand=True)


def show_order(order_frame, book_frame, settings_frame, history_frame=None, extra_frames=None):
    pages = {"order": order_frame, "book": book_frame, "settings": settings_frame}
    if history_frame is not None: pages["history"] = history_frame
    if extra_frames: pages.update(extra_frames)
    show_user_page("order", pages)


def show_book(order_frame, book_frame, settings_frame, history_frame=None, extra_frames=None):
    pages = {"order": order_frame, "book": book_frame, "settings": settings_frame}
    if history_frame is not None: pages["history"] = history_frame
    if extra_frames: pages.update(extra_frames)
    show_user_page("book", pages)


def show_settings(order_frame, book_frame, settings_frame, show_frame, history_frame=None, extra_frames=None):
    pages = {"order": order_frame, "book": book_frame, "settings": settings_frame}
    if history_frame is not None: pages["history"] = history_frame
    if extra_frames: pages.update(extra_frames)
    for widget in settings_frame.winfo_children(): widget.destroy()
    create_settings_page(settings_frame, show_frame)
    show_user_page("settings", pages)


def show_order_history(order_frame, book_frame, settings_frame, history_frame, refresh_orders, extra_frames=None):
    pages = {"order": order_frame, "book": book_frame, "settings": settings_frame, "history": history_frame}
    if extra_frames: pages.update(extra_frames)
    show_user_page("history", pages, refresh_orders)


def create_navbar(parent, order_frame, book_frame, settings_frame, show_frame,
                  history_frame=None, refresh_orders=None, adoption_frame=None,
                  playdates_frame=None, chatbot_frame=None):
    navbar = ctk.CTkFrame(parent, height=70, fg_color="#FA9A85", corner_radius=0)
    navbar.pack(fill="x")
    ctk.CTkLabel(navbar, text="🐾 Pet Supplies", font=("Arial", 26, "bold"), text_color="white").pack(side="left", padx=18, pady=15)
    button_frame = ctk.CTkFrame(navbar, fg_color="transparent")
    button_frame.pack(side="right", padx=12)

    pages = {"order": order_frame, "book": book_frame, "settings": settings_frame}
    if history_frame is not None: pages["history"] = history_frame
    if adoption_frame is not None: pages["adoption"] = adoption_frame
    if playdates_frame is not None: pages["playdates"] = playdates_frame
    if chatbot_frame is not None: pages["chatbot"] = chatbot_frame

    def navigate(target):
        # Settings is intentionally created only when first opened. The frame
        # is otherwise empty, so populate it before switching to that page.
        if target == "settings":
            if not getattr(settings_frame, "_settings_page_built", False):
                create_settings_page(settings_frame, show_frame)
                settings_frame._settings_page_built = True

        show_user_page(
            target,
            pages,
            refresh_orders if target == "history" else None
        )

    def nav_button(label, target):
        ctk.CTkButton(
            button_frame,
            text=label,
            fg_color="white",
            text_color="#FA9A85",
            hover_color="#f9d8d1",
            font=("Arial", 14, "bold"),
            height=34,
            command=lambda key=target: navigate(key)
        ).pack(side="left", padx=3)

    nav_button("Order", "order")
    nav_button("Book", "book")
    if adoption_frame is not None: nav_button("🐾 Adopt", "adoption")
    if playdates_frame is not None: nav_button("🐕 Playdates", "playdates")
    if chatbot_frame is not None: nav_button("💬 Chatbot", "chatbot")
    nav_button("Settings", "settings")
    if history_frame is not None: nav_button("My Orders", "history")


# =====================================================
# BILL / INVOICE GENERATION
# =====================================================

def generate_order_bill(order_id, user_id):
    """Display the saved order invoice inside the Cat Nip application.

    Also saves an HTML copy so the user can open a printable version and
    save it as PDF if desired.
    """
    invoice_data = db.get_order_invoice_data(order_id, user_id)
    if not invoice_data:
        raise ValueError("The order details could not be found for this account.")

    order = invoice_data["order"]
    items = invoice_data["items"]
    (saved_order_id, total, order_date, status, username, email, phone, address) = order

    def esc(value):
        return html.escape("" if value is None else str(value))

    date_text = order_date.strftime("%d %b %Y, %I:%M %p") if hasattr(order_date, "strftime") else str(order_date)

    html_rows = []
    for _product_id, name, quantity, price in items:
        subtotal = float(price) * int(quantity)
        html_rows.append(
            "<tr>"
            f"<td>{esc(name)}</td>"
            f"<td class='number'>{int(quantity)}</td>"
            f"<td class='number'>₹{float(price):,.2f}</td>"
            f"<td class='number'>₹{subtotal:,.2f}</td>"
            "</tr>"
        )
    if not html_rows:
        html_rows.append("<tr><td colspan='4'>No item details available.</td></tr>")

    # Keep a printable copy available, but show the invoice in the app by default.
    bill_html = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><title>Cat Nip Invoice #{saved_order_id}</title>
<style>body{{font-family:Arial,sans-serif;color:#30251f;background:#fff8f3;padding:32px}}.invoice{{max-width:800px;margin:auto;background:white;padding:36px}}table{{width:100%;border-collapse:collapse;margin-top:24px}}th,td{{padding:10px;border-bottom:1px solid #eee;text-align:left}}th{{background:#fa9a85}}.number{{text-align:right}}.total{{text-align:right;font-size:22px;font-weight:bold;margin-top:24px}}@media print{{.no-print{{display:none}}}}</style></head>
<body><main class="invoice"><h1>🐾 Cat Nip</h1><p>Pet Goods &amp; Services — Customer Invoice</p>
<p><strong>Invoice #CN-{saved_order_id}</strong><br>Date: {esc(date_text)}<br>Order status: {esc(status or 'Placed')}</p>
<p><strong>Bill to:</strong><br>{esc(username)}<br>{esc(address)}<br>{esc(phone)}<br>{esc(email)}</p>
<table><thead><tr><th>Product</th><th>Qty</th><th>Unit price</th><th>Subtotal</th></tr></thead><tbody>{''.join(html_rows)}</tbody></table>
<p class="total">Total: ₹{float(total):,.2f}</p><p>Thank you for shopping with Cat Nip!</p>
<button class="no-print" onclick="window.print()">Print / Save as PDF</button></main></body></html>"""
    bills_dir = Path(__file__).resolve().parent.parent / "bills"
    bills_dir.mkdir(parents=True, exist_ok=True)
    bill_path = bills_dir / f"invoice_{saved_order_id}.html"
    bill_path.write_text(bill_html, encoding="utf-8")

    # In-app invoice window.
    bill_window = ctk.CTkToplevel()
    bill_window.title(f"Cat Nip - Invoice #CN-{saved_order_id}")
    bill_window.geometry("820x680")
    bill_window.minsize(650, 520)
    bill_window.transient()
    bill_window.grab_set()

    page = ctk.CTkScrollableFrame(bill_window, fg_color="#fffaf6", corner_radius=0)
    page.pack(fill="both", expand=True, padx=12, pady=(12, 6))

    header = ctk.CTkFrame(page, fg_color="#fffaf6")
    header.pack(fill="x", padx=18, pady=(18, 10))
    ctk.CTkLabel(header, text="🐾 Cat Nip", font=("Arial", 28, "bold"), text_color="#d96e59").pack(anchor="w")
    ctk.CTkLabel(header, text="PET GOODS & SERVICES  •  CUSTOMER INVOICE", font=("Arial", 12, "bold"), text_color="#766b65").pack(anchor="w", pady=(2, 12))
    ctk.CTkFrame(header, height=2, fg_color="#fa9a85").pack(fill="x", pady=(0, 12))

    order_info = ctk.CTkFrame(page, fg_color="white", corner_radius=10)
    order_info.pack(fill="x", padx=18, pady=6)
    ctk.CTkLabel(order_info, text=f"Invoice #CN-{saved_order_id}", font=("Arial", 18, "bold"), text_color="#30251f").pack(anchor="w", padx=16, pady=(12, 2))
    ctk.CTkLabel(order_info, text=f"Date: {date_text}    |    Status: {status or 'Placed'}", font=("Arial", 12), text_color="#766b65").pack(anchor="w", padx=16, pady=(0, 12))

    customer = ctk.CTkFrame(page, fg_color="white", corner_radius=10)
    customer.pack(fill="x", padx=18, pady=6)
    ctk.CTkLabel(customer, text="BILL TO", font=("Arial", 11, "bold"), text_color="#d96e59").pack(anchor="w", padx=16, pady=(12, 2))
    customer_text = "\n".join(str(v) for v in (username, address, phone, email) if v)
    ctk.CTkLabel(customer, text=customer_text or "Customer details unavailable", justify="left", anchor="w", font=("Arial", 12), text_color="#30251f").pack(anchor="w", padx=16, pady=(0, 12))

    table = ctk.CTkFrame(page, fg_color="white", corner_radius=10)
    table.pack(fill="x", padx=18, pady=6)
    table.grid_columnconfigure(0, weight=5)
    table.grid_columnconfigure(1, weight=1)
    table.grid_columnconfigure(2, weight=2)
    table.grid_columnconfigure(3, weight=2)
    headings = [("Product", 0), ("Qty", 1), ("Unit price", 2), ("Subtotal", 3)]
    for title, col in headings:
        ctk.CTkLabel(table, text=title, font=("Arial", 11, "bold"), text_color="#30251f", fg_color="#fa9a85", corner_radius=4).grid(row=0, column=col, sticky="ew", padx=3, pady=(8, 5), ipady=7)

    for row_index, (_product_id, name, quantity, price) in enumerate(items, start=1):
        qty = int(quantity)
        unit_price = float(price)
        values = (str(name), str(qty), f"₹{unit_price:,.2f}", f"₹{unit_price * qty:,.2f}")
        for col, value in enumerate(values):
            ctk.CTkLabel(table, text=value, anchor="w" if col == 0 else "e", font=("Arial", 12), text_color="#30251f").grid(row=row_index, column=col, sticky="ew", padx=10, pady=8)
        ctk.CTkFrame(table, height=1, fg_color="#f0e4dc").grid(row=row_index + 1, column=0, columnspan=4, sticky="ew", padx=8)

    ctk.CTkLabel(page, text=f"TOTAL:  ₹{float(total):,.2f}", font=("Arial", 24, "bold"), text_color="#b95340").pack(anchor="e", padx=28, pady=(16, 6))
    ctk.CTkLabel(page, text="Thank you for shopping with Cat Nip! Keep this invoice for your records.", font=("Arial", 12), text_color="#766b65", wraplength=700).pack(anchor="w", padx=22, pady=(0, 18))

    actions = ctk.CTkFrame(bill_window, fg_color="transparent")
    actions.pack(fill="x", padx=18, pady=(4, 14))
    ctk.CTkButton(actions, text="Open Printable Version", fg_color="#fa9a85", hover_color="#e98270", text_color="#30251f", command=lambda: webbrowser.open(bill_path.resolve().as_uri())).pack(side="left", padx=(0, 8))
    ctk.CTkButton(actions, text="Close", command=bill_window.destroy).pack(side="right")
    return bill_path


# =====================================================
# CART SIDEBAR
# =====================================================

def create_cart_sidebar(
        parent,
        refresh_callback):


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


    # CART ITEMS

    cart_items_frame = ctk.CTkScrollableFrame(
        sidebar,
        width=240
    )


    cart_items_frame.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )


    # TOTAL

    total_label = ctk.CTkLabel(
        sidebar,
        text="Total: ₹0.00",
        font=("Arial", 20, "bold"),
        text_color="black"
    )


    total_label.pack(
        pady=10
    )


    # =================================================
    # CHECKOUT
    # =================================================

    def checkout():

        global current_user_id


        # LOGIN CHECK

        if current_user_id is None:

            messagebox.showerror(
                "Error",
                "No user is logged in."
            )

            return


        # EMPTY CART CHECK

        if not cart or sum(cart.values()) == 0:

            messagebox.showwarning(
                "Cart Empty",
                "Please add products to your cart first."
            )

            return


        # CONFIRM

        confirm = messagebox.askyesno(
            "Confirm Checkout",
            "Are you sure you want to place this order?"
        )


        if not confirm:
            return


        # CHECKOUT

        order_id = db.checkout(
            current_user_id
        )


        if order_id:


            # CLEAR LOCAL CART

            cart.clear()


            # GET LATEST PRODUCTS

            products = db.get_products()


            # REFRESH CART

            refresh_cart(
                cart_items_frame,
                total_label,
                products
            )


            # REFRESH PRODUCT CARDS

            if refresh_callback[0]:

                refresh_callback[0]()


            # SUCCESS MESSAGE

            # Generate the invoice after checkout succeeds. A bill-generation
            # problem must not turn a successful order into a failed checkout.
            try:
                generate_order_bill(order_id, current_user_id)
                bill_message = (
                    f"Your order has been placed successfully!\n\n"
                    f"Order ID: {order_id}\n"
                    "Your invoice is displayed inside Cat Nip. "
                    "Use Open Printable Version to print or save it as PDF."
                )
            except Exception as exc:
                print("Bill generation error:", exc)
                bill_message = (
                    f"Your order has been placed successfully!\n\n"
                    f"Order ID: {order_id}\n"
                    "However, the invoice could not be generated. "
                    "Please contact the project administrator."
                )

            messagebox.showinfo(
                "Order Successful",
                bill_message
            )


        else:

            messagebox.showerror(
                "Checkout Failed",
                "Something went wrong while placing your order."
            )


    # CHECKOUT BUTTON

    ctk.CTkButton(
        sidebar,
        text="Checkout",
        height=45,
        fg_color="#7ed957",
        text_color="black",
        font=("Arial", 16, "bold"),
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

def user_screen(
        container,
        show_frame):


    global current_user_id


    # =================================================
    # GET CURRENT USER
    # =================================================

    current_user_id = db.get_current_user_id()


    # =================================================
    # MAIN PAGE
    # =================================================

    page = ctk.CTkFrame(
        container,
        fg_color="#ffe7d6"
    )


    # =================================================
    # NAVBAR PLACEHOLDER
    # =================================================

    # The navbar will be created after pages are ready


    # =================================================
    # MAIN CONTENT AREA
    # =================================================

    content_area = ctk.CTkFrame(
        page,
        fg_color="#ffe7d6"
    )


    content_area.pack(
        fill="both",
        expand=True
    )


    # =================================================
    # REFRESH CALLBACK
    # =================================================

    # This stores the refresh_products function.
    # It is created later by create_order_page.

    refresh_callback = [None]


    # =================================================
    # CART SIDEBAR
    # =================================================

    cart_frame, total_label = create_cart_sidebar(
        content_area,
        refresh_callback
    )


    # =================================================
    # LEFT CONTENT AREA
    # =================================================

    page_container = ctk.CTkFrame(
        content_area,
        fg_color="#ffe7d6"
    )


    page_container.pack(
        side="left",
        fill="both",
        expand=True
    )


    # =================================================
    # GET PRODUCTS
    # =================================================

    products = db.get_products()


    # =================================================
    # LOAD USER CART
    # =================================================

    if current_user_id is not None:

        load_user_cart(
            current_user_id
        )


    # =================================================
    # CREATE ORDER PAGE
    # =================================================

    order_frame, refresh_products = create_order_page(
        page_container,
        products,
        cart_frame,
        total_label
    )


    # =================================================
    # CONNECT REFRESH FUNCTION
    # =================================================

    refresh_callback[0] = refresh_products


    # =================================================
    # CREATE BOOK PAGE
    # =================================================

    book_frame = create_book_page(
        page_container
    )


    # =================================================
    # SETTINGS FRAME
    # =================================================

    settings_frame = ctk.CTkFrame(
        page_container,
        fg_color="#ffe7d6"
    )

    history_frame, refresh_orders = create_order_history_page(page_container)

    # These features are embedded into the main user-page content area, just
    # like Order, Book, Settings, and My Orders (not separate pop-up windows).
    adoption_frame = ctk.CTkFrame(page_container, fg_color="#FFF6EF", corner_radius=0)
    open_adoption_window(adoption_frame, current_user_id, embedded=True)
    playdates_frame = ctk.CTkFrame(page_container, fg_color="#FFF6EF", corner_radius=0)
    open_playdates_user(playdates_frame, current_user_id, embedded=True)
    chatbot_frame = create_chatbot_page(page_container)

    # =====================================================
    # NAVBAR

    # =================================================
    # NAVBAR
    # =================================================

    create_navbar(
        page,
        order_frame,
        book_frame,
        settings_frame,
        show_frame,
        history_frame,
        refresh_orders,
        adoption_frame,
        playdates_frame,
        chatbot_frame
    )


    # =================================================
    # SHOW ORDER PAGE
    # =================================================

    for _page in (book_frame, settings_frame, history_frame, adoption_frame, playdates_frame, chatbot_frame):
        _page.pack_forget()

    order_frame.pack(
        fill="both",
        expand=True
    )


    # =================================================
    # REFRESH CART
    # =================================================

    refresh_cart(
        cart_frame,
        total_label,
        products
    )


    return page