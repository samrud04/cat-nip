

import calendar
from datetime import date
import customtkinter as ctk


PEACH = "#F4B183"
PEACH_DARK = "#D98958"
TEXT = "#30251F"
MUTED = "#75675F"


def attach_date_picker(entry, parent, *, date_format="%Y-%m-%d", min_date=None,
                       max_date=None, initial_date=None):

    today = date.today()
    min_date = min_date or date(1000, 1, 1)
    max_date = max_date or date(9999, 12, 31)
    initial_date = initial_date or today

    def open_calendar():
        try:
            typed = entry.get().strip()
            current = date.fromisoformat(typed) if date_format == "%Y-%m-%d" else None
            if date_format != "%Y-%m-%d" and typed:
                from datetime import datetime
                current = datetime.strptime(typed, date_format).date()
        except (ValueError, TypeError):
            current = initial_date
        if current is None:
            current = initial_date
        current = max(min_date, min(max_date, current))

        win = ctk.CTkToplevel(parent)
        win.title("Select a date")
        win.resizable(False, False)
        win.configure(fg_color="#FFF8F2")
        try:
            win.transient(parent.winfo_toplevel())
        except Exception:
            pass
        win.grab_set()

        def close_calendar():
            try:
                if win.grab_current() is not None:
                    win.grab_release()
            except Exception:
                pass
            try:
                win.destroy()
            except Exception:
                pass

        win.protocol("WM_DELETE_WINDOW", close_calendar)

        year_var = ctk.StringVar(value=str(current.year))
        month_var = {"value": current.month}

        header = ctk.CTkFrame(win, fg_color="#FFF8F2")
        header.pack(fill="x", padx=14, pady=(14, 5))
        title = ctk.CTkLabel(header, text="", font=("Arial", 17, "bold"), text_color=TEXT)
        title.pack(side="left", padx=(4, 10))

        year_box = ctk.CTkEntry(header, width=72, textvariable=year_var, justify="center")
        year_box.pack(side="left", padx=(0, 5))

        grid_frame = ctk.CTkFrame(win, fg_color="#FFF8F2")
        grid_frame.pack(padx=14, pady=5)

        def change_month(delta):
            month = month_var["value"] + delta
            year = int(year_var.get())
            if month < 1:
                month, year = 12, year - 1
            elif month > 12:
                month, year = 1, year + 1
            if 1000 <= year <= 9999:
                year_var.set(str(year))
                month_var["value"] = month
                render_days()

        ctk.CTkButton(header, text="‹", width=30, command=lambda: change_month(-1),
                      fg_color=PEACH, hover_color=PEACH_DARK, text_color=TEXT).pack(side="left", padx=(0, 4))
        ctk.CTkButton(header, text="›", width=30, command=lambda: change_month(1),
                      fg_color=PEACH, hover_color=PEACH_DARK, text_color=TEXT).pack(side="left")

        def jump_year(_event=None):
            try:
                year = int(year_var.get())
                if not 1000 <= year <= 9999:
                    raise ValueError
                year_var.set(str(year))
                render_days()
            except ValueError:
                year_var.set(str(current.year))

        year_box.bind("<Return>", jump_year)
        ctk.CTkButton(header, text="Go", width=42, command=jump_year,
                      fg_color=PEACH, hover_color=PEACH_DARK, text_color=TEXT).pack(side="left", padx=(5, 0))

        def choose(day):
            chosen = date(int(year_var.get()), month_var["value"], day)
            try:
                entry.delete(0, "end")
                entry.insert(0, chosen.strftime(date_format))
            finally:
                close_calendar()

        def render_days():
            for widget in grid_frame.winfo_children():
                widget.destroy()
            year = int(year_var.get())
            month = month_var["value"]
            title.configure(text=f"{calendar.month_name[month]}")
            for col, name in enumerate(("Mo", "Tu", "We", "Th", "Fr", "Sa", "Su")):
                ctk.CTkLabel(grid_frame, text=name, width=38, height=28,
                             text_color=MUTED, font=("Arial", 11, "bold")).grid(row=0, column=col, padx=2, pady=2)
            weeks = calendar.monthcalendar(year, month)
            for row, week in enumerate(weeks, start=1):
                for col, day in enumerate(week):
                    if not day:
                        ctk.CTkLabel(grid_frame, text="", width=38, height=32).grid(row=row, column=col, padx=2, pady=2)
                        continue
                    picked = date(year, month, day)
                    allowed = min_date <= picked <= max_date
                    is_selected = picked == current
                    ctk.CTkButton(
                        grid_frame, text=str(day), width=38, height=32, corner_radius=8,
                        fg_color=(PEACH_DARK if is_selected else (PEACH if allowed else "#E8E1DC")),
                        hover_color=PEACH_DARK, text_color=(TEXT if allowed else "#A9A09A"),
                        state=("normal" if allowed else "disabled"),
                        command=lambda d=day: choose(d)
                    ).grid(row=row, column=col, padx=2, pady=2)

        render_days()
        footer = ctk.CTkFrame(win, fg_color="transparent")
        footer.pack(fill="x", padx=14, pady=(5, 14))
        ctk.CTkLabel(footer, text=f"Allowed: {min_date:%d %b %Y} – {max_date:%d %b %Y}",
                     text_color=MUTED, font=("Arial", 10)).pack(side="left")
        ctk.CTkButton(footer, text="Today", width=65, fg_color=PEACH,
                      hover_color=PEACH_DARK, text_color=TEXT,
                      state=("normal" if min_date <= today <= max_date else "disabled"),
                      command=lambda: choose(today.day) if today.year == int(year_var.get()) and today.month == month_var["value"] else set_today()).pack(side="right")

        def set_today():
            if min_date <= today <= max_date:
                year_var.set(str(today.year))
                month_var["value"] = today.month
                render_days()
                choose(today.day)

    return open_calendar
