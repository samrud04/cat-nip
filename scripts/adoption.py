"""Shelter-style pet adoption UI for Cat Nip (demonstration listings)."""
import customtkinter as ctk
from tkinter import ttk, messagebox
import db

CREAM = "#FFF6EF"
PEACH = "#FA9A85"
INK = "#49352F"
SAGE = "#DDEBDD"

# Keep pet icons in the UI, but store ASCII tokens in MySQL so older
# database/table character sets do not reject 4-byte emoji characters.
PET_ICONS = {"cat": "🐱", "dog": "🐶", "rabbit": "🐰", "paw": "🐾"}

def display_pet_icon(value):
    return PET_ICONS.get(str(value).lower(), "🐾")


def open_adoption_window(parent, user_id, embedded=False):
    if not user_id:
        messagebox.showerror("Sign in required", "Please sign in before applying to adopt a pet.")
        return
    try:
        db.ensure_adoption_tables()
    except Exception as exc:
        messagebox.showerror("Adoption unavailable", f"Could not prepare the adoption database.\n\n{exc}")
        return

    if embedded:
        win = ctk.CTkFrame(parent, fg_color=CREAM, corner_radius=0)
        win.pack(fill="both", expand=True)
    else:
        win = ctk.CTkToplevel(parent)
        win.title("Cat Nip — Adopt a Pet")
        win.geometry("1040x760")
        win.minsize(850, 620)
        win.configure(fg_color=CREAM)
        win.transient(parent.winfo_toplevel())

    header = ctk.CTkFrame(win, fg_color=PEACH, corner_radius=0)
    header.pack(fill="x")
    ctk.CTkLabel(header, text="🐾  Find Your New Best Friend", font=("Arial", 26, "bold"), text_color="white").pack(anchor="w", padx=24, pady=(18, 2))
    ctk.CTkLabel(header, text="Choose a pet, tell us a little about your home, and submit an adoption application.", font=("Arial", 13), text_color=INK).pack(anchor="w", padx=27, pady=(0, 16))

    toolbar = ctk.CTkFrame(win, fg_color="transparent")
    toolbar.pack(fill="x", padx=22, pady=(15, 5))
    ctk.CTkLabel(toolbar, text="Available pets", font=("Arial", 20, "bold"), text_color=INK).pack(side="left")
    species_filter = ctk.CTkComboBox(toolbar, values=["All", "Cat", "Dog", "Rabbit"], width=140, command=lambda _v: refresh_pets())
    species_filter.set("All")
    species_filter.pack(side="right")
    ctk.CTkLabel(toolbar, text="Filter:", text_color=INK).pack(side="right", padx=8)

    body = ctk.CTkFrame(win, fg_color="transparent")
    body.pack(fill="both", expand=True, padx=22, pady=10)
    body.grid_columnconfigure(0, weight=3)
    body.grid_columnconfigure(1, weight=2)
    body.grid_rowconfigure(0, weight=1)

    listing_panel = ctk.CTkScrollableFrame(body, fg_color="white", corner_radius=14)
    listing_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
    detail_panel = ctk.CTkFrame(body, fg_color=SAGE, corner_radius=14)
    detail_panel.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

    selected = {"pet": None}
    detail_widgets = []

    def set_detail(pet):
        selected["pet"] = pet
        for widget in detail_panel.winfo_children():
            widget.destroy()
        if not pet:
            ctk.CTkLabel(detail_panel, text="💛", font=("Arial", 54)).pack(pady=(55, 10))
            ctk.CTkLabel(detail_panel, text="Choose a pet", font=("Arial", 22, "bold"), text_color=INK).pack(pady=5)
            ctk.CTkLabel(detail_panel, text="Select a profile to learn more\nand apply for adoption.", text_color=INK, justify="center").pack(pady=8)
            return
        pet_id, name, species, age, gender, description, emoji, status = pet
        ctk.CTkLabel(detail_panel, text=display_pet_icon(emoji), font=("Arial", 66)).pack(pady=(22, 4))
        ctk.CTkLabel(detail_panel, text=name, font=("Arial", 25, "bold"), text_color=INK).pack(pady=2)
        ctk.CTkLabel(detail_panel, text=f"{species}  •  {age}  •  {gender}", font=("Arial", 13, "bold"), text_color=INK).pack(pady=4)
        ctk.CTkLabel(detail_panel, text=description, wraplength=290, justify="center", text_color=INK).pack(padx=18, pady=(8, 18))
        ctk.CTkLabel(detail_panel, text="Why would you like to adopt?", font=("Arial", 14, "bold"), text_color=INK).pack(anchor="w", padx=18, pady=(0, 6))
        reason_box = ctk.CTkTextbox(detail_panel, height=115, corner_radius=10)
        reason_box.pack(fill="x", padx=18, pady=(0, 12))
        reason_box.insert("1.0", "I can provide a safe, caring home because…")
        def submit():
            reason = reason_box.get("1.0", "end").strip()
            if not reason or reason == "I can provide a safe, caring home because…" or len(reason) < 10:
                messagebox.showwarning("A little more detail", "Please write a short reason (at least 10 characters).", parent=win)
                return
            try:
                result = db.submit_adoption_application(user_id, pet_id, reason)
            except Exception as exc:
                messagebox.showerror("Could not submit", str(exc), parent=win)
                return
            if result == "submitted":
                messagebox.showinfo("Application submitted", f"Your application for {name} is now Pending. The shelter admin will review it.", parent=win)
                refresh_pets()
                refresh_applications()
            elif result == "exists":
                messagebox.showinfo("Already applied", "You already have an application for this pet.", parent=win)
            else:
                messagebox.showwarning("No longer available", "This pet is no longer available for adoption.", parent=win)
                refresh_pets()
        ctk.CTkButton(detail_panel, text="❤️ Apply for Adoption", command=submit, fg_color=PEACH, hover_color="#E98270", text_color=INK, height=40).pack(fill="x", padx=18, pady=(0, 18))

    def refresh_pets():
        for widget in listing_panel.winfo_children():
            widget.destroy()
        try:
            pets = db.get_available_pets(species_filter.get())
        except Exception as exc:
            ctk.CTkLabel(listing_panel, text=f"Could not load pets: {exc}", text_color="#9B3D36", wraplength=420).pack(padx=15, pady=20)
            return
        if not pets:
            ctk.CTkLabel(listing_panel, text="No pets in this category right now.\nPlease check back later! 🐾", text_color=INK, justify="center").pack(padx=20, pady=40)
            set_detail(None)
            return
        for pet in pets:
            pet_id, name, species, age, gender, description, emoji, status = pet
            card = ctk.CTkFrame(listing_panel, fg_color=CREAM, corner_radius=12, border_width=1, border_color="#F0D8CB")
            card.pack(fill="x", padx=7, pady=7)
            ctk.CTkLabel(card, text=display_pet_icon(emoji), font=("Arial", 36), width=60).pack(side="left", padx=(12, 5), pady=10)
            text_area = ctk.CTkFrame(card, fg_color="transparent")
            text_area.pack(side="left", fill="x", expand=True, padx=4, pady=10)
            ctk.CTkLabel(text_area, text=name, font=("Arial", 17, "bold"), text_color=INK).pack(anchor="w")
            ctk.CTkLabel(text_area, text=f"{species} • {age} • {gender}", font=("Arial", 12), text_color=INK).pack(anchor="w")
            ctk.CTkLabel(card, text="View →", text_color=INK, font=("Arial", 12, "bold")).pack(side="right", padx=14)
            for widget in (card, text_area):
                widget.bind("<Button-1>", lambda _e, item=pet: set_detail(item))
            for child in text_area.winfo_children():
                child.bind("<Button-1>", lambda _e, item=pet: set_detail(item))
            card.bind("<Button-1>", lambda _e, item=pet: set_detail(item))
        if selected["pet"] and not any(p[0] == selected["pet"][0] for p in pets):
            set_detail(None)

    app_frame = ctk.CTkScrollableFrame(win, fg_color="white", corner_radius=12, height=150)
    app_frame.pack(fill="x", padx=22, pady=(0, 18))
    ctk.CTkLabel(app_frame, text="📋 My Adoption Applications", font=("Arial", 16, "bold"), text_color=INK).pack(anchor="w", padx=14, pady=(10, 4))
    app_text = ctk.CTkLabel(app_frame, text="No applications yet.", text_color=INK, justify="left", anchor="w", wraplength=950)
    app_text.pack(fill="x", padx=14, pady=(0, 12))

    def refresh_applications():
        try:
            apps = db.get_user_adoption_applications(user_id)
            if not apps:
                label = "No applications yet. Choose a pet above to get started!"
            else:
                sections = []
                for app in apps:
                    app_id, pet_name, species, status, created, reason, address = app
                    section = f"Application #{app_id}  •  {pet_name} ({species})\nStatus: {status}"
                    if status == "Approved":
                        section += (
                            f"\n\n🎉 ADOPTION APPROVAL PASS\n"
                            f"Approved pet: {pet_name} ({species})\n"
                            f"Pass / application ID: ADP-{app_id:04d}\n"
                            f"Collection address (fictional demo location):\n{address or 'Address is being prepared; refresh shortly.'}\n"
                            "Instructions: Show this pass and your application ID to the centre staff. "
                            "This is a school-project simulation; do not travel to this demo address."
                        )
                    sections.append(section)
                label = "\n\n────────────────────────\n\n".join(sections)
            app_text.configure(text=label)
        except Exception:
            app_text.configure(text="Application status is temporarily unavailable.")

    refresh_pets()
    refresh_applications()
    return win


