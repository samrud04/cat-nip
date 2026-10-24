"""Standalone Cat Nip local-AI chat prototype.

This is intentionally not wired into the live shopping/booking database yet.
First verify Ollama works; then integrate this window into the current app and
add carefully validated Python functions for database actions.
"""

import threading
import customtkinter as ctk
from tkinter import messagebox

MODEL = "qwen3:1.7b"

SYSTEM_PROMPT = (
    "You are Cat Nip's friendly pet supplies and services assistant. "
    "Help users understand how to browse products, orders, pet services, "
    "adoption applications, and playdates. Be concise and ask clarifying "
    "questions when needed. IMPORTANT: You do not have access to the live "
    "Cat Nip database or the ability to place orders/book anything yet. "
    "Never claim an action was completed. Explain that this is the initial "
    "chat prototype when users ask you to perform an action."
)


class CatNipChatbot(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Cat Nip AI Assistant")
        self.geometry("760x650")
        self.minsize(560, 460)
        self.transient(master) if master is not None else None
        self.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        self.busy = False
        self.protocol("WM_DELETE_WINDOW", self.destroy)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            self, text="🐾 Cat Nip AI Assistant",
            font=("Segoe UI", 24, "bold")
        ).grid(row=0, column=0, padx=18, pady=(16, 6), sticky="w")

        self.transcript = ctk.CTkTextbox(self, wrap="word", font=("Segoe UI", 14))
        self.transcript.grid(row=1, column=0, padx=18, pady=8, sticky="nsew")
        self.transcript.configure(state="disabled")
        self._append("Cat Nip", "Hi! 👋 How can I help? You can ask about products, orders, services, adoption, or playdates. This first version can chat, but it cannot make bookings or orders yet.")

        bottom = ctk.CTkFrame(self, fg_color="transparent")
        bottom.grid(row=2, column=0, padx=18, pady=(6, 18), sticky="ew")
        bottom.grid_columnconfigure(0, weight=1)
        self.entry = ctk.CTkEntry(bottom, placeholder_text="Type your message…", height=42)
        self.entry.grid(row=0, column=0, padx=(0, 8), sticky="ew")
        self.entry.bind("<Return>", self._on_enter)
        self.send_button = ctk.CTkButton(bottom, text="Send", width=100, height=42, command=self.send)
        self.send_button.grid(row=0, column=1)
        self.status = ctk.CTkLabel(self, text="Local model: " + MODEL, anchor="w", text_color="gray")
        self.status.grid(row=3, column=0, padx=20, pady=(0, 10), sticky="ew")
        self.entry.focus_set()

    def _on_enter(self, _event):
        self.send()
        return "break"

    def _append(self, speaker, text):
        self.transcript.configure(state="normal")
        self.transcript.insert("end", f"{speaker}:\n{text}\n\n")
        self.transcript.see("end")
        self.transcript.configure(state="disabled")

    def send(self):
        text = self.entry.get().strip()
        if not text or self.busy:
            return
        self.entry.delete(0, "end")
        self._append("You", text)
        self.messages.append({"role": "user", "content": text})
        self.busy = True
        self.send_button.configure(state="disabled")
        self.status.configure(text="Thinking… (the first reply may take a little longer)")
        threading.Thread(target=self._get_reply, daemon=True).start()

    def _get_reply(self):
        try:
            import ollama
            response = ollama.chat(
                model=MODEL,
                messages=self.messages,
                options={"temperature": 0.4},
            )
            reply = response.message.content or "Sorry, I couldn't form a response. Try rephrasing that."
            self.messages.append({"role": "assistant", "content": reply})
            self.after(0, lambda: self._finish(reply, None))
        except Exception as exc:
            self.after(0, lambda error=str(exc): self._finish(None, error))

    def _finish(self, reply, error):
        if not self.winfo_exists():
            return
        if error:
            self._append("Cat Nip", "I couldn't connect to Ollama. Make sure Ollama is installed and running, and that the model exists. In PowerShell run: ollama run " + MODEL + "\n\nDetails: " + error)
            self.status.configure(text="Not connected to Ollama")
        else:
            self._append("Cat Nip", reply)
            self.status.configure(text="Connected locally · " + MODEL)
        self.busy = False
        self.send_button.configure(state="normal")
        self.entry.focus_set()


def open_chatbot(master=None):
    """Open the standalone prototype window."""
    return CatNipChatbot(master)


if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
    app = ctk.CTk()
    app.withdraw()
    window = CatNipChatbot(app)
    app.mainloop()
