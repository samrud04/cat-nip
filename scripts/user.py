import customtkinter as ctk
from tkinter import messagebox
import os
import db


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

    # Clear previous user's cart
    cart.clear()

    # Get this user's cart
    cart_items = db.get_cart(user_id)

    for item in cart_items:

        product_id = item[0]
        quantity = item[1]

        cart[product_id] = quantity


# =====================================================
# REFRESH CART
# =====================================================

def refresh_cart(cart_frame, total_label, products):

    # Clear old cart display
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


    # Show cart items
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
                    text=f"{name}",
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


    # Empty cart message
    if not cart:

        ctk.CTkLabel(
            cart_frame,
            text="Your cart is empty",
            text_color="gray"
        ).pack(
            pady=30
        )


    # Update total
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


    # Check stock
    if current_quantity >= stock:

        messagebox.showwarning(
            "Stock Limit",
            "Cannot add more than available stock."
        )

        return


    # Add to database
    db.add_to_cart(
        current_user_id,
        product_id
    )


    # Update local cart
    cart[product_id] = current_quantity + 1


    # Update quantity label
    qty_label.configure(
        text=str(cart[product_id])
    )


    # Refresh cart
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


    # Remove from database
    db.remove_from_cart(
        current_user_id,
        product_id
    )


    # Reduce local quantity
    cart[product_id] -= 1


    # Remove completely if zero
    if cart[product_id] <= 0:

        del cart[product_id]

        qty_label.configure(
            text="0"
        )

    else:

        qty_label.configure(
            text=str(cart[product_id])
        )


    # Refresh cart
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

    # ---------- Product Card ----------
    card = ctk.CTkFrame(
        parent,
        width=230,
        height=360,
        fg_color="white",
        corner_radius=20,
        border_width=1,
        border_color="#f0d9c8"
    )
    card.grid(row=row, column=column, padx=12, pady=12, sticky="n")
    card.grid_propagate(False)

    # ---------- Icon Area ----------
    image_frame = ctk.CTkFrame(
        card,
        width=190,
        height=110,
        fg_color="#FFF0E6",          # soft peach
        corner_radius=16
    )
    image_frame.pack(pady=(18, 10))
    image_frame.pack_propagate(False)

    # Smarter icon selection
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

    # ---------- Product Name ----------
    ctk.CTkLabel(
        card,
        text=name,
        font=("Segoe UI", 16, "bold"),
        text_color="#2b1d14",
        wraplength=200
    ).pack(pady=(5, 2))

    # ---------- Brand & Category ----------
    ctk.CTkLabel(
        card,
        text=f"{brand}  •  {category}",
        font=("Segoe UI", 12),
        text_color="#666666"
    ).pack()

    # ---------- Price ----------
    ctk.CTkLabel(
        card,
        text=f"₹{price:.2f}",
        font=("Segoe UI", 18, "bold"),
        text_color="#2e7d32"
    ).pack(pady=6)

    # ---------- Stock Status ----------
    if stock <= 0:
        stock_text = "Out of Stock"
        stock_color = "#e53935"
    elif stock <= 10:
        stock_text = f"Only {stock} left!"
        stock_color = "#fb8c00"
    else:
        stock_text = "In Stock"
        stock_color = "#43a047"

    ctk.CTkLabel(
        card,
        text=stock_text,
        font=("Segoe UI", 13),
        text_color=stock_color
    ).pack()

    # ---------- Quantity Controls ----------
    quantity_frame = ctk.CTkFrame(card, fg_color="transparent")
    quantity_frame.pack(pady=12)

    qty_label = ctk.CTkLabel(
        quantity_frame,
        text=str(cart.get(product_id, 0)),
        width=40,
        font=("Segoe UI", 16, "bold"),
        text_color="#2b1d14"
    )

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
            product_id, qty_label, cart_frame, total_label, products
        )
    )

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
            product_id, stock, qty_label, cart_frame, total_label, products
        )
    )

    minus_button.pack(side="left", padx=4)
    qty_label.pack(side="left", padx=6)
    plus_button.pack(side="left", padx=4)

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


    # Configure columns

    for column in range(4):

        order_frame.grid_columnconfigure(
            column,
            weight=1
        )


    # Create product cards

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
# BOOK SERVICES PAGE
# =====================================================

