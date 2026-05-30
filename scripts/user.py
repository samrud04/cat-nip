import customtkinter as ctk
import tkinter as tk
import db

def user_screen(container):
    products = db.get_products() # Returns a list of tuples

    cart = {}
    
    # Create the main user screen frame
    user_screen = ctk.CTkFrame(container, fg_color="white")
    user_screen.grid(row=0, column=0, sticky="nsew")

    user_screen.grid_rowconfigure(0, weight=1)
    user_screen.grid_columnconfigure(0, weight=1)

    return user_screen

