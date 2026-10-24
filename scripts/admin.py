import customtkinter as ctk
from tkinter import ttk, messagebox
import os

from adoption import open_adoption_admin

from db import (
    get_products,
    add_product,
    delete_product,
    update_stock,
    update_product,
    get_all_orders,
    get_admin_order_details,
    update_order_status,
    get_all_bookings,
    get_admin_booking_details,
    update_booking_status,
)


def create_admin_frame(container, show_frame):

    # =====================================================
    # ADMIN FRAME
    # =====================================================

    admin_frame = ctk.CTkFrame(
        container,
        fg_color="#EAF4FF"
    )

    admin_frame.grid_rowconfigure(1, weight=1)
    admin_frame.grid_columnconfigure(1, weight=1)


    # =====================================================
    # LOGOUT
    # =====================================================

    def logout():

        # Remove session if it exists
        if os.path.exists("session.txt"):
            os.remove("session.txt")

        show_frame("login")


    # =====================================================
    # LOAD PRODUCTS
    # =====================================================

    def load_products():

        for row in tree.get_children():
            tree.delete(row)

        products = get_products()

        total_products = len(products)
        low_stock = 0
        inventory_value = 0

        for product in products:

            row_id = tree.insert(
                "",
                "end",
                values=product
            )

            price = float(product[2])
            stock = int(product[5])

            inventory_value += price * stock

            if stock < 5:

                low_stock += 1

                tree.item(
                    row_id,
                    tags=("low_stock",)
                )


        tree.tag_configure(
            "low_stock",
            background="#FFF0F0"
        )


        total_products_label.configure(
            text=f"Products: {total_products}"
        )


        low_stock_label.configure(
            text=f"Low Stock: {low_stock}"
        )


        inventory_value_label.configure(
            text=f"Inventory Value: ₹{inventory_value:,.2f}"
        )


    # =====================================================
    # ADD PRODUCT
    # =====================================================

    def add_product_gui():

        product_name = name_entry.get().strip()
        price = price_entry.get().strip()
        brand = brand_entry.get().strip()
        category = category_entry.get()
        stock = stock_entry.get().strip()


        if not product_name:

            messagebox.showerror(
                "Error",
                "Please enter a product name."
            )

            return


        if not price:

            messagebox.showerror(
                "Error",
                "Please enter a price."
            )

            return


        if not brand:

            messagebox.showerror(
                "Error",
                "Please enter a brand."
            )

            return


        if category == "Select Category":

            messagebox.showerror(
                "Error",
                "Please select a category."
            )

            return


        if not stock:

            messagebox.showerror(
                "Error",
                "Please enter the stock quantity."
            )

            return


        try:

            price = float(price)
            stock = int(stock)

        except ValueError:

            messagebox.showerror(
                "Invalid Input",
                "Price must be a number and stock must be a whole number."
            )

            return


        if price <= 0:

            messagebox.showerror(
                "Invalid Price",
                "Price must be greater than 0."
            )

            return


        if stock < 0:

            messagebox.showerror(
                "Invalid Stock",
                "Stock cannot be negative."
            )

            return


        add_product(
            (
                product_name,
                price,
                brand,
                category,
                stock
            )
        )


        load_products()


        name_entry.delete(0, "end")
        price_entry.delete(0, "end")
        brand_entry.delete(0, "end")

        category_entry.set(
            "Select Category"
        )

        stock_entry.delete(0, "end")


        messagebox.showinfo(
            "Success",
            f"{product_name} was added successfully!"
        )


    # =====================================================
    # DELETE PRODUCT
    # =====================================================

    def delete_selected():

        selected = tree.selection()


        if not selected:

            messagebox.showerror(
                "Error",
                "Please select a product to delete."
            )

            return


        values = tree.item(
            selected[0]
        )["values"]


        product_id = values[0]
        product_name = values[1]


        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete '{product_name}'?"
        )


        if not confirm:
            return


        delete_product(product_id)

        load_products()


        messagebox.showinfo(
            "Success",
            f"'{product_name}' was deleted successfully."
        )


    # =====================================================
    # EDIT PRODUCT
    # =====================================================

    def edit_selected():

        selected = tree.selection()


        if not selected:

            messagebox.showerror(
                "Error",
                "Please select a product to edit."
            )

            return


        values = tree.item(
            selected[0]
        )["values"]


        product_id = values[0]


        name_entry.delete(0, "end")
        name_entry.insert(0, values[1])


        price_entry.delete(0, "end")
        price_entry.insert(0, values[2])


        brand_entry.delete(0, "end")
        brand_entry.insert(0, values[3])


        category_entry.set(
            values[4]
        )


        stock_entry.delete(0, "end")
        stock_entry.insert(0, values[5])


        edit_button.configure(
            text="💾 Save Changes",
            command=lambda: save_edit(product_id)
        )


    # =====================================================
    # SAVE EDIT
    # =====================================================

    def save_edit(product_id):

        product_name = name_entry.get().strip()
        price = price_entry.get().strip()
        brand = brand_entry.get().strip()
        category = category_entry.get()
        stock = stock_entry.get().strip()


        if not product_name or not price or not brand or not stock:

            messagebox.showerror(
                "Error",
                "Please fill all fields."
            )

            return


        if category == "Select Category":

            messagebox.showerror(
                "Error",
                "Please select a category."
            )

            return


        try:

            price = float(price)
            stock = int(stock)

        except ValueError:

            messagebox.showerror(
                "Invalid Input",
                "Price and stock must be valid numbers."
            )

            return


        if price <= 0 or stock < 0:

            messagebox.showerror(
                "Error",
                "Enter valid price and stock."
            )

            return


        update_product(
            product_id,
            product_name,
            price,
            brand,
            category,
            stock
        )


        load_products()


        name_entry.delete(0, "end")
        price_entry.delete(0, "end")
        brand_entry.delete(0, "end")

        category_entry.set(
            "Select Category"
        )

        stock_entry.delete(0, "end")


        edit_button.configure(
            text="✏️ Edit Selected",
            command=edit_selected
        )


        messagebox.showinfo(
            "Success",
            f"{product_name} was updated successfully!"
        )


    # =====================================================
    # INCREASE STOCK
    # =====================================================

    def increase_stock():

        selected = tree.selection()


        if not selected:
            return


        values = tree.item(
            selected[0]
        )["values"]


        update_stock(
            values[0],
            int(values[5]) + 1
        )


        load_products()


    # =====================================================
    # DECREASE STOCK
    # =====================================================

    def decrease_stock():

        selected = tree.selection()


        if not selected:

            messagebox.showerror(
                "Error",
                "Please select a product."
            )

            return


        values = tree.item(
            selected[0]
        )["values"]


        product_id = values[0]
        product_name = values[1]

        current_stock = int(
            values[5]
        )


        if current_stock == 0:

            messagebox.showwarning(
                "Out of Stock",
                f"{product_name} is already out of stock."
            )

            return


        new_stock = current_stock - 1


        update_stock(
            product_id,
            new_stock
        )


        load_products()


        if new_stock == 0:

            messagebox.showwarning(
                "Out of Stock",
                f"{product_name} is now out of stock."
            )


        elif new_stock < 5:

            messagebox.showwarning(
                "Low Stock",
                f"{product_name} has only {new_stock} item(s) left."
            )


    # =====================================================
    # SEARCH PRODUCTS
    # =====================================================

    def search_products():

        search_text = search_entry.get().lower().strip()


        for row in tree.get_children():
            tree.delete(row)


        for product in get_products():

            product_text = " ".join(
                str(value) for value in product
            ).lower()


            if search_text in product_text:

                tree.insert(
                    "",
                    "end",
                    values=product
                )


    # =====================================================
    # ORDER MANAGEMENT
    # =====================================================

    def open_order_management():
        order_window = ctk.CTkToplevel(admin_frame)
        order_window.title("Cat Nip — Order Management")
        order_window.geometry("1100x700")
        order_window.minsize(850, 550)
        order_window.configure(fg_color="#EAF4FF")
        order_window.grab_set()

        ctk.CTkLabel(
            order_window,
            text="📦 Order Management",
            font=("Segoe UI", 26, "bold")
        ).pack(anchor="w", padx=20, pady=(18, 4))

        ctk.CTkLabel(
            order_window,
            text="Review purchases, view order contents, and update delivery status.",
            font=("Segoe UI", 13)
        ).pack(anchor="w", padx=22, pady=(0, 12))

        content = ctk.CTkFrame(order_window, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        content.grid_columnconfigure(0, weight=3)
        content.grid_columnconfigure(1, weight=2)
        content.grid_rowconfigure(0, weight=1)

        orders_panel = ctk.CTkFrame(content)
        orders_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        orders_panel.grid_columnconfigure(0, weight=1)
        orders_panel.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            orders_panel, text="All Orders", font=("Segoe UI", 18, "bold")
        ).grid(row=0, column=0, sticky="w", padx=12, pady=10)

        order_columns = ("Order ID", "Customer", "Date", "Total", "Status", "Items")
        orders_tree = ttk.Treeview(
            orders_panel, columns=order_columns, show="headings", height=18
        )
        for col in order_columns:
            orders_tree.heading(col, text=col)
            orders_tree.column(col, anchor="center", width=100)
        orders_tree.column("Customer", width=120)
        orders_tree.column("Date", width=145)
        orders_tree.grid(row=1, column=0, sticky="nsew", padx=(10, 0), pady=(0, 10))

        orders_scroll = ttk.Scrollbar(orders_panel, orient="vertical", command=orders_tree.yview)
        orders_tree.configure(yscrollcommand=orders_scroll.set)
        orders_scroll.grid(row=1, column=1, sticky="ns", pady=(0, 10))

        right_panel = ctk.CTkFrame(content)
        right_panel.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
        right_panel.grid_columnconfigure(0, weight=1)
        right_panel.grid_rowconfigure(2, weight=1)

        ctk.CTkLabel(
            right_panel, text="Order Details", font=("Segoe UI", 18, "bold")
        ).grid(row=0, column=0, sticky="w", padx=12, pady=(10, 5))

        customer_label = ctk.CTkLabel(
            right_panel, text="Select an order to view its details.",
            justify="left", anchor="w", wraplength=350
        )
        customer_label.grid(row=1, column=0, sticky="ew", padx=12, pady=5)

        item_columns = ("Product", "Qty", "Unit Price")
        items_tree = ttk.Treeview(right_panel, columns=item_columns, show="headings", height=10)
        for col in item_columns:
            items_tree.heading(col, text=col)
            items_tree.column(col, anchor="center", width=95)
        items_tree.column("Product", width=160, anchor="w")
        items_tree.grid(row=2, column=0, sticky="nsew", padx=10, pady=8)

        status_frame = ctk.CTkFrame(right_panel, fg_color="transparent")
        status_frame.grid(row=3, column=0, sticky="ew", padx=12, pady=(4, 12))
        status_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(status_frame, text="Update status:").grid(
            row=0, column=0, sticky="w", pady=(0, 5)
        )
        status_picker = ctk.CTkComboBox(
            status_frame,
            values=["Placed", "Processing", "Shipped", "Delivered", "Cancelled"],
            state="readonly"
        )
        status_picker.set("Placed")
        status_picker.grid(row=1, column=0, sticky="ew", pady=(0, 8))

        selected_order = {"id": None}

        def refresh_order_list(select_id=None):
            for row in orders_tree.get_children():
                orders_tree.delete(row)
            try:
                orders = get_all_orders()
                for order in orders:
                    order_id, username, order_date, total, status, item_count = order
                    date_text = order_date.strftime("%d %b %Y, %H:%M") if hasattr(order_date, "strftime") else str(order_date)
                    orders_tree.insert(
                        "", "end", iid=str(order_id),
                        values=(order_id, username or f"User #{order_id}", date_text,
                                f"₹{float(total):,.2f}", status or "Placed", item_count)
                    )
                if select_id is not None and orders_tree.exists(str(select_id)):
                    orders_tree.selection_set(str(select_id))
                    orders_tree.focus(str(select_id))
                    show_selected_order()
            except Exception as exc:
                messagebox.showerror("Orders Error", f"Could not load orders.\n\n{exc}", parent=order_window)

        def show_selected_order(_event=None):
            selection = orders_tree.selection()
            if not selection:
                return
            try:
                order_id = int(selection[0])
                data = get_admin_order_details(order_id)
                if not data:
                    customer_label.configure(text="Order not found.")
                    return
                order = data["order"]
                selected_order["id"] = order_id
                _, user_id, username, email, phone, address, total, order_date, status = order
                date_text = order_date.strftime("%d %b %Y, %H:%M") if hasattr(order_date, "strftime") else str(order_date)
                customer_label.configure(
                    text=(f"Order #{order_id}\nCustomer: {username or f'User #{user_id}'}\n"
                          f"Email: {email or '—'}\nPhone: {phone or '—'}\n"
                          f"Address: {address or '—'}\nDate: {date_text}\n"
                          f"Total: ₹{float(total):,.2f}\nCurrent status: {status or 'Placed'}")
                )
                for row in items_tree.get_children():
                    items_tree.delete(row)
                for product_id, product_name, quantity, price in data["items"]:
                    items_tree.insert(
                        "", "end",
                        values=(product_name, quantity, f"₹{float(price):,.2f}")
                    )
                status_picker.set(status or "Placed")
            except Exception as exc:
                messagebox.showerror("Order Details Error", f"Could not load order details.\n\n{exc}", parent=order_window)

        def save_status():
            order_id = selected_order["id"]
            if order_id is None:
                messagebox.showwarning("Select Order", "Select an order first.", parent=order_window)
                return
            new_status = status_picker.get()
            if not messagebox.askyesno(
                "Confirm Status Change",
                f"Set order #{order_id} to '{new_status}'?",
                parent=order_window
            ):
                return
            try:
                update_order_status(order_id, new_status)
                refresh_order_list(select_id=order_id)
                messagebox.showinfo("Updated", f"Order #{order_id} is now {new_status}.", parent=order_window)
            except Exception as exc:
                messagebox.showerror("Update Failed", f"Could not update status.\n\n{exc}", parent=order_window)

        orders_tree.bind("<<TreeviewSelect>>", show_selected_order)

        ctk.CTkButton(
            status_frame, text="💾 Update Order Status", command=save_status
        ).grid(row=2, column=0, sticky="ew", pady=(0, 7))
        ctk.CTkButton(
            status_frame, text="🔄 Refresh Orders",
            command=lambda: refresh_order_list(selected_order["id"])
        ).grid(row=3, column=0, sticky="ew")

        refresh_order_list()


    # =====================================================
    # BOOKING MANAGEMENT
    # =====================================================

    def open_booking_management():
        booking_window = ctk.CTkToplevel(admin_frame)
        booking_window.title("Cat Nip — Booking Management")
        booking_window.geometry("1120x710")
        booking_window.minsize(880, 570)
        booking_window.configure(fg_color="#EAF4FF")
        booking_window.grab_set()

        ctk.CTkLabel(
            booking_window,
            text="📅 Booking Management",
            font=("Segoe UI", 26, "bold")
        ).pack(anchor="w", padx=20, pady=(18, 4))
        ctk.CTkLabel(
            booking_window,
            text="Review service appointments, customer details, and update booking status.",
            font=("Segoe UI", 13)
        ).pack(anchor="w", padx=22, pady=(0, 12))

        content = ctk.CTkFrame(booking_window, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        content.grid_columnconfigure(0, weight=3)
        content.grid_columnconfigure(1, weight=2)
        content.grid_rowconfigure(0, weight=1)

        left = ctk.CTkFrame(content)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        left.grid_columnconfigure(0, weight=1)
        left.grid_rowconfigure(1, weight=1)
        ctk.CTkLabel(left, text="All Bookings", font=("Segoe UI", 18, "bold")).grid(
            row=0, column=0, sticky="w", padx=12, pady=10
        )

        columns = ("Booking ID", "Customer", "Service", "Pet", "Date", "Status")
        bookings_tree = ttk.Treeview(left, columns=columns, show="headings", height=18)
        for col in columns:
            bookings_tree.heading(col, text=col)
            bookings_tree.column(col, anchor="center", width=95)
        bookings_tree.column("Booking ID", width=85)
        bookings_tree.column("Customer", width=110)
        bookings_tree.column("Service", width=120)
        bookings_tree.column("Pet", width=90)
        bookings_tree.column("Date", width=100)
        bookings_tree.grid(row=1, column=0, sticky="nsew", padx=(10, 0), pady=(0, 10))
        scrollbar = ttk.Scrollbar(left, orient="vertical", command=bookings_tree.yview)
        bookings_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=1, column=1, sticky="ns", pady=(0, 10))

        right = ctk.CTkFrame(content)
        right.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
        right.grid_columnconfigure(0, weight=1)
        right.grid_rowconfigure(1, weight=1)
        ctk.CTkLabel(right, text="Booking Details", font=("Segoe UI", 18, "bold")).grid(
            row=0, column=0, sticky="w", padx=12, pady=(10, 5)
        )
        details = ctk.CTkTextbox(right, height=270, wrap="word")
        details.grid(row=1, column=0, sticky="nsew", padx=10, pady=8)
        details.insert("1.0", "Select a booking to view its details.")
        details.configure(state="disabled")

        status_frame = ctk.CTkFrame(right, fg_color="transparent")
        status_frame.grid(row=2, column=0, sticky="ew", padx=12, pady=(4, 12))
        status_frame.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(status_frame, text="Update status:").grid(
            row=0, column=0, sticky="w", pady=(0, 5)
        )
        status_picker = ctk.CTkComboBox(
            status_frame,
            values=["Pending", "Confirmed", "In Progress", "Completed", "Cancelled"],
            state="readonly"
        )
        status_picker.set("Pending")
        status_picker.grid(row=1, column=0, sticky="ew", pady=(0, 8))
        selected = {"id": None}

        def set_details(text):
            details.configure(state="normal")
            details.delete("1.0", "end")
            details.insert("1.0", text)
            details.configure(state="disabled")

        def show_selected_booking(_event=None):
            selection = bookings_tree.selection()
            if not selection:
                return
            try:
                booking_id = int(selection[0])
                row = get_admin_booking_details(booking_id)
                if not row:
                    set_details("Booking not found.")
                    return
                (bid, user_id, username, email, phone, service, pet, booking_date,
                 notes, status, created_at) = row
                selected["id"] = bid
                date_text = booking_date.strftime("%d %b %Y") if hasattr(booking_date, "strftime") else str(booking_date or "Not specified")
                created_text = created_at.strftime("%d %b %Y, %H:%M") if hasattr(created_at, "strftime") else str(created_at or "—")
                set_details(
                    f"Booking #{bid}\n"
                    f"Customer: {username or f'User #{user_id}'}\n"
                    f"Email: {email or '—'}\n"
                    f"Phone: {phone or '—'}\n\n"
                    f"Service: {service or '—'}\n"
                    f"Pet name: {pet or '—'}\n"
                    f"Appointment date: {date_text}\n"
                    f"Current status: {status or 'Pending'}\n"
                    f"Created: {created_text}\n\n"
                    f"Customer notes:\n{notes or 'No additional notes.'}"
                )
                status_picker.set(status or "Pending")
            except Exception as exc:
                messagebox.showerror(
                    "Booking Details Error", f"Could not load booking details.\n\n{exc}",
                    parent=booking_window
                )

        def refresh_booking_list(select_id=None):
            for item in bookings_tree.get_children():
                bookings_tree.delete(item)
            try:
                for booking in get_all_bookings():
                    bid, username, service, pet, booking_date, status, created_at = booking
                    date_text = booking_date.strftime("%d %b %Y") if hasattr(booking_date, "strftime") else str(booking_date or "—")
                    bookings_tree.insert(
                        "", "end", iid=str(bid),
                        values=(bid, username or "Unknown", service or "—", pet or "—", date_text, status or "Pending")
                    )
                if select_id is not None and bookings_tree.exists(str(select_id)):
                    bookings_tree.selection_set(str(select_id))
                    bookings_tree.focus(str(select_id))
                    show_selected_booking()
                elif select_id is None:
                    selected["id"] = None
                    set_details("Select a booking to view its details.")
            except Exception as exc:
                messagebox.showerror(
                    "Bookings Error", f"Could not load bookings.\n\n{exc}",
                    parent=booking_window
                )

        def save_booking_status():
            booking_id = selected["id"]
            if booking_id is None:
                messagebox.showwarning("Select Booking", "Select a booking first.", parent=booking_window)
                return
            new_status = status_picker.get()
            if not messagebox.askyesno(
                "Confirm Status Change",
                f"Set booking #{booking_id} to '{new_status}'?",
                parent=booking_window
            ):
                return
            try:
                update_booking_status(booking_id, new_status)
                refresh_booking_list(select_id=booking_id)
                messagebox.showinfo(
                    "Updated", f"Booking #{booking_id} is now {new_status}.", parent=booking_window
                )
            except Exception as exc:
                messagebox.showerror(
                    "Update Failed", f"Could not update booking status.\n\n{exc}",
                    parent=booking_window
                )

        bookings_tree.bind("<<TreeviewSelect>>", show_selected_booking)
        ctk.CTkButton(status_frame, text="💾 Update Booking Status", command=save_booking_status).grid(
            row=2, column=0, sticky="ew", pady=(0, 7)
        )
        ctk.CTkButton(
            status_frame, text="🔄 Refresh Bookings",
            command=lambda: refresh_booking_list(selected["id"])
        ).grid(row=3, column=0, sticky="ew")
        refresh_booking_list()


    # =====================================================
    # HEADER
    # =====================================================

    header = ctk.CTkFrame(
        admin_frame,
        fg_color="#D9ECFF",
        corner_radius=15
    )

    header.grid(
        row=0,
        column=0,
        columnspan=2,
        sticky="ew",
        padx=15,
        pady=15
    )


    header_top = ctk.CTkFrame(
        header,
        fg_color="transparent"
    )

    header_top.pack(
        fill="x",
        padx=20,
        pady=15
    )


    ctk.CTkLabel(
        header_top,
        text="🐾 Pet Store Admin",
        font=("Segoe UI", 28, "bold")
    ).pack(
        side="left"
    )


    ctk.CTkButton(
        header_top,
        text="Logout",
        command=logout,
        width=100,
        fg_color="#D9534F",
        hover_color="#C9302C"
    ).pack(
        side="right"
    )

    ctk.CTkButton(
        header_top,
        text="📦 Manage Orders",
        command=open_order_management,
        width=155,
        fg_color="#2878B5",
        hover_color="#1F6396"
    ).pack(
        side="right",
        padx=(0, 10)
    )

    ctk.CTkButton(
        header_top,
        text="📅 Manage Bookings",
        command=open_booking_management,
        width=170,
        fg_color="#39845A",
        hover_color="#2D6D49"
    ).pack(
        side="right",
        padx=(0, 10)
    )

    ctk.CTkButton(
        header_top,
        text="🐾 Adoption Applications",
        command=lambda: open_adoption_admin(admin_frame),
        width=190,
        fg_color="#B96D57",
        hover_color="#9E5947"
    ).pack(
        side="right",
        padx=(0, 10)
    )


    # =====================================================
    # STATISTICS
    # =====================================================

    stats_frame = ctk.CTkFrame(
        header,
        fg_color="transparent"
    )

    stats_frame.pack(
        fill="x",
        padx=20,
        pady=(0, 15)
    )


    total_products_label = ctk.CTkLabel(
        stats_frame,
        text="Products: 0",
        font=("Segoe UI", 16, "bold")
    )

    total_products_label.pack(
        side="left",
        expand=True
    )


    low_stock_label = ctk.CTkLabel(
        stats_frame,
        text="Low Stock: 0",
        font=("Segoe UI", 16, "bold")
    )

    low_stock_label.pack(
        side="left",
        expand=True
    )


    inventory_value_label = ctk.CTkLabel(
        stats_frame,
        text="Inventory Value: ₹0",
        font=("Segoe UI", 16, "bold")
    )

    inventory_value_label.pack(
        side="left",
        expand=True
    )


    # =====================================================
    # SIDEBAR
    # =====================================================

    sidebar = ctk.CTkFrame(
        admin_frame,
        fg_color="#DFF1FF",
        width=300
    )

    sidebar.grid(
        row=1,
        column=0,
        sticky="ns",
        padx=(15, 8),
        pady=(0, 15)
    )


    name_entry = ctk.CTkEntry(
        sidebar,
        placeholder_text="Product Name"
    )

    name_entry.pack(
        padx=20,
        pady=10,
        fill="x"
    )


    price_entry = ctk.CTkEntry(
        sidebar,
        placeholder_text="Price"
    )

    price_entry.pack(
        padx=20,
        pady=10,
        fill="x"
    )


    brand_entry = ctk.CTkEntry(
        sidebar,
        placeholder_text="Brand"
    )

    brand_entry.pack(
        padx=20,
        pady=10,
        fill="x"
    )


    category_entry = ctk.CTkComboBox(
        sidebar,
        values=["Food", "Accessory"]
    )

    category_entry.set(
        "Select Category"
    )

    category_entry.pack(
        padx=20,
        pady=10,
        fill="x"
    )


    stock_entry = ctk.CTkEntry(
        sidebar,
        placeholder_text="Stock"
    )

    stock_entry.pack(
        padx=20,
        pady=10,
        fill="x"
    )


    ctk.CTkButton(
        sidebar,
        text="➕ Add Product",
        command=add_product_gui
    ).pack(
        padx=20,
        pady=10,
        fill="x"
    )


    ctk.CTkButton(
        sidebar,
        text="🗑 Remove Selected",
        command=delete_selected,
        fg_color="#D9534F"
    ).pack(
        padx=20,
        pady=10,
        fill="x"
    )


    edit_button = ctk.CTkButton(
        sidebar,
        text="✏️ Edit Selected",
        command=edit_selected
    )

    edit_button.pack(
        padx=20,
        pady=10,
        fill="x"
    )


    ctk.CTkButton(
        sidebar,
        text="+ Stock",
        command=increase_stock
    ).pack(
        padx=20,
        pady=10,
        fill="x"
    )


    ctk.CTkButton(
        sidebar,
        text="- Stock",
        command=decrease_stock
    ).pack(
        padx=20,
        pady=10,
        fill="x"
    )


    # =====================================================
    # TABLE FRAME
    # =====================================================

    table_frame = ctk.CTkFrame(
        admin_frame
    )

    table_frame.grid(
        row=1,
        column=1,
        sticky="nsew",
        padx=(8, 15),
        pady=(0, 15)
    )


    # =====================================================
    # SEARCH
    # =====================================================

    search_frame = ctk.CTkFrame(
        table_frame,
        fg_color="transparent"
    )

    search_frame.grid(
        row=0,
        column=0,
        columnspan=2,
        sticky="ew",
        padx=10,
        pady=(10, 5)
    )

    search_frame.grid_columnconfigure(
        0,
        weight=1
    )


    search_entry = ctk.CTkEntry(
        search_frame,
        placeholder_text="🔎 Search products..."
    )

    search_entry.grid(
        row=0,
        column=0,
        sticky="ew",
        padx=(0, 5)
    )


    ctk.CTkButton(
        search_frame,
        text="Search",
        width=100,
        command=search_products
    ).grid(
        row=0,
        column=1,
        padx=5
    )


    ctk.CTkButton(
        search_frame,
        text="Clear",
        width=80,
        command=load_products
    ).grid(
        row=0,
        column=2,
        padx=(5, 0)
    )

    ctk.CTkButton(
        search_frame,
        text="🔄 Refresh",
        width=100,
        command=load_products
    ).grid(
        row=0,
        column=3,
        padx=(5, 0)
    )


    # =====================================================
    # PRODUCT TABLE
    # =====================================================

    table_frame.grid_rowconfigure(
        1,
        weight=1
    )

    table_frame.grid_columnconfigure(
        0,
        weight=1
    )


    columns = (
        "ID",
        "Name",
        "Price",
        "Brand",
        "Category",
        "Stock"
    )


    tree = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings"
    )


    for col in columns:

        tree.heading(
            col,
            text=col
        )

        tree.column(
            col,
            anchor="center",
            width=120
        )


    tree.grid(
        row=1,
        column=0,
        sticky="nsew",
        padx=10,
        pady=10
    )


    scrollbar = ttk.Scrollbar(
        table_frame,
        orient="vertical",
        command=tree.yview
    )


    tree.configure(
        yscrollcommand=scrollbar.set
    )


    scrollbar.grid(
        row=1,
        column=1,
        sticky="ns"
    )


    # =====================================================
    # INITIAL LOAD
    # =====================================================

    load_products()


    return admin_frame