def create_book_page(parent):

    book_frame = ctk.CTkScrollableFrame(
        parent,
        fg_color="#ffe7d6"
    )

    # Title
    ctk.CTkLabel(
        book_frame,
        text="🐾 Book Pet Services",
        font=("Segoe UI", 32, "bold"),
        text_color="#2b1d14"
    ).pack(pady=(30, 10))

    ctk.CTkLabel(
        book_frame,
        text="Choose a service for your furry friend",
        font=("Segoe UI", 16),
        text_color="#666666"
    ).pack(pady=(0, 25))

    services = [
        {"title": "Pet Grooming", "emoji": "✂️", "description": "Full grooming service including bath, haircut, nail trimming and ear cleaning.", "price": "₹499 onwards"},
        {"title": "Vet Consultation", "emoji": "🩺", "description": "Professional veterinary check-up and health consultation for your pet.", "price": "₹299"},
        {"title": "Pet Boarding", "emoji": "🏠", "description": "Safe and comfortable temporary stay for your pet while you're away.", "price": "₹799 / night"},
        {"title": "Nail Trimming", "emoji": "💅", "description": "Quick and gentle nail trimming service by trained staff.", "price": "₹149"},
        {"title": "Pet Training", "emoji": "🎓", "description": "Basic obedience and behavior training sessions for dogs.", "price": "₹999 / session"},
        {"title": "Dental Care", "emoji": "🦷", "description": "Teeth cleaning and oral health check for cats and dogs.", "price": "₹599"},
    ]

    for service in services:

        card = ctk.CTkFrame(
            book_frame,
            fg_color="white",
            corner_radius=18,
            border_width=1,
            border_color="#f0d9c8"
        )
        card.pack(fill="x", padx=40, pady=10)

        left = ctk.CTkFrame(card, fg_color="transparent")
        left.pack(side="left", fill="both", expand=True, padx=20, pady=18)

        title_frame = ctk.CTkFrame(left, fg_color="transparent")
        title_frame.pack(anchor="w")

        ctk.CTkLabel(
            title_frame,
            text=service["emoji"],
            font=("Segoe UI Emoji", 28)
        ).pack(side="left", padx=(0, 12))

        ctk.CTkLabel(
            title_frame,
            text=service["title"],
            font=("Segoe UI", 20, "bold"),
            text_color="#2b1d14"
        ).pack(side="left")

        ctk.CTkLabel(
            left,
            text=service["description"],
            font=("Segoe UI", 14),
            text_color="#555555",
            wraplength=520,
            justify="left"
        ).pack(anchor="w", pady=(8, 6))

        ctk.CTkLabel(
            left,
            text=service["price"],
            font=("Segoe UI", 15, "bold"),
            text_color="#e67e22"
        ).pack(anchor="w")

        # ========== WORKING BOOK BUTTON WITH POPUP ==========
        def open_booking_popup(service_name=service["title"]):

            if current_user_id is None:
                messagebox.showerror("Error", "Please login first.")
                return

            popup = ctk.CTkToplevel()
            popup.title(f"Book {service_name}")
            popup.geometry("420x500")
            popup.grab_set()
            popup.resizable(False, False)

            ctk.CTkLabel(
                popup,
                text=f"Book: {service_name}",
                font=("Segoe UI", 22, "bold"),
                text_color="#2b1d14"
            ).pack(pady=(25, 20))

            # Pet Name
            ctk.CTkLabel(popup, text="Pet Name", anchor="w").pack(fill="x", padx=40)
            pet_entry = ctk.CTkEntry(popup, height=38, placeholder_text="e.g. Bruno, Milo...")
            pet_entry.pack(fill="x", padx=40, pady=(5, 15))

            # Date
            ctk.CTkLabel(popup, text="Preferred Date (YYYY-MM-DD)", anchor="w").pack(fill="x", padx=40)
            date_entry = ctk.CTkEntry(popup, height=38, placeholder_text="2025-04-20")
            date_entry.pack(fill="x", padx=40, pady=(5, 15))

            # Notes
            ctk.CTkLabel(popup, text="Additional Notes (optional)", anchor="w").pack(fill="x", padx=40)
            notes_entry = ctk.CTkTextbox(popup, height=90)
            notes_entry.pack(fill="x", padx=40, pady=(5, 25))

            def confirm_booking():
                pet_name = pet_entry.get().strip()
                booking_date = date_entry.get().strip()
                notes = notes_entry.get("1.0", "end").strip()

                if not pet_name or not booking_date:
                    messagebox.showwarning("Missing Info", "Please enter Pet Name and Date.")
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
                    messagebox.showerror("Error", "Could not save booking. Please try again.")

            ctk.CTkButton(
                popup,
                text="Confirm Booking",
                height=45,
                fg_color="#FA9A85",
                hover_color="#f08b75",
                font=("Segoe UI", 15, "bold"),
                command=confirm_booking
            ).pack(fill="x", padx=40, pady=5)

            ctk.CTkButton(
                popup,
                text="Cancel",
                height=38,
                fg_color="#e0e0e0",
                hover_color="#d0d0d0",
                text_color="#333",
                command=popup.destroy
            ).pack(fill="x", padx=40, pady=(5, 20))

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
        ).pack(side="right", padx=25, pady=25)

    return book_frame 

