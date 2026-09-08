import customtkinter as ctk
from tkinter import ttk, messagebox
import os

from db import (
    get_products,
    add_product,
    delete_product,
    update_stock,
    update_product,
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