def open_adoption_admin(parent):
    try:
        db.ensure_adoption_tables()
    except Exception as exc:
        messagebox.showerror("Adoption unavailable", f"Could not prepare the adoption database.\n\n{exc}")
        return
    # Use the actual application window as the parent, not the embedded admin frame.
    # This keeps the adoption manager in front instead of appearing behind the admin page.
    root = parent.winfo_toplevel() if hasattr(parent, "winfo_toplevel") else parent
    win = ctk.CTkToplevel(root)
    win.title("Cat Nip — Adoption Applications")
    win.geometry("1100x620")
    win.minsize(900, 520)
    win.configure(fg_color=CREAM)
    try:
        win.transient(root)
    except Exception:
        pass
    ctk.CTkLabel(win, text="🐾 Adoption Application Review", font=("Arial", 24, "bold"), text_color=INK).pack(anchor="w", padx=20, pady=(18, 8))
    ctk.CTkLabel(win, text="Review each request before approving. Approving one application marks that pet as Adopted.", text_color=INK).pack(anchor="w", padx=20, pady=(0, 12))
    table_frame = ctk.CTkFrame(win, fg_color="white")
    table_frame.pack(fill="both", expand=True, padx=20, pady=(0, 12))
    cols = ("ID", "Pet", "Species", "Username", "Email", "Phone", "Reason", "Status", "Submitted")
    tree = ttk.Treeview(table_frame, columns=cols, show="headings", height=14)
    # Long reasons stay in the database and are opened in a dedicated scrollable viewer.
    widths = (55, 90, 80, 100, 150, 95, 135, 90, 140)
    reasons_by_id = {}
    for col, width in zip(cols, widths):
        tree.heading(col, text=col)
        tree.column(col, width=width, minwidth=50, anchor="w")
    yscroll = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    xscroll = ttk.Scrollbar(table_frame, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=yscroll.set, xscrollcommand=xscroll.set)
    tree.grid(row=0, column=0, sticky="nsew")
    yscroll.grid(row=0, column=1, sticky="ns")
    xscroll.grid(row=1, column=0, sticky="ew")
    table_frame.grid_rowconfigure(0, weight=1); table_frame.grid_columnconfigure(0, weight=1)

    def load():
        for row in tree.get_children(): tree.delete(row)
        reasons_by_id.clear()
        try:
            for app in db.get_all_adoption_applications():
                app_id, pet, species, username, email, phone, reason, status, created, pet_id, user_id = app
                reasons_by_id[int(app_id)] = reason or "No reason provided."
                tree.insert("", "end", iid=str(app_id), values=(app_id, pet, species, username, email or "—", phone or "—", "Select row → View Reason", status, created))
        except Exception as exc:
            messagebox.showerror("Could not load applications", str(exc), parent=win)

    def view_reason():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Select an application", "Choose an application in the table first.", parent=win)
            return
        app_id = int(selected[0])
        values = tree.item(selected[0], "values")
        pet_name = values[1] if len(values) > 1 else "Pet"
        username = values[3] if len(values) > 3 else "User"
        popup = ctk.CTkToplevel(win)
        popup.title(f"Adoption Reason — Application #{app_id}")
        popup.geometry("680x480")
        popup.minsize(500, 350)
        popup.configure(fg_color=CREAM)
        ctk.CTkLabel(popup, text=f"Application #{app_id} — {pet_name}", font=("Arial", 21, "bold"), text_color=INK).pack(anchor="w", padx=18, pady=(16, 3))
        ctk.CTkLabel(popup, text=f"Applicant: {username}", text_color=INK).pack(anchor="w", padx=18, pady=(0, 10))
        reason_box = ctk.CTkTextbox(popup, wrap="word", font=("Arial", 14), corner_radius=10)
        reason_box.pack(fill="both", expand=True, padx=18, pady=(0, 12))
        reason_box.insert("1.0", reasons_by_id.get(app_id, "No reason provided."))
        reason_box.configure(state="disabled")
        ctk.CTkButton(popup, text="Close", command=popup.destroy).pack(anchor="e", padx=18, pady=(0, 14))
        try:
            popup.transient(win); popup.lift(); popup.focus_force()
        except Exception:
            pass

    actions = ctk.CTkFrame(win, fg_color="transparent")
    actions.pack(fill="x", padx=20, pady=(0, 18))
    status_box = ctk.CTkComboBox(actions, values=["Pending", "Approved", "Rejected"], width=160)
    status_box.set("Approved")
    status_box.pack(side="left", padx=(0, 8))

    def update():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Select an application", "Choose an application in the table first.", parent=win)
            return
        try:
            ok = db.update_adoption_application(int(selected[0]), status_box.get())
        except Exception as exc:
            messagebox.showerror("Update failed", str(exc), parent=win)
            return
        if not ok:
            messagebox.showwarning("Pet unavailable", "This pet may already have been adopted. Refresh the list and review the application.", parent=win)
        else:
            messagebox.showinfo("Updated", f"Application marked {status_box.get()}.", parent=win)
        load()

    ctk.CTkButton(actions, text="View Full Reason", command=view_reason, fg_color="#6C8D70", hover_color="#55755A").pack(side="left", padx=(0, 5))
    ctk.CTkButton(actions, text="Update Selected", command=update, fg_color=PEACH, hover_color="#E98270", text_color=INK).pack(side="left", padx=5)
    ctk.CTkButton(actions, text="Refresh", command=load).pack(side="left", padx=5)
    ctk.CTkButton(actions, text="Close", command=win.destroy).pack(side="right")
    load()
    # Match the other admin managers: keep this window active and in the foreground.
    try:
        win.grab_set()
    except Exception:
        pass
    win.lift()
    win.focus_force()
    win.after(120, lambda: (win.lift(), win.focus_force()) if win.winfo_exists() else None)
    return win
