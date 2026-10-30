
import customtkinter as ctk
from tkinter import ttk, messagebox
import json
import db

CREAM = "#FFF6EF"
PEACH = "#FA9A85"
INK = "#49352F"
SAGE = "#DDEBDD"


def _maximize_window(win):
    
    def apply():
        try:
            if not win.winfo_exists():
                return
            try:
                win.state("zoomed")
                if str(win.state()) == "zoomed":
                    return
            except Exception:
                pass
            width = win.winfo_screenwidth()
            height = win.winfo_screenheight()
            win.geometry(f"{width}x{height}+0+0")
        except Exception:
            pass
    try:
        win.after(60, apply)
    except Exception:
        apply()


def _show_foreground(win):
    
    def raise_window():
        try:
            if not win.winfo_exists():
                return
            if str(win.state()) == "iconic":
                win.deiconify()
            win.lift()
            # Brief topmost prevents the new Toplevel opening behind the dashboard.
            # It is immediately disabled so it does not stay above other applications.
            win.attributes("-topmost", True)
            win.after(250, lambda: win.attributes("-topmost", False) if win.winfo_exists() else None)
            win.focus_force()
        except Exception:
            pass
    try:
        win.after_idle(raise_window)
        win.after(120, raise_window)
    except Exception:
        raise_window()