# =====================================================
# ABOUT POPUP
# =====================================================

def show_about_popup():

    popup = ctk.CTkToplevel()

    popup.geometry("400x300")

    popup.title("About")

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

    popup.geometry("400x300")

    popup.title("Contact Support")

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

    popup.geometry("500x450")

    popup.title("FAQ")

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
# CREATE SETTINGS PAGE
# =====================================================

def create_settings_page(parent, show_frame):
    global current_user_id
    bookings = db.get_user_bookings(current_user_id)

    print("Current User ID:", current_user_id)
    print("Bookings found:", bookings)

    settings_content = ctk.CTkScrollableFrame(
        parent,
        fg_color="#ffe7d6"
    )
    settings_content.pack(fill="both", expand=True)

    # ========== TITLE ==========
    ctk.CTkLabel(
        settings_content,
        text="Settings",
        font=("Segoe UI", 32, "bold"),
        text_color="#2b1d14"
    ).pack(pady=(25, 15))

    
    user_data = db.get_user(current_user_id)

    # ========== ACCOUNT INFORMATION ==========
    account_frame = ctk.CTkFrame(
        settings_content,
        fg_color="white",
        corner_radius=15
    )
    account_frame.pack(fill="x", padx=30, pady=10)

    ctk.CTkLabel(
        account_frame,
        text="Account Information",
        font=("Segoe UI", 18, "bold"),
        text_color="#2b1d14"
    ).pack(anchor="w", padx=20, pady=(15, 10))

    if user_data:
        username = user_data[1]
        email = user_data[2]
        phone = user_data[3]
        address = user_data[4]

        ctk.CTkLabel(account_frame, text=f"Username: {username}", text_color="#333").pack(anchor="w", padx=20, pady=2)
        ctk.CTkLabel(account_frame, text=f"Email: {email}", text_color="#333").pack(anchor="w", padx=20, pady=2)
        ctk.CTkLabel(account_frame, text=f"Phone: {phone}", text_color="#333").pack(anchor="w", padx=20, pady=2)
        ctk.CTkLabel(account_frame, text=f"Address: {address}", text_color="#333", wraplength=700).pack(anchor="w", padx=20, pady=(2, 15))

    # ========== MY BOOKINGS ==========
    bookings_frame = ctk.CTkFrame(
        settings_content,
        fg_color="white",
        corner_radius=15
    )
    bookings_frame.pack(fill="x", padx=30, pady=10)

    ctk.CTkLabel(
        bookings_frame,
        text="My Bookings",
        font=("Segoe UI", 18, "bold"),
        text_color="#2b1d14"
    ).pack(anchor="w", padx=20, pady=(15, 10))

    bookings = db.get_user_bookings(current_user_id)

    if not bookings:
        ctk.CTkLabel(
            bookings_frame,
            text="You have no bookings yet.",
            text_color="#888888",
            font=("Segoe UI", 14)
        ).pack(pady=25)
    else:
        for booking in bookings:
            b_id, service, pet, date, notes, status, created = booking

            card = ctk.CTkFrame(
                bookings_frame,
                fg_color="#FFF8F3",
                corner_radius=12
            )
            card.pack(fill="x", padx=15, pady=6)

            # Top row: Service name + Status
            top = ctk.CTkFrame(card, fg_color="transparent")
            top.pack(fill="x", padx=15, pady=(12, 4))

            ctk.CTkLabel(
                top,
                text=service,
                font=("Segoe UI", 15, "bold"),
                text_color="#2b1d14"
            ).pack(side="left")

            status_color = "#43a047" if status.lower() == "confirmed" else "#e67e22"
            ctk.CTkLabel(
                top,
                text=status,
                font=("Segoe UI", 13, "bold"),
                text_color=status_color
            ).pack(side="right")

            # Details
            ctk.CTkLabel(
                card,
                text=f"Pet: {pet}   •   Date: {date}",
                font=("Segoe UI", 13),
                text_color="#555555"
            ).pack(anchor="w", padx=15)

            if notes and notes.strip():
                ctk.CTkLabel(
                    card,
                    text=f"Notes: {notes}",
                    font=("Segoe UI", 12),
                    text_color="#777777",
                    wraplength=650
                ).pack(anchor="w", padx=15, pady=(4, 12))
            else:
                ctk.CTkLabel(card, text="").pack(pady=6)

    # ========== HELP & SUPPORT ==========
    help_frame = ctk.CTkFrame(
        settings_content,
        fg_color="white",
        corner_radius=15
    )
    help_frame.pack(fill="x", padx=30, pady=10)

    ctk.CTkLabel(
        help_frame,
        text="Help & Support",
        font=("Segoe UI", 18, "bold"),
        text_color="#2b1d14"
    ).pack(anchor="w", padx=20, pady=(15, 10))

    ctk.CTkButton(help_frame, text="About App", fg_color="#FA9A85", command=show_about_popup).pack(fill="x", padx=20, pady=5)
    ctk.CTkButton(help_frame, text="Contact Support", fg_color="#FA9A85", command=show_contact_popup).pack(fill="x", padx=20, pady=5)
    ctk.CTkButton(help_frame, text="FAQ", fg_color="#FA9A85", command=show_faq_popup).pack(fill="x", padx=20, pady=(5, 15))

    # ========== LOGOUT ==========
    danger_frame = ctk.CTkFrame(
        settings_content,
        fg_color="white",
        corner_radius=15
    )
    danger_frame.pack(fill="x", padx=30, pady=10)

    ctk.CTkLabel(
        danger_frame,
        text="Account",
        font=("Segoe UI", 18, "bold"),
        text_color="#2b1d14"
    ).pack(anchor="w", padx=20, pady=(15, 10))

    def logout():
        global current_user_id
        confirm = messagebox.askyesno("Logout", "Are you sure you want to logout?")
        if not confirm:
            return

        if os.path.exists("session.txt"):
            os.remove("session.txt")

        cart.clear()
        current_user_id = None
        show_frame("login")

    ctk.CTkButton(
        danger_frame,
        text="Logout",
        fg_color="tomato",
        hover_color="#e57373",
        text_color="white",
        height=42,
        font=("Segoe UI", 14, "bold"),
        command=logout
    ).pack(fill="x", padx=20, pady=(0, 15))


