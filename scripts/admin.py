import customtkinter as ctk
from tkinter import ttk

from db import (
    get_products,
    add_product,
    delete_product,
    update_stock
)

def create_admin_frame(container):

    admin_frame = ctk.CTkFrame(
        container,
        fg_color="#EAF4FF"
    )

    admin_frame.grid_rowconfigure(1, weight=1)
    admin_frame.grid_columnconfigure(1, weight=1)

    # ==========================
    # FUNCTIONS
    # ==========================

    def load_products():

        for row in tree.get_children():
            tree.delete(row)

        for product in get_products():
            tree.insert("", "end", values=product)

    def add_product_gui():

        try:
            add_product((
                name_entry.get(),
                float(price_entry.get()),
                brand_entry.get(),
                category_entry.get(),
                int(stock_entry.get())
            ))

            load_products()

            name_entry.delete(0, "end")
            price_entry.delete(0, "end")
            brand_entry.delete(0, "end")
            category_entry.delete(0, "end")
            stock_entry.delete(0, "end")

        except ValueError:
            print("Invalid Input")

    def delete_selected():

        selected = tree.selection()

        if not selected:
            return

        product_id = tree.item(selected[0])["values"][0]

        delete_product(product_id)

        load_products()

    def increase_stock():

        selected = tree.selection()

        if not selected:
            return

        values = tree.item(selected[0])["values"]

        update_stock(
            values[0],
            int(values[5]) + 1
        )

        load_products()

    def decrease_stock():

        selected = tree.selection()

        if not selected:
            return

        values = tree.item(selected[0])["values"]

        current_stock = int(values[5])

        if current_stock > 0:
            update_stock(
                values[0],
                current_stock - 1
            )

        load_products()

    # ==========================
    # HEADER
    # ==========================

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

    ctk.CTkLabel(
        header,
        text="🐾 Pet Store Admin",
        font=("Segoe UI", 28, "bold")
    ).pack(pady=15)

    # ==========================
    # SIDEBAR
    # ==========================

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
    name_entry.pack(padx=20, pady=10, fill="x")

    price_entry = ctk.CTkEntry(
        sidebar,
        placeholder_text="Price"
    )
    price_entry.pack(padx=20, pady=10, fill="x")

    brand_entry = ctk.CTkEntry(
        sidebar,
        placeholder_text="Brand"
    )
    brand_entry.pack(padx=20, pady=10, fill="x")

    category_entry = ctk.CTkEntry(
        sidebar,
        placeholder_text="Category"
    )
    category_entry.pack(padx=20, pady=10, fill="x")

    stock_entry = ctk.CTkEntry(
        sidebar,
        placeholder_text="Stock"
    )
    stock_entry.pack(padx=20, pady=10, fill="x")

    ctk.CTkButton(
        sidebar,
        text="➕ Add Product",
        command=add_product_gui
    ).pack(padx=20, pady=10, fill="x")

    ctk.CTkButton(
        sidebar,
        text="🗑 Remove Selected",
        command=delete_selected,
        fg_color="#D9534F"
    ).pack(padx=20, pady=10, fill="x")

    ctk.CTkButton(
        sidebar,
        text="+ Stock",
        command=increase_stock
    ).pack(padx=20, pady=10, fill="x")

    ctk.CTkButton(
        sidebar,
        text="- Stock",
        command=decrease_stock
    ).pack(padx=20, pady=10, fill="x")

    # ==========================
    # TABLE
    # ==========================

    table_frame = ctk.CTkFrame(admin_frame)

    table_frame.grid(
        row=1,
        column=1,
        sticky="nsew",
        padx=(8, 15),
        pady=(0, 15)
    )

    table_frame.grid_rowconfigure(0, weight=1)
    table_frame.grid_columnconfigure(0, weight=1)

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
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=120)

    tree.grid(
        row=0,
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
        row=0,
        column=1,
        sticky="ns"
    )

    load_products()

    return admin_frame
    

    