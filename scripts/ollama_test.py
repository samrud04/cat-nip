"""Quick connectivity test for Cat Nip's local Ollama setup.

Run from the project root after installing the `ollama` Python package and
pulling the configured model:
    python scripts/ollama_test.py
"""

import sys

MODEL = "qwen3:1.7b"


def main():
    try:
        import ollama
    except ImportError:
        print("Missing Python package. Run: python -m pip install ollama")
        return 1

    try:
        ollama.show(MODEL)
    except Exception as exc:
        print("Could not reach the model through Ollama.")
        print("1. Open/install Ollama for Windows.")
        print(f"2. In PowerShell, run: ollama run {MODEL}")
        print("3. Keep Ollama installed/running, then run this test again.")
        print(f"Details: {exc}")
        return 1

    try:
        response = ollama.chat(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are Cat Nip's friendly pet-shop assistant. Keep answers concise."},
                {"role": "user", "content": "Say hello and tell me one thing you can help with."},
            ],
            options={"temperature": 0.4},
        )
        print("Ollama connection successful!\n")
        print(response.message.content or "(The model returned an empty response.)")
        return 0
    except Exception as exc:
        print(f"The model was found but the chat request failed: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