def open_playdates_admin(parent):
    
    from datetime import date
    from date_picker import attach_date_picker

    try:
        db.ensure_playdate_tables()
    except Exception as exc:
        messagebox.showerror("Playdates unavailable", f"Could not prepare playdate tables.\n\n{exc}", parent=parent)
        return

    root = parent.winfo_toplevel() if hasattr(parent, "winfo_toplevel") else parent
    win = ctk.CTkToplevel(root)
    win.title("Cat Nip — Manage Playdates")
    win.geometry("1180x800")
    win.minsize(960, 680)
    win.configure(fg_color=CREAM)
    _maximize_window(win)

    ctk.CTkLabel(win, text="🐾 Manage Playdate Events", font=("Arial", 24, "bold"), text_color=INK).pack(anchor="w", padx=22, pady=(16, 3))
    ctk.CTkLabel(win, text="Create and manage events. Set a date, time, location, participant limit and own-pet rules.", text_color=INK, wraplength=1080).pack(anchor="w", padx=22, pady=(0, 12))

    form = ctk.CTkFrame(win, fg_color="white", corner_radius=12)
    form.pack(fill="x", padx=20, pady=(0, 12))
    for col in range(4):
        form.grid_columnconfigure(col, weight=1, uniform="eventform")

    def add_field(label, row, col, placeholder="", *, colspan=1):
        cell = ctk.CTkFrame(form, fg_color="transparent")
        cell.grid(row=row, column=col, columnspan=colspan, sticky="ew", padx=9, pady=7)
        ctk.CTkLabel(cell, text=label, text_color=INK, font=("Arial", 12, "bold")).pack(anchor="w", pady=(0, 3))
        entry = ctk.CTkEntry(cell, placeholder_text=placeholder, height=34)
        entry.pack(fill="x")
        return entry

    title_entry = add_field("Event name *", 0, 0, "Dog social hour")
    pet_cell = ctk.CTkFrame(form, fg_color="transparent")
    pet_cell.grid(row=0, column=1, sticky="ew", padx=9, pady=7)
    ctk.CTkLabel(pet_cell, text="Pet focus", text_color=INK, font=("Arial", 12, "bold")).pack(anchor="w", pady=(0, 3))
    pet_type_box = ctk.CTkComboBox(pet_cell, values=["All", "Cat", "Dog", "Rabbit"], height=34)
    pet_type_box.pack(fill="x"); pet_type_box.set("All")

    date_cell = ctk.CTkFrame(form, fg_color="transparent")
    date_cell.grid(row=0, column=2, sticky="ew", padx=9, pady=7)
    ctk.CTkLabel(date_cell, text="Event date *", text_color=INK, font=("Arial", 12, "bold")).pack(anchor="w", pady=(0, 3))
    date_row = ctk.CTkFrame(date_cell, fg_color="transparent")
    date_row.pack(fill="x")
    date_entry = ctk.CTkEntry(date_row, placeholder_text="YYYY-MM-DD", height=34)
    date_entry.pack(side="left", fill="x", expand=True)
    date_entry.insert(0, date.today().isoformat())
    ctk.CTkButton(date_row, text="📅", width=42, height=34, fg_color=PEACH, hover_color="#E98270", text_color=INK,
                  command=attach_date_picker(date_entry, win, min_date=date.today(), initial_date=date.today())).pack(side="left", padx=(5, 0))

    location_entry = add_field("Location *", 0, 3, "Venue / collection centre")
    start_entry = add_field("Start time * (24-hour HH:MM)", 1, 0, "10:00")
    start_entry.insert(0, "10:00")
    end_entry = add_field("End time * (24-hour HH:MM)", 1, 1, "11:00")
    end_entry.insert(0, "11:00")
    capacity_entry = add_field("Participant capacity *", 1, 2, "10")
    capacity_entry.insert(0, "10")
    allowed_entry = add_field("Permitted own-pet types", 1, 3, "Dog,Cat,Rabbit")
    allowed_entry.insert(0, "Dog,Cat,Rabbit")

    desc_cell = ctk.CTkFrame(form, fg_color="transparent")
    desc_cell.grid(row=2, column=0, columnspan=3, sticky="ew", padx=9, pady=(4, 9))
    ctk.CTkLabel(desc_cell, text="Description / instructions", text_color=INK, font=("Arial", 12, "bold")).pack(anchor="w", pady=(0, 3))
    description_entry = ctk.CTkTextbox(desc_cell, height=72, wrap="word", corner_radius=8)
    description_entry.pack(fill="x")
    description_entry.insert("1.0", "Friendly, supervised playdate. Please follow the venue's instructions.")

    rules_cell = ctk.CTkFrame(form, fg_color="transparent")
    rules_cell.grid(row=2, column=3, sticky="nsew", padx=9, pady=(4, 9))
    ctk.CTkLabel(rules_cell, text="Pet attendance", text_color=INK, font=("Arial", 12, "bold")).pack(anchor="w", pady=(0, 8))
    
    allow_own_pets = {"value": False}
    allow_button = ctk.CTkButton(
        rules_cell,
        text="Own pets: NOT ALLOWED",
        height=34,
        fg_color="#E8E1DC",
        hover_color="#D8CEC7",
        text_color=INK,
        anchor="w",
        command=lambda: toggle_own_pets(),
    )
    allow_button.pack(anchor="w", fill="x", pady=(0, 5))

    def toggle_own_pets():
        allow_own_pets["value"] = not allow_own_pets["value"]
        if allow_own_pets["value"]:
            allow_button.configure(text="Own pets: ALLOWED", fg_color="#B9D9B8", hover_color="#A7CBA6")
        else:
            allow_button.configure(text="Own pets: NOT ALLOWED", fg_color="#E8E1DC", hover_color="#D8CEC7")

    ctk.CTkLabel(rules_cell, text="Capacity counts people, not pets.", text_color="#75675F", wraplength=220, justify="left").pack(anchor="w")

    events_frame = ctk.CTkFrame(win, fg_color="white", corner_radius=12)
    events_frame.pack(fill="both", expand=True, padx=20, pady=(0, 10))
    cols = ("ID", "Event", "Date", "Time", "Location", "Capacity", "Booked", "Own pets", "Status")
    tree = ttk.Treeview(events_frame, columns=cols, show="headings", height=8)
    widths = (48, 170, 100, 112, 230, 70, 65, 78, 85)
    for col, width in zip(cols, widths):
        tree.heading(col, text=col)
        tree.column(col, width=width, minwidth=45, anchor="w")
    ys = ttk.Scrollbar(events_frame, orient="vertical", command=tree.yview)
    xs = ttk.Scrollbar(events_frame, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=ys.set, xscrollcommand=xs.set)
    tree.grid(row=0, column=0, sticky="nsew"); ys.grid(row=0, column=1, sticky="ns"); xs.grid(row=1, column=0, sticky="ew")
    events_frame.grid_rowconfigure(0, weight=1); events_frame.grid_columnconfigure(0, weight=1)

    def load_events():
        for item in tree.get_children(): tree.delete(item)
        try:
            for e in db.get_playdate_events(include_past=True):
                eid, title, desc, focus, day, start, end, location, capacity, allow, allowed, status, booked = e
                tree.insert("", "end", iid=str(eid), values=(eid, title, day, f"{str(start)[:5]}–{str(end)[:5]}", location, capacity, booked, "Yes" if allow else "No", status))
        except Exception as exc:
            messagebox.showerror("Could not load events", str(exc), parent=win)

    def create_event():
        try:
            title = title_entry.get().strip()
            day = date_entry.get().strip()
            location = location_entry.get().strip()
            start = start_entry.get().strip()
            end = end_entry.get().strip()
            capacity_text = capacity_entry.get().strip()
            description = description_entry.get("1.0", "end-1c").strip()
            if not title or not day or not location or not start or not end or not capacity_text:
                raise ValueError("Please fill in all fields marked with *.")
            if not capacity_text.isdigit() or int(capacity_text) < 1:
                raise ValueError("Participant capacity must be a whole number greater than zero.")
            from datetime import date as _date, time as _time
            parsed_day = _date.fromisoformat(day)
            if parsed_day < _date.today():
                raise ValueError("Choose today or a future date for the playdate.")
            _time.fromisoformat(start)
            _time.fromisoformat(end)
            eid = db.create_playdate_event(title, description, pet_type_box.get(), day, start, end,
                location, int(capacity_text), allow_own_pets["value"], allowed_entry.get().strip() or "Dog,Cat,Rabbit")
        except Exception as exc:
            messagebox.showerror("Could not create event", str(exc), parent=win)
            _show_foreground(win)
            return
        messagebox.showinfo("Event created", f"Playdate event #{eid} has been created.", parent=win)
        for widget in (title_entry, location_entry, start_entry, end_entry, capacity_entry, allowed_entry):
            widget.delete(0, "end")
        title_entry.focus_set()
        description_entry.delete("1.0", "end")
        load_events()
        _show_foreground(win)

    def selected_id():
        selection = tree.selection()
        if not selection:
            messagebox.showwarning("Select an event", "Select an event in the list first.", parent=win); return None
        return int(selection[0])

    def set_status(status):
        eid = selected_id()
        if eid is None: return
        try:
            db.update_playdate_event_status(eid, status)
            load_events()
        except Exception as exc:
            messagebox.showerror("Could not update event", str(exc), parent=win)
        _show_foreground(win)

    def show_attendees():
        eid = selected_id()
        if eid is None: return
        try:
            rows = db.get_admin_playdate_bookings(eid)
        except Exception as exc:
            messagebox.showerror("Could not load attendees", str(exc), parent=win); return
        popup = ctk.CTkToplevel(root); popup.title("Playdate attendees"); popup.geometry("760x430"); popup.configure(fg_color=CREAM)
        ctk.CTkLabel(popup, text=f"Attendees for event #{eid}", font=("Arial", 20, "bold"), text_color=INK).pack(anchor="w", padx=16, pady=12)
        box = ctk.CTkScrollableFrame(popup, fg_color="white"); box.pack(fill="both", expand=True, padx=16, pady=(0, 16))
        if not rows:
            ctk.CTkLabel(box, text="No bookings yet.", text_color=INK).pack(anchor="w", padx=10, pady=10)
        for row in rows:
            bid, event_id, name, username, email, day, start, pet_name, pet_type, status, *extra = row
            pets_json = extra[0] if extra else None
            line = f"Booking #{bid} — {username} ({email or 'no email'}) — {status}"
            try:
                pets = json.loads(pets_json) if pets_json else ([{"name": pet_name, "type": pet_type}] if pet_name else [])
            except (TypeError, ValueError):
                pets = ([{"name": pet_name, "type": pet_type}] if pet_name else [])
            if pets: line += "\nBringing: " + ", ".join(f"{p.get('name', 'Pet')} ({p.get('type', 'Unknown')})" for p in pets)
            ctk.CTkLabel(box, text=line, justify="left", anchor="w", wraplength=680, text_color=INK).pack(fill="x", padx=10, pady=8)
        _show_foreground(popup)

    actions = ctk.CTkFrame(win, fg_color="transparent")
    actions.pack(fill="x", padx=20, pady=(0, 14))
    ctk.CTkButton(actions, text="＋ Create Event", command=create_event, fg_color=PEACH, hover_color="#E98270", text_color=INK).pack(side="left", padx=(0, 6))
    ctk.CTkButton(actions, text="View Attendees", command=show_attendees).pack(side="left", padx=6)
    ctk.CTkButton(actions, text="Reopen Event", command=lambda: set_status("Open")).pack(side="left", padx=6)
    ctk.CTkButton(actions, text="Cancel Event", command=lambda: set_status("Cancelled"), fg_color="#B95353", hover_color="#963D3D").pack(side="left", padx=6)
    ctk.CTkButton(actions, text="Mark Completed", command=lambda: set_status("Completed")).pack(side="left", padx=6)
    ctk.CTkButton(actions, text="Refresh", command=load_events).pack(side="left", padx=6)
    ctk.CTkButton(actions, text="Close", command=win.destroy).pack(side="right")
    win.protocol("WM_DELETE_WINDOW", win.destroy)
    load_events()
    _show_foreground(win)
    return win

