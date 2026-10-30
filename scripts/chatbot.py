"""Embedded local Ollama chatbot page for Cat Nip."""
import threading
import customtkinter as ctk

MODEL = "qwen3:1.7b"
SYSTEM_PROMPT = (
    "You are Cat Nip's friendly pet supplies and services assistant. "
    "Help users understand products, shopping carts, orders, pet services, "
    "adoption applications, and playdates. Be concise, friendly, and ask "
    "clarifying questions when needed. This chat is currently informational: "
    "you cannot read or change Cat Nip's live database, place orders, or make "
    "bookings. Never claim an action was completed. Tell the user how to use "
    "the relevant Cat Nip page instead. Do not invent product stock, prices, "
    "booking availability, or user/order details."
)


def create_chatbot_page(parent):
    page = ctk.CTkFrame(parent, fg_color="#FFF6EF", corner_radius=0)
    page.grid_columnconfigure(0, weight=1)
    page.grid_rowconfigure(1, weight=1)

    header = ctk.CTkFrame(page, fg_color="#FA9A85", corner_radius=0)
    header.grid(row=0, column=0, sticky="ew")
    ctk.CTkLabel(header, text="🐾 Cat Nip AI Assistant", font=("Segoe UI", 25, "bold"), text_color="white").pack(anchor="w", padx=20, pady=(14, 2))
    ctk.CTkLabel(header, text="Ask about shopping, services, adoption, or playdates.", font=("Segoe UI", 13), text_color="#49352F").pack(anchor="w", padx=23, pady=(0, 12))

    transcript = ctk.CTkTextbox(page, wrap="word", font=("Segoe UI", 14), corner_radius=12)
    transcript.grid(row=1, column=0, sticky="nsew", padx=18, pady=(14, 8))
    transcript.configure(state="disabled")
    bottom = ctk.CTkFrame(page, fg_color="transparent")
    bottom.grid(row=2, column=0, sticky="ew", padx=18, pady=(4, 8))
    bottom.grid_columnconfigure(0, weight=1)
    entry = ctk.CTkEntry(bottom, placeholder_text="Type your message…", height=42)
    entry.grid(row=0, column=0, sticky="ew", padx=(0, 8))
    send_button = ctk.CTkButton(bottom, text="Send", width=100, height=42, fg_color="#FA9A85", hover_color="#E98270", text_color="#30251f")
    send_button.grid(row=0, column=1)
    status = ctk.CTkLabel(page, text=f"Local model: {MODEL} · runs on this computer", anchor="w", text_color="#6D625D")
    status.grid(row=3, column=0, sticky="ew", padx=20, pady=(0, 10))

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    state = {"busy": False, "alive": True}

    def append(speaker, text):
        if not page.winfo_exists():
            return
        transcript.configure(state="normal")
        transcript.insert("end", f"{speaker}:\n{text}\n\n")
        transcript.see("end")
        transcript.configure(state="disabled")

    append("Cat Nip", "Hi! 👋 How can I help? Ask me about products, order steps, pet services, adoption, or playdates. I can answer questions, but actions must still be completed through the app pages.")

    def finish(reply=None, error=None):
        if not page.winfo_exists():
            return
        if error:
            append("Cat Nip", "I couldn't connect to Ollama. Make sure Ollama is running and the model is installed. In PowerShell, run: ollama run " + MODEL + f"\n\nDetails: {error}")
            status.configure(text="Not connected to Ollama")
        else:
            append("Cat Nip", reply or "Sorry, I couldn't form a response. Try rephrasing that.")
            status.configure(text=f"Connected locally · {MODEL}")
        state["busy"] = False
        send_button.configure(state="normal")
        entry.focus_set()

    def get_reply(history):
        try:
            import ollama
            response = ollama.chat(model=MODEL, messages=history, options={"temperature": 0.4})
            reply = response.message.content or "Sorry, I couldn't form a response. Try rephrasing that."
            messages.append({"role": "assistant", "content": reply})
            page.after(0, lambda result=reply: finish(result, None))
        except Exception as exc:
            page.after(0, lambda error=str(exc): finish(None, error))

    def send(_event=None):
        text = entry.get().strip()
        if not text or state["busy"]:
            return "break"
        entry.delete(0, "end")
        append("You", text)
        messages.append({"role": "user", "content": text})
        state["busy"] = True
        send_button.configure(state="disabled")
        status.configure(text="Thinking… (first reply may take a little longer)")
        threading.Thread(target=get_reply, args=(list(messages),), daemon=True).start()
        return "break"

    send_button.configure(command=send)
    entry.bind("<Return>", send)
    entry.focus_set()
    return page
