import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from db import (
    get_products,
    add_product as db_add_product,
    delete_product as db_delete_product,
    update_stock as db_update_stock
)

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class AdminScreen(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Pet Store Admin")
        self.geometry("1300x750")

        self.configure(fg_color="#EAF4FF")

        # =======================
        # GRID CONFIG
        # =======================
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.create_header()
        self.create_sidebar()
        self.create_table_section()
        self.load_products()
        

    # ===================================================
    # HEADER
    # ===================================================
    def create_header(self):

        header = ctk.CTkFrame(
            self,
            corner_radius=15,
            fg_color="#D9ECFF",
            height=80
        )
        header.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=15,
            pady=15
        )

        header.grid_columnconfigure(1, weight=1)

        title = ctk.CTkLabel(
            header,
            text="🐾 Pet Store Admin Dashboard",
            font=("Segoe UI", 28, "bold")
        )
        title.grid(row=0, column=0, padx=20, pady=20)

        self.search_entry = ctk.CTkEntry(
            header,
            width=300,
            placeholder_text="Search Product..."
        )
        self.search_entry.grid(
            row=0,
            column=2,
            padx=20
        )

    # ===================================================
    # SIDEBAR / PRODUCT FORM
    # ===================================================
    def create_sidebar(self):

        sidebar = ctk.CTkFrame(
            self,
            fg_color="#DFF1FF",
            corner_radius=15,
            width=300
        )

        sidebar.grid(
            row=1,
            column=0,
            sticky="ns",
            padx=(15, 8),
            pady=(0, 15)
        )

        sidebar.grid_columnconfigure(0, weight=1)

        heading = ctk.CTkLabel(
            sidebar,
            text="Add Product",
            font=("Segoe UI", 22, "bold")
        )
        heading.grid(row=0, column=0, pady=(20, 10))

        self.name_entry = ctk.CTkEntry(
            sidebar,
            placeholder_text="Product Name"
        )
        self.name_entry.grid(
            row=1,
            column=0,
            padx=20,
            pady=8,
            sticky="ew"
        )

        self.price_entry = ctk.CTkEntry(
            sidebar,
            placeholder_text="Price"
        )
        self.price_entry.grid(
            row=2,
            column=0,
            padx=20,
            pady=8,
            sticky="ew"
        )

        self.brand_entry = ctk.CTkEntry(
            sidebar,
            placeholder_text="Brand"
        )
        self.brand_entry.grid(
            row=3,
            column=0,
            padx=20,
            pady=8,
            sticky="ew"
        )

        self.category_entry = ctk.CTkEntry(
            sidebar,
            placeholder_text="Category"
        )
        self.category_entry.grid(
            row=4,
            column=0,
            padx=20,
            pady=8,
            sticky="ew"
        )

        self.stock_entry = ctk.CTkEntry(
            sidebar,
            placeholder_text="Initial Stock"
        )
        self.stock_entry.grid(
            row=5,
            column=0,
            padx=20,
            pady=8,
            sticky="ew"
        )

        add_btn = ctk.CTkButton(
            sidebar,
            text="➕ Add Product",
            height=40,
            command=self.add_product
        )
        add_btn.grid(
            row=6,
            column=0,
            padx=20,
            pady=(15, 10),
            sticky="ew"
        )

        delete_btn = ctk.CTkButton(
            sidebar,
            text="🗑 Remove Selected",
            fg_color="#D9534F",
            hover_color="#C9302C",
            height=40,
            command=self.delete_product
        )
        delete_btn.grid(
            row=7,
            column=0,
            padx=20,
            pady=10,
            sticky="ew"
        )

        stock_frame = ctk.CTkFrame(
            sidebar,
            fg_color="transparent"
        )
        stock_frame.grid(
            row=8,
            column=0,
            pady=20
        )

        plus_btn = ctk.CTkButton(
            stock_frame,
            text="+ Stock",
            width=100,
            command=self.increase_stock
        )
        plus_btn.grid(row=0, column=0, padx=5)

        minus_btn = ctk.CTkButton(
            stock_frame,
            text="- Stock",
            width=100,
            command=self.decrease_stock
        )
        minus_btn.grid(row=0, column=1, padx=5)

    # ===================================================
    # TABLE SECTION
    # ===================================================
    def create_table_section(self):

        table_frame = ctk.CTkFrame(
            self,
            fg_color="#F7FBFF",
            corner_radius=15
        )

        table_frame.grid(
            row=1,
            column=1,
            sticky="nsew",
            padx=(8, 15),
            pady=(0, 15)
        )

        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        style = ttk.Style()

        style.theme_use("default")

        style.configure(
            "Treeview",
            rowheight=35,
            font=("Segoe UI", 10),
        )

        columns = (
            "ID",
            "Name",
            "Price",
            "Brand",
            "Category",
            "Stock"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(
                col,
                anchor="center",
                width=120
            )

        self.tree.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=15,
            pady=15
        )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )

        self.tree.configure(
            yscrollcommand=scrollbar.set
        )

        scrollbar.grid(
            row=0,
            column=1,
            sticky="ns",
            pady=15
        )

    def load_products(self):

        for row in self.tree.get_children():
            self.tree.delete(row)

        products = get_products()

        for product in products:
            self.tree.insert("", "end", values=product)


    # ===================================================
    # BUTTON FUNCTIONS
    # ===================================================

    def add_product(self):

        name = self.name_entry.get()
        price = self.price_entry.get()
        brand = self.brand_entry.get()
        category = self.category_entry.get()
        stock = self.stock_entry.get()

        if not name or not price or not brand or not category or not stock:
            return

        try:
            price = float(price)
            stock = int(stock)
        except ValueError:
            return

        db_add_product((name, price, brand, category, stock))

        self.name_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)
        self.brand_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.stock_entry.delete(0, tk.END)

        self.load_products()

    def delete_product(self):

        selected = self.tree.selection()

        if not selected:
            return

        item = self.tree.item(selected[0])

        product_id = item["values"][0]

        db_delete_product(product_id)

        self.load_products()


    


    def increase_stock(self):

        selected = self.tree.selection()

        if not selected:
            return

        item = self.tree.item(selected[0])

        product_id = item["values"][0]
        current_stock = item["values"][5]

        db_update_stock(product_id, current_stock + 1)

        self.load_products()
    
    def decrease_stock(self):

        selected = self.tree.selection()

        if not selected:
            return

        item = self.tree.item(selected[0])

        product_id = item["values"][0]
        current_stock = item["values"][5]

        if current_stock > 0:
            db_update_stock(product_id, current_stock - 1)

            self.load_products()
    
    

if __name__ == "__main__":
    app = AdminScreen()
    app.mainloop()