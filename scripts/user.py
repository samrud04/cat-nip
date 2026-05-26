user_screen = ctk.CTkFrame(container, fg_color="white", width=800, height=600)
    user_screen.grid(row=0, column=0, sticky="nsew")   
    user_screen.grid_rowconfigure(0, weight=1)
    user_screen.grid_columnconfigure(0, weight=1)

    user_screen_main = ctk.CTkScrollableFrame(user_screen, fg_color="#feefb5", width=800, height=520, corner_radius=20)
    user_screen_main.grid(row=0, column=0, sticky="nsew", padx=(30, 30), pady=(30, 20))   
    user_screen_main.grid_rowconfigure(0, weight=0)
    user_screen_main.grid_columnconfigure(0, weight=0)
    user_screen_main.grid_columnconfigure(1, weight=0)

    user_screen_nav = ctk.CTkFrame(user_screen, fg_color="#fbe58c", width=800, height=80, corner_radius=20)
    user_screen_nav.grid(row=1, column=0, sticky="nsew", padx=(30, 30), pady=(0, 30))   
    user_screen_nav.grid_rowconfigure(0, weight=0)
    user_screen_nav.grid_columnconfigure(0, weight=0)
    user_screen_nav.grid_columnconfigure(1, weight=0)

    ctk.CTkButton(
        user_screen,
        text="Back",
        command=lambda: show_frame(login),
        width=100,
        height=40,
        fg_color="tomato",
        text_color="black",
        hover_color="#FC846F",
        bg_color="#ffea00",
        font=("Arial", 16, "bold")
    ).place(x=50,y=50)

    order_icon = ctk.CTkImage(Image.open("./assets/order_icon.png"), size=(20, 20))
    book_icon = ctk.CTkImage(Image.open("./assets/book_icon.png"), size=(20, 20))
    settings_icon = ctk.CTkImage(Image.open("./assets/settings_icon.png"), size=(20, 20))

    order_button = ctk.CTkButton(
        user_screen_nav,
        text=" Order",
        image=order_icon,
        compound="left",
        font=("Arial", 16, "bold"),
        corner_radius=12,
        fg_color="#f9b746", 
        text_color="black",
        hover_color="#e0a73d",
        width=250,
        height=60
    ).place(x=50, y=10)

    book_button = ctk.CTkButton(
        user_screen_nav,
        text=" Book",
        image=book_icon,
        compound="left",
        font=("Arial", 16, "bold"),
        corner_radius=12,
        fg_color="#f9b746", 
        text_color="black",
        hover_color="#e0a73d",
        width=250,
        height=60
    ).place(x=620, y=10)

    settings_button = ctk.CTkButton(
        user_screen_nav,
        text=" Settings",
        image=settings_icon,
        compound="left",
        font=("Arial", 16, "bold"),
        corner_radius=12,
        fg_color="#f9b746", 
        text_color="black",
        hover_color="#e0a73d",
        width=250,
        height=60
    ).place(x=1200, y=10)

    ctk.CTkLabel(
        user_screen_main, 
        text="Search:", 
        font=("Arial", 24), 
        text_color="black", 
        fg_color="#feefb5"
    ).grid(row=0, column=0, sticky="w",padx=10, pady=120)

    user_search_entry_order = ctk.CTkEntry(
        user_screen_main,
        placeholder_text="eg: Cat Food",
        width=400,
        height=35,
        fg_color="white",
        text_color="black",
        font=("Arial", 16))
    
    


    user_search_entry_order.grid(row=0, column=1, sticky="w", pady=120)
    ctk.CTkLabel(
        user_screen_main, 
        text="CATEGORY:", 
        font=("Arial", 16), 
        text_color="black", 
        fg_color="#feefb5"
    ).grid(row=1, column=0, sticky="w", padx=10)
    category=tk.Spinbox(
        user_screen_main,
        values=[" Food", "Toys", "Accessories"],
        width=20,
        font=("Arial", 14)
    )
    category.grid(row=1, column=1, sticky="w", pady=10)
    def categ():
        global category
        category = category.get()
        if category == "pet Food":
            user_search_entry_order.configure(placeholder_text="eg: Whiskas, Meow Mix")
        elif category == "Toys":
            user_search_entry_order.configure(placeholder_text="eg: Catnip Mouse, Feather Wand")
        elif category == "Accessories":
            user_search_entry_order.configure(placeholder_text="eg: Cat Bed, Scratching Post")
    category.bind("<<ComboboxSelected>>", lambda e: categ())
    ctk.CTkButton(
        user_screen_main,
        text="DONE",
        command=categ
    ).grid(row=2, column=1, sticky="w", pady=10)
    
