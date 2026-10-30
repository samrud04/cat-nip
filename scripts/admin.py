import customtkinter as ctk
from tkinter import ttk, messagebox
import os

from adoption import open_adoption_admin
from playdates import open_playdates_admin

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

    admin_frame = ctk.CTkFrame(
        container,
        fg_color=("#F1F5F9", "#0F172A")
    )

    admin_frame.grid_columnconfigure(0, weight=0)  # Left Full Sidebar
    admin_frame.grid_columnconfigure(1, weight=1)  # Main Content Area
    admin_frame.grid_rowconfigure(0, weight=1)

    
    style = ttk.Style()
    style.theme_use("clam")

    style.configure(
        "CatNip.Treeview",
        background="#1E293B",
        foreground="#F8FAFC",
        fieldbackground="#1E293B",
        rowheight=34,
        font=("Segoe UI", 10),
        borderwidth=0
    )
    style.configure(
        "CatNip.Treeview.Heading",
        background="#0F172A",
        foreground="#38BDF8",
        font=("Segoe UI", 10, "bold"),
        relief="flat",
        padding=(8, 8)
    )
    style.map(
        "CatNip.Treeview",
        background=[("selected", "#0284C7")],
        foreground=[("selected", "#FFFFFF")]
    )
    style.map(
        "CatNip.Treeview.Heading",
        background=[("active", "#1E293B")]
    )


    # =====================================================
    # LOGOUT
    # =====================================================

    def logout():
        if os.path.exists("session.txt"):
            os.remove("session.txt")
        show_frame("login")


    # =====================================================
    # LOAD PRODUCTS & STATS
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
            background="#450A0A",
            foreground="#FCA5A5"
        )

        total_products_label.configure(text=str(total_products))
        low_stock_label.configure(text=str(low_stock))
        inventory_value_label.configure(text=f"₹{inventory_value:,.2f}")


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
            messagebox.showerror("Error", "Please enter a product name.")
            return

        if not price:
            messagebox.showerror("Error", "Please enter a price.")
            return

        if not brand:
            messagebox.showerror("Error", "Please enter a brand.")
            return

        if category == "Select Category":
            messagebox.showerror("Error", "Please select a category.")
            return

        if not stock:
            messagebox.showerror("Error", "Please enter the stock quantity.")
            return

        try:
            price = float(price)
            stock = int(stock)
        except ValueError:
            messagebox.showerror("Invalid Input", "Price must be a number and stock must be a whole number.")
            return

        if price <= 0:
            messagebox.showerror("Invalid Price", "Price must be greater than 0.")
            return

        if stock < 0:
            messagebox.showerror("Invalid Stock", "Stock cannot be negative.")
            return

        add_product((
            product_name,
            price,
            brand,
            category,
            stock
        ))

        load_products()

        name_entry.delete(0, "end")
        price_entry.delete(0, "end")
        brand_entry.delete(0, "end")
        category_entry.set("Select Category")
        stock_entry.delete(0, "end")

        messagebox.showinfo("Success", f"{product_name} was added successfully!")


    # =====================================================
    # DELETE PRODUCT
    # =====================================================

    def delete_selected():
        selected = tree.selection()

        if not selected:
            messagebox.showerror("Error", "Please select a product to delete.")
            return

        values = tree.item(selected[0])["values"]
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
        messagebox.showinfo("Success", f"'{product_name}' was deleted successfully.")


    # =====================================================
    # EDIT PRODUCT
    # =====================================================

    def edit_selected():
        selected = tree.selection()

        if not selected:
            messagebox.showerror("Error", "Please select a product to edit.")
            return

        values = tree.item(selected[0])["values"]
        product_id = values[0]

        name_entry.delete(0, "end")
        name_entry.insert(0, values[1])

        price_entry.delete(0, "end")
        price_entry.insert(0, values[2])

        brand_entry.delete(0, "end")
        brand_entry.insert(0, values[3])

        category_entry.set(values[4])

        stock_entry.delete(0, "end")
        stock_entry.insert(0, values[5])

        edit_button.configure(
            text="💾 Save Changes",
            fg_color="#10B981",
            hover_color="#059669",
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
            messagebox.showerror("Error", "Please fill all fields.")
            return

        if category == "Select Category":
            messagebox.showerror("Error", "Please select a category.")
            return

        try:
            price = float(price)
            stock = int(stock)
        except ValueError:
            messagebox.showerror("Invalid Input", "Price and stock must be valid numbers.")
            return

        if price <= 0 or stock < 0:
            messagebox.showerror("Error", "Enter valid price and stock.")
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
        category_entry.set("Select Category")
        stock_entry.delete(0, "end")

        edit_button.configure(
            text="✏️ Edit Selected",
            fg_color="#334155",
            hover_color="#475569",
            command=edit_selected
        )

        messagebox.showinfo("Success", f"{product_name} was updated successfully!")


    # =====================================================
    # INCREASE STOCK
    # =====================================================

    def increase_stock():
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a product.")
            return

        values = tree.item(selected[0])["values"]
        update_stock(values[0], int(values[5]) + 1)
        load_products()


    # =====================================================
    # DECREASE STOCK
    # =====================================================

    def decrease_stock():
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a product.")
            return

        values = tree.item(selected[0])["values"]
        product_id = values[0]
        product_name = values[1]
        current_stock = int(values[5])

        if current_stock == 0:
            messagebox.showwarning("Out of Stock", f"{product_name} is already out of stock.")
            return

        new_stock = current_stock - 1
        update_stock(product_id, new_stock)
        load_products()

        if new_stock == 0:
            messagebox.showwarning("Out of Stock", f"{product_name} is now out of stock.")
        elif new_stock < 5:
            messagebox.showwarning("Low Stock", f"{product_name} has only {new_stock} item(s) left.")


    # =====================================================
    # SEARCH PRODUCTS
    # =====================================================

    def search_products():
        search_text = search_entry.get().lower().strip()

        for row in tree.get_children():
            tree.delete(row)

        for product in get_products():
            product_text = " ".join(str(value) for value in product).lower()
            if search_text in product_text:
                tree.insert("", "end", values=product)


    # =====================================================
    # ORDER MANAGEMENT WINDOW 
    # =====================================================

    def open_order_management():
        order_window = ctk.CTkToplevel(admin_frame)
        order_window.title("Cat Nip — Order Management")
        order_window.geometry("1120x720")
        order_window.minsize(880, 580)
        order_window.configure(fg_color=("#F1F5F9", "#0F172A"))
        order_window.grab_set()

        modal_header = ctk.CTkFrame(order_window, corner_radius=12, fg_color=("#FFFFFF", "#1E293B"), border_width=1, border_color=("#E2E8F0", "#334155"))
        modal_header.pack(fill="x", padx=18, pady=(18, 12))

        ctk.CTkLabel(
            modal_header,
            text="📦 Order Management",
            font=("Segoe UI", 22, "bold"),
            text_color="#38BDF8"
        ).pack(anchor="w", padx=20, pady=(14, 2))

        ctk.CTkLabel(
            modal_header,
            text="Review purchases, view order contents, and update delivery status.",
            font=("Segoe UI", 12),
            text_color="#94A3B8"
        ).pack(anchor="w", padx=20, pady=(0, 14))

        content = ctk.CTkFrame(order_window, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=18, pady=(0, 18))
        content.grid_columnconfigure(0, weight=3)
        content.grid_columnconfigure(1, weight=2)
        content.grid_rowconfigure(0, weight=1)

        orders_panel = ctk.CTkFrame(content, corner_radius=12, fg_color=("#FFFFFF", "#1E293B"), border_width=1, border_color=("#E2E8F0", "#334155"))
        orders_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        orders_panel.grid_columnconfigure(0, weight=1)
        orders_panel.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            orders_panel, text="All Orders", font=("Segoe UI", 16, "bold"), text_color="#38BDF8"
        ).grid(row=0, column=0, sticky="w", padx=16, pady=(14, 8))

        order_columns = ("Order ID", "Customer", "Date", "Total", "Status", "Items")
        orders_tree = ttk.Treeview(
            orders_panel, columns=order_columns, show="headings", height=18, style="CatNip.Treeview"
        )
        for col in order_columns:
            orders_tree.heading(col, text=col)
            orders_tree.column(col, anchor="center", width=100)
        orders_tree.column("Customer", width=120)
        orders_tree.column("Date", width=145)
        orders_tree.grid(row=1, column=0, sticky="nsew", padx=(14, 0), pady=(0, 14))

        orders_scroll = ttk.Scrollbar(orders_panel, orient="vertical", command=orders_tree.yview)
        orders_tree.configure(yscrollcommand=orders_scroll.set)
        orders_scroll.grid(row=1, column=1, sticky="ns", pady=(0, 14), padx=(0, 8))

        right_panel = ctk.CTkFrame(content, corner_radius=12, fg_color=("#FFFFFF", "#1E293B"), border_width=1, border_color=("#E2E8F0", "#334155"))
        right_panel.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
        right_panel.grid_columnconfigure(0, weight=1)
        right_panel.grid_rowconfigure(2, weight=1)

        ctk.CTkLabel(
            right_panel, text="Order Details", font=("Segoe UI", 16, "bold"), text_color="#38BDF8"
        ).grid(row=0, column=0, sticky="w", padx=16, pady=(14, 6))

        customer_card = ctk.CTkFrame(right_panel, corner_radius=8, fg_color=("#F8FAFC", "#0F172A"))
        customer_card.grid(row=1, column=0, sticky="ew", padx=14, pady=4)
        customer_label = ctk.CTkLabel(
            customer_card, text="Select an order to view its details.",
            justify="left", anchor="w", wraplength=340, font=("Segoe UI", 12)
        )
        customer_label.pack(fill="both", padx=12, pady=10)

        item_columns = ("Product", "Qty", "Unit Price")
        items_tree = ttk.Treeview(right_panel, columns=item_columns, show="headings", height=8, style="CatNip.Treeview")
        for col in item_columns:
            items_tree.heading(col, text=col)
            items_tree.column(col, anchor="center", width=95)
        items_tree.column("Product", width=160, anchor="w")
        items_tree.grid(row=2, column=0, sticky="nsew", padx=14, pady=10)

        status_frame = ctk.CTkFrame(right_panel, fg_color="transparent")
        status_frame.grid(row=3, column=0, sticky="ew", padx=14, pady=(4, 14))
        status_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(status_frame, text="Update Status:", font=("Segoe UI", 12, "bold")).grid(
            row=0, column=0, sticky="w", pady=(0, 4)
        )
        status_picker = ctk.CTkComboBox(
            status_frame,
            values=["Placed", "Processing", "Shipped", "Delivered", "Cancelled"],
            state="readonly",
            height=36
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
                          f"Email: {email or '—'}  |  Phone: {phone or '—'}\n"
                          f"Address: {address or '—'}\nDate: {date_text}\n"
                          f"Total: ₹{float(total):,.2f}  |  Status: {status or 'Placed'}")
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
            status_frame, text="💾 Update Order Status", command=save_status,
            height=36, font=("Segoe UI", 12, "bold"), fg_color="#10B981", hover_color="#059669"
        ).grid(row=2, column=0, sticky="ew", pady=(0, 6))

        ctk.CTkButton(
            status_frame, text="🔄 Refresh Orders",
            command=lambda: refresh_order_list(selected_order["id"]),
            height=34, font=("Segoe UI", 12), fg_color="#334155", hover_color="#475569"
        ).grid(row=3, column=0, sticky="ew")

        refresh_order_list()


    # =====================================================
    # BOOKING MANAGEMENT WINDOW
    # =====================================================

    def open_booking_management():
        booking_window = ctk.CTkToplevel(admin_frame)
        booking_window.title("Cat Nip — Booking Management")
        booking_window.geometry("1140x720")
        booking_window.minsize(890, 580)
        booking_window.configure(fg_color=("#F1F5F9", "#0F172A"))
        booking_window.grab_set()

        modal_header = ctk.CTkFrame(booking_window, corner_radius=12, fg_color=("#FFFFFF", "#1E293B"), border_width=1, border_color=("#E2E8F0", "#334155"))
        modal_header.pack(fill="x", padx=18, pady=(18, 12))

        ctk.CTkLabel(
            modal_header,
            text="📅 Booking Management",
            font=("Segoe UI", 22, "bold"),
            text_color="#0D9488"
        ).pack(anchor="w", padx=20, pady=(14, 2))

        ctk.CTkLabel(
            modal_header,
            text="Review service appointments, customer details, and update booking status.",
            font=("Segoe UI", 12),
            text_color="#94A3B8"
        ).pack(anchor="w", padx=20, pady=(0, 14))

        content = ctk.CTkFrame(booking_window, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=18, pady=(0, 18))
        content.grid_columnconfigure(0, weight=3)
        content.grid_columnconfigure(1, weight=2)
        content.grid_rowconfigure(0, weight=1)

        left = ctk.CTkFrame(content, corner_radius=12, fg_color=("#FFFFFF", "#1E293B"), border_width=1, border_color=("#E2E8F0", "#334155"))
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        left.grid_columnconfigure(0, weight=1)
        left.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(left, text="All Bookings", font=("Segoe UI", 16, "bold"), text_color="#0D9488").grid(
            row=0, column=0, sticky="w", padx=16, pady=(14, 8)
        )

        columns = ("Booking ID", "Customer", "Service", "Pet", "Date", "Status")
        bookings_tree = ttk.Treeview(left, columns=columns, show="headings", height=18, style="CatNip.Treeview")
        for col in columns:
            bookings_tree.heading(col, text=col)
            bookings_tree.column(col, anchor="center", width=95)
        bookings_tree.column("Booking ID", width=85)
        bookings_tree.column("Customer", width=110)
        bookings_tree.column("Service", width=120)
        bookings_tree.column("Pet", width=90)
        bookings_tree.column("Date", width=100)
        bookings_tree.grid(row=1, column=0, sticky="nsew", padx=(14, 0), pady=(0, 14))

        scrollbar = ttk.Scrollbar(left, orient="vertical", command=bookings_tree.yview)
        bookings_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=1, column=1, sticky="ns", pady=(0, 14), padx=(0, 8))

        right = ctk.CTkFrame(content, corner_radius=12, fg_color=("#FFFFFF", "#1E293B"), border_width=1, border_color=("#E2E8F0", "#334155"))
        right.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
        right.grid_columnconfigure(0, weight=1)
        right.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(right, text="Booking Details", font=("Segoe UI", 16, "bold"), text_color="#0D9488").grid(
            row=0, column=0, sticky="w", padx=16, pady=(14, 6)
        )

        details = ctk.CTkTextbox(right, height=270, wrap="word", corner_radius=8, font=("Segoe UI", 12))
        details.grid(row=1, column=0, sticky="nsew", padx=14, pady=8)
        details.insert("1.0", "Select a booking to view its details.")
        details.configure(state="disabled")

        status_frame = ctk.CTkFrame(right, fg_color="transparent")
        status_frame.grid(row=2, column=0, sticky="ew", padx=14, pady=(4, 14))
        status_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(status_frame, text="Update Status:", font=("Segoe UI", 12, "bold")).grid(
            row=0, column=0, sticky="w", pady=(0, 4)
        )
        status_picker = ctk.CTkComboBox(
            status_frame,
            values=["Pending", "Confirmed", "In Progress", "Completed", "Cancelled"],
            state="readonly",
            height=36
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
                    f"Email: {email or '—'}  |  Phone: {phone or '—'}\n\n"
                    f"Service: {service or '—'}\n"
                    f"Pet Name: {pet or '—'}\n"
                    f"Appointment Date: {date_text}\n"
                    f"Current Status: {status or 'Pending'}\n"
                    f"Created: {created_text}\n\n"
                    f"Customer Notes:\n{notes or 'No additional notes.'}"
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

        ctk.CTkButton(
            status_frame, text="💾 Update Booking Status", command=save_booking_status,
            height=36, font=("Segoe UI", 12, "bold"), fg_color="#10B981", hover_color="#059669"
        ).grid(row=2, column=0, sticky="ew", pady=(0, 6))

        ctk.CTkButton(
            status_frame, text="🔄 Refresh Bookings",
            command=lambda: refresh_booking_list(selected["id"]),
            height=34, font=("Segoe UI", 12), fg_color="#334155", hover_color="#475569"
        ).grid(row=3, column=0, sticky="ew")

        refresh_booking_list()


    sidebar = ctk.CTkFrame(
        admin_frame,
        width=245,
        corner_radius=0,
        fg_color=("#F1F5F9", "#0F172A")
    )
    sidebar.grid(row=0, column=0, sticky="nsew")
    sidebar.grid_propagate(False)

    # Brand Title
    brand_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
    brand_frame.pack(fill="x", padx=16, pady=(22, 20))

    ctk.CTkLabel(brand_frame, text="🐾", font=("Segoe UI", 30)).pack(side="left", padx=(0, 8))
    title_box = ctk.CTkFrame(brand_frame, fg_color="transparent")
    title_box.pack(side="left")
    ctk.CTkLabel(
        title_box,
        text="Cat Nip Admin",
        font=("Segoe UI", 17, "bold"),
        text_color="#38BDF8"
    ).pack(anchor="w")
    ctk.CTkLabel(
        title_box,
        text="Store Management",
        font=("Segoe UI", 10),
        text_color="#94A3B8"
    ).pack(anchor="w")

    # Divider
    ctk.CTkFrame(sidebar, height=1, fg_color=("#CBD5E1", "#334155")).pack(fill="x", padx=14, pady=(0, 15))

    # Navigation Buttons 
    ctk.CTkLabel(
        sidebar,
        text="STORE MODULES",
        font=("Segoe UI", 10, "bold"),
        text_color="#64748B"
    ).pack(anchor="w", padx=20, pady=(0, 6))

    ctk.CTkButton(
        sidebar,
        text="📦  Manage Orders",
        command=open_order_management,
        anchor="w",
        font=("Segoe UI", 12, "bold"),
        height=40,
        fg_color="#0284C7",
        hover_color="#0369A1"
    ).pack(fill="x", padx=14, pady=3)

    ctk.CTkButton(
        sidebar,
        text="📅  Manage Bookings",
        command=open_booking_management,
        anchor="w",
        font=("Segoe UI", 12, "bold"),
        height=40,
        fg_color="#0D9488",
        hover_color="#0F766E"
    ).pack(fill="x", padx=14, pady=3)

    ctk.CTkButton(
        sidebar,
        text="🐾  Adoption Requests",
        command=lambda: open_adoption_admin(admin_frame),
        anchor="w",
        font=("Segoe UI", 12, "bold"),
        height=40,
        fg_color="#EA580C",
        hover_color="#C2410C"
    ).pack(fill="x", padx=14, pady=3)

    ctk.CTkButton(
        sidebar,
        text="🐕  Manage Playdates",
        command=lambda: open_playdates_admin(admin_frame),
        anchor="w",
        font=("Segoe UI", 12, "bold"),
        height=40,
        fg_color="#7C3AED",
        hover_color="#6D28D9"
    ).pack(fill="x", padx=14, pady=3)

    # Bottom of Sidebar (Status & Logout)
    bottom_box = ctk.CTkFrame(sidebar, fg_color="transparent")
    bottom_box.pack(side="bottom", fill="x", padx=14, pady=20)

    ctk.CTkLabel(
        bottom_box,
        text="🟢 Admin Session Active",
        font=("Segoe UI", 11),
        text_color="#10B981"
    ).pack(anchor="w", pady=(0, 10))

    ctk.CTkButton(
        bottom_box,
        text="🚪  Logout",
        command=logout,
        font=("Segoe UI", 12, "bold"),
        height=38,
        fg_color="#EF4444",
        hover_color="#DC2626"
    ).pack(fill="x")


    # =====================================================
    # RIGHT MAIN CONTENT AREA
    # =====================================================

    main_content = ctk.CTkFrame(admin_frame, fg_color="transparent")
    main_content.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
    main_content.grid_rowconfigure(2, weight=1)
    main_content.grid_columnconfigure(0, weight=1)

    # Top Header Title
    top_header = ctk.CTkFrame(main_content, fg_color="transparent")
    top_header.grid(row=0, column=0, sticky="ew", pady=(0, 14))

    ctk.CTkLabel(
        top_header,
        text="Store Management Dashboard",
        font=("Segoe UI", 24, "bold"),
        text_color=("#0F172A", "#F8FAFC")
    ).pack(anchor="w")

    ctk.CTkLabel(
        top_header,
        text="Live inventory metrics, stock manipulation & item management",
        font=("Segoe UI", 12),
        text_color="#94A3B8"
    ).pack(anchor="w", pady=(2, 0))


    # =====================================================
    # KPI METRIC CARDS ROW
    # =====================================================

    stats_row = ctk.CTkFrame(main_content, fg_color="transparent")
    stats_row.grid(row=1, column=0, sticky="ew", pady=(0, 14))
    stats_row.columnconfigure((0, 1, 2), weight=1)

    # Card 1: Total Products
    card_prod = ctk.CTkFrame(stats_row, corner_radius=12, fg_color=("#FFFFFF", "#1E293B"), border_width=1, border_color=("#E2E8F0", "#334155"))
    card_prod.grid(row=0, column=0, padx=(0, 8), sticky="ew")
    top_p = ctk.CTkFrame(card_prod, fg_color="transparent")
    top_p.pack(fill="x", padx=16, pady=(12, 2))
    ctk.CTkLabel(top_p, text="Total Products", font=("Segoe UI", 12), text_color="#94A3B8").pack(side="left")
    ctk.CTkLabel(top_p, text="📦", font=("Segoe UI", 16)).pack(side="right")
    total_products_label = ctk.CTkLabel(card_prod, text="0", font=("Segoe UI", 26, "bold"), text_color="#38BDF8")
    total_products_label.pack(anchor="w", padx=16, pady=(0, 12))

    # Card 2: Low Stock Alert
    card_stock = ctk.CTkFrame(stats_row, corner_radius=12, fg_color=("#FFFFFF", "#1E293B"), border_width=1, border_color=("#E2E8F0", "#334155"))
    card_stock.grid(row=0, column=1, padx=4, sticky="ew")
    top_s = ctk.CTkFrame(card_stock, fg_color="transparent")
    top_s.pack(fill="x", padx=16, pady=(12, 2))
    ctk.CTkLabel(top_s, text="Low Stock (< 5 items)", font=("Segoe UI", 12), text_color="#94A3B8").pack(side="left")
    ctk.CTkLabel(top_s, text="⚠️", font=("Segoe UI", 16)).pack(side="right")
    low_stock_label = ctk.CTkLabel(card_stock, text="0", font=("Segoe UI", 26, "bold"), text_color="#EF4444")
    low_stock_label.pack(anchor="w", padx=16, pady=(0, 12))

    # Card 3: Inventory Value
    card_val = ctk.CTkFrame(stats_row, corner_radius=12, fg_color=("#FFFFFF", "#1E293B"), border_width=1, border_color=("#E2E8F0", "#334155"))
    card_val.grid(row=0, column=2, padx=(8, 0), sticky="ew")
    top_v = ctk.CTkFrame(card_val, fg_color="transparent")
    top_v.pack(fill="x", padx=16, pady=(12, 2))
    ctk.CTkLabel(top_v, text="Inventory Value", font=("Segoe UI", 12), text_color="#94A3B8").pack(side="left")
    ctk.CTkLabel(top_v, text="💰", font=("Segoe UI", 16)).pack(side="right")
    inventory_value_label = ctk.CTkLabel(card_val, text="₹0.00", font=("Segoe UI", 24, "bold"), text_color="#10B981")
    inventory_value_label.pack(anchor="w", padx=16, pady=(0, 12))


    # =====================================================
    # 5. WORKSPACE (PRODUCT FORM CARD + TABLE CARD)
    # =====================================================

    workspace = ctk.CTkFrame(main_content, fg_color="transparent")
    workspace.grid(row=2, column=0, sticky="nsew")
    workspace.grid_columnconfigure(0, weight=0)  # Form Card
    workspace.grid_columnconfigure(1, weight=1)  # Table Card
    workspace.grid_rowconfigure(0, weight=1)

    # -----------------------------------------------------
    # PRODUCT FORM CARD
    # -----------------------------------------------------
    form_card = ctk.CTkFrame(
        workspace,
        width=310,
        corner_radius=14,
        fg_color=("#FFFFFF", "#1E293B"),
        border_width=1,
        border_color=("#E2E8F0", "#334155")
    )
    form_card.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
    form_card.grid_propagate(False)

    form_scroll = ctk.CTkScrollableFrame(form_card, fg_color="transparent")
    form_scroll.pack(fill="both", expand=True, padx=14, pady=14)

    ctk.CTkLabel(
        form_scroll,
        text="🏷️ Product Controls",
        font=("Segoe UI", 16, "bold"),
        text_color="#38BDF8"
    ).pack(anchor="w", pady=(0, 10))

    ctk.CTkLabel(form_scroll, text="Product Name", font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(2, 2))
    name_entry = ctk.CTkEntry(form_scroll, placeholder_text="e.g. Feather Wand", height=36)
    name_entry.pack(fill="x", pady=(0, 6))

    ctk.CTkLabel(form_scroll, text="Price (₹)", font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(2, 2))
    price_entry = ctk.CTkEntry(form_scroll, placeholder_text="e.g. 499.00", height=36)
    price_entry.pack(fill="x", pady=(0, 6))

    ctk.CTkLabel(form_scroll, text="Brand", font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(2, 2))
    brand_entry = ctk.CTkEntry(form_scroll, placeholder_text="e.g. CatNip Co", height=36)
    brand_entry.pack(fill="x", pady=(0, 6))

    ctk.CTkLabel(form_scroll, text="Category", font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(2, 2))
    category_entry = ctk.CTkComboBox(
        form_scroll,
        values=["Food", "Accessory"],
        height=36,
        state="readonly"
    )
    category_entry.set("Select Category")
    category_entry.pack(fill="x", pady=(0, 6))

    ctk.CTkLabel(form_scroll, text="Stock Quantity", font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(2, 2))
    stock_entry = ctk.CTkEntry(form_scroll, placeholder_text="e.g. 20", height=36)
    stock_entry.pack(fill="x", pady=(0, 12))

    # Add Product Button
    ctk.CTkButton(
        form_scroll,
        text="➕ Add Product",
        command=add_product_gui,
        height=38,
        font=("Segoe UI", 12, "bold"),
        fg_color="#0284C7",
        hover_color="#0369A1"
    ).pack(fill="x", pady=4)

    # Edit Selected Button
    edit_button = ctk.CTkButton(
        form_scroll,
        text="✏️ Edit Selected",
        command=edit_selected,
        height=36,
        font=("Segoe UI", 12),
        fg_color="#334155",
        hover_color="#475569"
    )
    edit_button.pack(fill="x", pady=4)

    # Quick Stock Adjustment Side-by-Side Grid
    stock_grid = ctk.CTkFrame(form_scroll, fg_color="transparent")
    stock_grid.pack(fill="x", pady=4)
    stock_grid.columnconfigure((0, 1), weight=1)

    ctk.CTkButton(
        stock_grid,
        text="▲ +1 Stock",
        command=increase_stock,
        height=34,
        font=("Segoe UI", 11, "bold"),
        fg_color="#10B981",
        hover_color="#059669"
    ).grid(row=0, column=0, padx=(0, 4), sticky="ew")

    ctk.CTkButton(
        stock_grid,
        text="▼ -1 Stock",
        command=decrease_stock,
        height=34,
        font=("Segoe UI", 11, "bold"),
        fg_color="#F59E0B",
        hover_color="#D97706"
    ).grid(row=0, column=1, padx=(4, 0), sticky="ew")

    # Delete Selected Button
    ctk.CTkButton(
        form_scroll,
        text="🗑️ Remove Selected",
        command=delete_selected,
        height=36,
        font=("Segoe UI", 12),
        fg_color="#EF4444",
        hover_color="#DC2626"
    ).pack(fill="x", pady=(8, 4))


    # -----------------------------------------------------
    # PRODUCT TABLE CARD
    # -----------------------------------------------------
    table_card = ctk.CTkFrame(
        workspace,
        corner_radius=14,
        fg_color=("#FFFFFF", "#1E293B"),
        border_width=1,
        border_color=("#E2E8F0", "#334155")
    )
    table_card.grid(row=0, column=1, sticky="nsew")
    table_card.grid_rowconfigure(1, weight=1)
    table_card.grid_columnconfigure(0, weight=1)

    # Search Bar Toolbar
    search_frame = ctk.CTkFrame(table_card, fg_color="transparent")
    search_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=16, pady=(14, 10))
    search_frame.grid_columnconfigure(0, weight=1)

    search_entry = ctk.CTkEntry(
        search_frame,
        placeholder_text="🔎 Search by product name, brand, category...",
        height=38,
        font=("Segoe UI", 12)
    )
    search_entry.grid(row=0, column=0, sticky="ew", padx=(0, 8))
    search_entry.bind("<Return>", lambda e: search_products())

    ctk.CTkButton(
        search_frame,
        text="Search",
        width=90,
        height=38,
        font=("Segoe UI", 12, "bold"),
        fg_color="#0284C7",
        hover_color="#0369A1",
        command=search_products
    ).grid(row=0, column=1, padx=4)

    ctk.CTkButton(
        search_frame,
        text="Clear",
        width=75,
        height=38,
        font=("Segoe UI", 12),
        fg_color="#64748B",
        hover_color="#475569",
        command=lambda: (search_entry.delete(0, "end"), load_products())
    ).grid(row=0, column=2, padx=4)

    ctk.CTkButton(
        search_frame,
        text="🔄 Refresh",
        width=95,
        height=38,
        font=("Segoe UI", 12),
        fg_color="#334155",
        hover_color="#475569",
        command=load_products
    ).grid(row=0, column=3, padx=(4, 0))

    # Product Table
    columns = (
        "ID",
        "Name",
        "Price",
        "Brand",
        "Category",
        "Stock"
    )

    tree = ttk.Treeview(
        table_card,
        columns=columns,
        show="headings",
        style="CatNip.Treeview"
    )

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=120)

    tree.column("ID", width=70)
    tree.column("Name", width=220, anchor="w")
    tree.column("Brand", width=140)
    tree.column("Category", width=120)

    tree.grid(row=1, column=0, sticky="nsew", padx=(16, 0), pady=(0, 16))

    scrollbar = ttk.Scrollbar(
        table_card,
        orient="vertical",
        command=tree.yview
    )
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.grid(row=1, column=1, sticky="ns", pady=(0, 16), padx=(0, 10))

    # Initial Load
    load_products()

    return admin_frame