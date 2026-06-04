import customtkinter as ctk
import tkinter as tk
import db
from scripts.user import user_screen

def admin_screen(container):
    #products = db.get_products() # Returns a list of tuples

    #cart = {}
    
    # Create the main user screen frame
    admin_screen = ctk.CTkFrame(container, fg_color="white")
    admin_screen.grid(row=0, column=0, sticky="nsew")

    admin_screen.grid_rowconfigure(0, weight=1)
    admin_screen.grid_columnconfigure(0, weight=1)

    return admin_screen