def open_playdates_user(parent, user_id, embedded=False):
    if not user_id:
        messagebox.showerror("Sign in required", "Please sign in before booking a playdate.", parent=parent); return
    try:
        db.ensure_playdate_tables()
    except Exception as exc:
        messagebox.showerror("Playdates unavailable", str(exc), parent=parent); return
    if embedded:
        win = ctk.CTkFrame(parent, fg_color=CREAM, corner_radius=0)
        win.pack(fill="both", expand=True)
    else:
        root = parent.winfo_toplevel() if hasattr(parent, "winfo_toplevel") else parent
        win = ctk.CTkToplevel(root); win.title("Cat Nip — Playdates"); win.geometry("1000x720"); win.minsize(800, 600); win.configure(fg_color=CREAM)
        _maximize_window(win)
    ctk.CTkLabel(win, text="🐾 Upcoming Playdates", font=("Arial", 25, "bold"), text_color=INK).pack(anchor="w", padx=20, pady=(18, 3))
    ctk.CTkLabel(win, text="Choose an event to book a place. You can cancel your booking before the event starts.", text_color=INK).pack(anchor="w", padx=20, pady=(0, 12))
    body = ctk.CTkFrame(win, fg_color="transparent"); body.pack(fill="both", expand=True, padx=20, pady=(0, 10))
    body.grid_columnconfigure(0, weight=3); body.grid_columnconfigure(1, weight=2); body.grid_rowconfigure(0, weight=1)
    event_frame = ctk.CTkScrollableFrame(body, fg_color="white", corner_radius=12); event_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
    detail = ctk.CTkScrollableFrame(body, fg_color=SAGE, corner_radius=12); detail.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
    chosen = {"event": None}

    def render_detail(event):
        chosen["event"] = event
        for child in detail.winfo_children(): child.destroy()
        if not event:
            ctk.CTkLabel(detail, text="Select an event to see details.", text_color=INK, wraplength=300).pack(padx=15, pady=30); return
        eid, title, desc, focus, day, start, end, location, capacity, allow, allowed, status, booked = event
        ctk.CTkLabel(detail, text=title, font=("Arial", 20, "bold"), text_color=INK, wraplength=300).pack(anchor="w", padx=14, pady=(14, 5))
        info = f"📅 {day}\n🕒 {str(start)[:5]}–{str(end)[:5]}\n📍 {location}\n🐾 Pet focus: {focus}\n👥 Places remaining: {max(0, int(capacity)-int(booked))} / {capacity}"
        if desc: info += f"\n\n{desc}"
        info += "\n\nOwn pets: " + (f"Allowed ({allowed})" if allow else "Not permitted for this event")
        ctk.CTkLabel(detail, text=info, text_color=INK, justify="left", anchor="w", wraplength=300).pack(fill="x", padx=14, pady=6)
        pets_area = ctk.CTkFrame(detail, fg_color="transparent")
        pet_fields = []
        allowed_types = [x.strip() for x in (allowed or "Dog,Cat,Rabbit").split(",") if x.strip()] or ["Dog", "Cat", "Rabbit"]
        pet_count_box = None
        if allow:
            ctk.CTkLabel(detail, text="Bringing your own pets? (optional, up to 3)", text_color=INK, font=("Arial", 12, "bold")).pack(anchor="w", padx=14, pady=(10, 3))
            count_row = ctk.CTkFrame(detail, fg_color="transparent")
            count_row.pack(fill="x", padx=14, pady=(0, 4))
            ctk.CTkLabel(count_row, text="Number of pets", text_color=INK).pack(side="left", padx=(0, 8))
            pet_count_box = ctk.CTkComboBox(count_row, values=["0", "1", "2", "3"], width=90, state="readonly")
            pet_count_box.pack(side="left"); pet_count_box.set("0")
            pets_area.pack(fill="x", padx=14, pady=2)

            def build_pet_fields(_value=None):
                for child in pets_area.winfo_children(): child.destroy()
                pet_fields.clear()
                try: count = int(pet_count_box.get())
                except ValueError: count = 0
                for idx in range(count):
                    row = ctk.CTkFrame(pets_area, fg_color=CREAM, corner_radius=8)
                    row.pack(fill="x", pady=4)
                    ctk.CTkLabel(row, text=f"Pet {idx + 1}", text_color=INK, font=("Arial", 11, "bold")).pack(anchor="w", padx=8, pady=(5, 0))
                    name_entry = ctk.CTkEntry(row, placeholder_text=f"Pet {idx + 1} name", height=32)
                    name_entry.pack(fill="x", padx=8, pady=4)
                    type_box = ctk.CTkComboBox(row, values=allowed_types, height=32, state="readonly")
                    type_box.pack(fill="x", padx=8, pady=(0, 7)); type_box.set(allowed_types[0])
                    pet_fields.append((name_entry, type_box))
            pet_count_box.configure(command=build_pet_fields)

        def book():
            pets = []
            if allow:
                for idx, (name_entry, type_box) in enumerate(pet_fields, start=1):
                    name = name_entry.get().strip()
                    ptype = type_box.get().strip()
                    if not name:
                        messagebox.showwarning("Pet name needed", f"Enter a name for Pet {idx}, or change the pet count.", parent=win)
                        return
                    pets.append({"name": name, "type": ptype})
            try: result = db.book_playdate(eid, user_id, pets=pets)
            except Exception as exc:
                messagebox.showerror("Booking failed", str(exc), parent=win); return
            messages = {"confirmed": ("Booking confirmed", "You're booked in! The event details are shown in My Playdates."),
                        "closed": ("Event unavailable", "This event is no longer open for bookings."),
                        "started": ("Booking closed", "This event has already started."),
                        "exists": ("Already booked", "You already have a confirmed booking for this event."),
                        "full": ("Fully booked", "Sorry, this playdate has reached its participant capacity."),
                        "pets_not_allowed": ("Pets not allowed", "This event does not allow attendees to bring their own pets."),
                        "pet_type_not_allowed": ("Pet type not allowed", "One or more pets have a type not permitted for this event.")}
            title_msg, body_msg = messages.get(result, ("Booking result", str(result)))
            messagebox.showinfo(title_msg, body_msg, parent=win); load_events(); load_bookings()
        ctk.CTkButton(detail, text="Book Now", command=book, fg_color=PEACH, hover_color="#E98270", text_color=INK).pack(fill="x", padx=14, pady=(12, 16))

    def load_events():
        for child in event_frame.winfo_children(): child.destroy()
        try: events = db.get_playdate_events()
        except Exception as exc:
            ctk.CTkLabel(event_frame, text=f"Could not load events: {exc}", text_color="#9B3D36", wraplength=420).pack(padx=12, pady=15); return
        if not events:
            ctk.CTkLabel(event_frame, text="No upcoming playdates are open for booking right now.", text_color=INK, wraplength=400).pack(padx=15, pady=25); render_detail(None); return
        for event in events:
            eid, title, desc, focus, day, start, end, location, capacity, allow, allowed, status, booked = event
            card = ctk.CTkFrame(event_frame, fg_color=CREAM, corner_radius=10, border_width=1, border_color="#F0D8CB")
            card.pack(fill="x", padx=6, pady=6)
            ctk.CTkLabel(card, text=title, font=("Arial", 16, "bold"), text_color=INK).pack(anchor="w", padx=12, pady=(9, 2))
            ctk.CTkLabel(card, text=f"{day}  •  {str(start)[:5]}–{str(end)[:5]}  •  {max(0, int(capacity)-int(booked))} spots left", text_color=INK).pack(anchor="w", padx=12, pady=(0, 9))
            for widget in (card, *card.winfo_children()): widget.bind("<Button-1>", lambda _e, item=event: render_detail(item))
        if chosen["event"] and not any(e[0] == chosen["event"][0] for e in events): render_detail(None)

    bookings_frame = ctk.CTkScrollableFrame(win, fg_color="white", corner_radius=12, height=170)
    bookings_frame.pack(fill="x", padx=20, pady=(0, 18))
    ctk.CTkLabel(bookings_frame, text="📋 My Playdates", font=("Arial", 16, "bold"), text_color=INK).pack(anchor="w", padx=10, pady=(8, 3))

    def load_bookings():
        for child in bookings_frame.winfo_children():
            if child.winfo_class() != "CTkLabel" or child.cget("text") != "📋 My Playdates": child.destroy()
        try: rows = db.get_user_playdate_bookings(user_id)
        except Exception as exc:
            ctk.CTkLabel(bookings_frame, text=f"Could not load bookings: {exc}", text_color="#9B3D36", wraplength=850).pack(anchor="w", padx=10, pady=6); return
        if not rows:
            ctk.CTkLabel(bookings_frame, text="You have no playdate bookings yet.", text_color=INK).pack(anchor="w", padx=10, pady=6); return
        for row in rows:
            bid, eid, title, day, start, end, location, pet_name, pet_type, status, event_status, *extra = row
            text = f"{title} — {day}, {str(start)[:5]}–{str(end)[:5]} | {location} | {status}"
            pets_json = extra[0] if extra else None
            try:
                pets = json.loads(pets_json) if pets_json else ([{"name": pet_name, "type": pet_type}] if pet_name else [])
            except (TypeError, ValueError):
                pets = ([{"name": pet_name, "type": pet_type}] if pet_name else [])
            if pets: text += " | Bringing: " + ", ".join(f"{p.get('name', 'Pet')} ({p.get('type', 'Unknown')})" for p in pets)
            line = ctk.CTkFrame(bookings_frame, fg_color=CREAM, corner_radius=8); line.pack(fill="x", padx=6, pady=4)
            ctk.CTkLabel(line, text=text, text_color=INK, wraplength=700, justify="left", anchor="w").pack(side="left", fill="x", expand=True, padx=8, pady=6)
            if status == "Confirmed" and event_status != "Cancelled":
                ctk.CTkButton(line, text="Cancel booking", width=110, command=lambda booking_id=bid: cancel(booking_id)).pack(side="right", padx=8, pady=5)

    def cancel(booking_id):
        if not messagebox.askyesno("Cancel booking", "Cancel this playdate booking? The slot will become available again.", parent=win): return
        if db.cancel_playdate_booking(booking_id, user_id): messagebox.showinfo("Booking cancelled", "Your booking has been cancelled.", parent=win)
        else: messagebox.showwarning("Cannot cancel", "Bookings can only be cancelled before the event starts.", parent=win)
        load_events(); load_bookings()

    if not embedded:
        win.protocol("WM_DELETE_WINDOW", win.destroy)
    load_events(); load_bookings()
    if not embedded:
        _show_foreground(win)
    return win