# =====================================================
# INTERNAL PAGE SWITCHING
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


    # Clear previous settings

    for widget in settings_frame.winfo_children():

        widget.destroy()


    # Recreate settings
    # This refreshes user information

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

    navbar.pack(
        fill="x"
    )


    # Logo

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


    # Button frame

    button_frame = ctk.CTkFrame(
        navbar,
        fg_color="transparent"
    )

    button_frame.pack(
        side="right",
        padx=20
    )


    # ORDER

    ctk.CTkButton(
        button_frame,
        text="Order",
        fg_color="white",
        text_color="#FA9A85",
        hover_color="#f9d8d1",
        font=("Arial", 16, "bold"),
        command=lambda: show_order(
            order_frame,
            book_frame,
            settings_frame
        )
    ).pack(
        side="left",
        padx=5
    )


    # BOOK

    ctk.CTkButton(
        button_frame,
        text="Book",
        fg_color="white",
        text_color="#FA9A85",
        hover_color="#f9d8d1",
        font=("Arial", 16, "bold"),
        command=lambda: show_book(
            order_frame,
            book_frame,
            settings_frame
        )
    ).pack(
        side="left",
        padx=5
    )


    # SETTINGS

    ctk.CTkButton(
        button_frame,
        text="Settings",
        fg_color="white",
        text_color="#FA9A85",
        hover_color="#f9d8d1",
        font=("Arial", 16, "bold"),
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


    # Cart items area

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


    # Total

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

        # Check if a user is logged in
        if current_user_id is None:

            messagebox.showerror(
                "Error",
                "No user is logged in."
            )

            return


        # Check if cart is empty
        if not cart or sum(cart.values()) == 0:

            messagebox.showwarning(
                "Cart Empty",
                "Please add products to your cart first."
            )

            return


        # Confirm checkout
        confirm = messagebox.askyesno(
            "Confirm Checkout",
            "Are you sure you want to place this order?"
        )

        if not confirm:
            return


        # Save order to database
        success = db.checkout(
                current_user_id
        )


        if success:

            # Clear local cart
            cart.clear()


            # Get latest products
            products = db.get_products()


            # Refresh cart display
            refresh_cart(
                cart_items_frame,
                total_label,
                products
            )


            messagebox.showinfo(
                "Order Successful",
                "Your order has been placed successfully!"
            )


        else:

            messagebox.showerror(
                "Checkout Failed",
                "Something went wrong while placing your order."
            )
    # Checkout button

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

def user_screen(container, show_frame):

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
    # CART SIDEBAR
    # =================================================

    cart_frame, total_label = create_cart_sidebar(
        content_area
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
    # PRODUCTS
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

    order_frame = create_order_page(
        page_container,
        products,
        cart_frame,
        total_label
    )


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


    # =================================================
    # NAVBAR
    # =================================================

    create_navbar(
        page,
        order_frame,
        book_frame,
        settings_frame,
        show_frame
    )


    # =================================================
    # SHOW ORDER PAGE FIRST
    # =================================================

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