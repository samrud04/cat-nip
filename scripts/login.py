login = ctk.CTkFrame(container, fg_color="white", width=800, height=600)
    login.grid(row=0, column=0, sticky="nsew")

    login.grid_columnconfigure(0, weight=1)
    login.grid_columnconfigure(1, weight=1)
    login.grid_rowconfigure(0, weight=1)

    login_lframe = ctk.CTkFrame(login, fg_color="#ffe683",width=200, height=300)
    login_lframe.grid(row=0, column=0, sticky="nsew",padx=(40,40), pady=40)

    login_rframe = ctk.CTkFrame(login, fg_color="#feefb5", width=300, height=600)
    login_rframe.grid(row=0, column=1, sticky="nsew",padx=(0,40), pady=40)

    ctk.CTkLabel(login_lframe, text="Login", fg_color="#ffe683", text_color="black", font=("Arial", 64, "bold")).place(x=220, y=100)

    # User type radio buttons
    loginch = ctk.StringVar()
    loginch.set("user")
    ctk.CTkRadioButton(
        login_lframe, text="User",
        variable=loginch, value="user",
        fg_color="light blue",
        text_color="black",
        font=("Arial", 24, "bold")
    ).place(x=250, y=250)

    ctk.CTkRadioButton(
        login_lframe, text="Employee",
        variable=loginch, value="employee",
        fg_color="light blue",
        text_color="black",
        font=("Arial", 24, "bold")
    ).place(x=250, y=350)

    ctk.CTkRadioButton(
        login_lframe, text="Admin",
        variable=loginch, value="admin",
        fg_color="light blue",
        text_color="black",
        font=("Arial", 24, "bold")
    ).place(x=250, y=450)

    # Login fields
    ctk.CTkLabel(login_rframe, text="Username:",text_color="black", fg_color="#feefb5", font=("Arial", 34, "bold")).place(x=180, y=250)
    login_uname_entry = ctk.CTkEntry(login_rframe, width=150, fg_color="white", text_color="black")
    login_uname_entry.place(x=420, y=257)

    ctk.CTkLabel(login_rframe, text="Password:",text_color="black", fg_color="#feefb5", font=("Arial", 34, "bold")).place(x=180, y=320)
    login_pwd_entry = ctk.CTkEntry(login_rframe, show="*", width=150, fg_color="white", text_color="black")
    login_pwd_entry.place(x=420, y=327)

    def log_submit():
        username = login_uname_entry.get()
        password = login_pwd_entry.get()
        user_type = loginch.get()
        if not username or not password or not user_type:
            tk.messagebox.showerror("Error", "Please fill all fields!")
            return
        else:
            logged_In = db.login(user_type, username, password)
            if logged_In:
                show_frame(user_screen)
            else:
                tk.messagebox.showerror("Error", "Invalid credentials!")

    ctk.CTkButton(
        login_rframe,
        text="Submit",
        command=log_submit,
        fg_color="#7ed957",
        text_color="black",
        hover_color="#99D980",
        font=("Arial", 16, "bold")
    ).place(x=280, y=400)   

    ctk.CTkButton(
        login,
        text="Back",
        command=lambda: show_frame(main_frame),
        width=100,
        height=40,
        fg_color="tomato",
        text_color="black",
        hover_color="#FC846F",
        bg_color="#ffde59",
        font=("Arial", 16, "bold")
    ).place(x=80,y=80)

    ctk.CTkButton(
        login_rframe,  
        text="user screen",
        command=lambda: show_frame(user_screen),
        width=150,
        height=40,
        fg_color="#7ed957",
        text_color="black",
        hover_color="#99D980",
        font=("Arial", 16, "bold")
    ).place(x=280, y=450)
