import random
import string
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import pyperclip
import json
import os

# File to save passwords
PASSWORD_FILE = "saved_passwords.json"

# Load saved passwords
def load_passwords():
    if os.path.exists(PASSWORD_FILE):
        with open(PASSWORD_FILE, 'r') as f:
            return json.load(f)
    return {}

# Save passwords
def save_passwords(data):
    with open(PASSWORD_FILE, 'w') as f:
        json.dump(data, f, indent=4)

class PasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Ultimate Password Generator")
        self.root.geometry("750x650")
        self.root.configure(bg="#121212")
        self.root.resizable(False, False)

        self.saved_passwords = load_passwords()
        self.create_widgets()

    def create_widgets(self):
        # Title
        title = tk.Label(self.root, text="Secure Password Generator", font=("Arial", 24, "bold"), fg="#00FF88", bg="#121212")
        title.pack(pady=15)

        # Length Frame
        len_frame = tk.Frame(self.root, bg="#121212")
        len_frame.pack(pady=10)
        tk.Label(len_frame, text="Password Length:", font=("Arial", 12), fg="white", bg="#121212").pack(side=tk.LEFT, padx=10)
        self.length_var = tk.IntVar(value=16)
        length_slider = ttk.Scale(len_frame, from_=8, to=128, orient=tk.HORIZONTAL, variable=self.length_var, length=300)
        length_slider.pack(side=tk.LEFT, padx=10)
        self.length_label = tk.Label(len_frame, text="16", font=("Arial", 12, "bold"), fg="#00FF88", bg="#121212")
        self.length_label.pack(side=tk.LEFT, padx=10)
        length_slider.config(command=self.update_length)

        # Checkboxes
        check_frame = tk.LabelFrame(self.root, text=" Include Characters ", font=("Arial", 12, "bold"), fg="#00D4FF", bg="#1E1E1E", padx=20, pady=10)
        check_frame.pack(pady=15, fill=tk.X, padx=40)

        self.upper = tk.BooleanVar(value=True)
        self.lower = tk.BooleanVar(value=True)
        self.digits = tk.BooleanVar(value=True)
        self.symbols = tk.BooleanVar(value=True)
        self.exclude_similar = tk.BooleanVar(value=True)

        tk.Checkbutton(check_frame, text="A-Z Uppercase", variable=self.upper, fg="white", bg="#1E1E1E", selectcolor="#333").grid(row=0, column=0, sticky=tk.W, pady=5)
        tk.Checkbutton(check_frame, text="a-z Lowercase", variable=self.lower, fg="white", bg="#1E1E1E", selectcolor="#333").grid(row=1, column=0, sticky=tk.W, pady=5)
        tk.Checkbutton(check_frame, text="0-9 Numbers", variable=self.digits, fg="white", bg="#1E1E1E", selectcolor="#333").grid(row=2, column=0, sticky=tk.W, pady=5)
        tk.Checkbutton(check_frame, text="!@#$%^&* Symbols", variable=self.symbols, fg="white", bg="#1E1E1E", selectcolor="#333").grid(row=3, column=0, sticky=tk.W, pady=5)
        tk.Checkbutton(check_frame, text="Exclude similar (l1Io0O)", variable=self.exclude_similar, fg="#FF9800", bg="#1E1E1E", selectcolor="#333").grid(row=4, column=0, sticky=tk.W, pady=5)

        # Generate Button
        gen_btn = tk.Button(self.root, text="Generate Password", font=("Arial", 16, "bold"), bg="#00FF88", fg="black", height=2, width=20, command=self.generate_password)
        gen_btn.pack(pady=15)

        # Password Display
        self.password_var = tk.StringVar(value="Click Generate to create a password")
        pass_entry = tk.Entry(self.root, textvariable=self.password_var, font=("Consolas", 16, "bold"), justify="center", fg="#00FF88", bg="#1E1E1E", relief=tk.FLAT, state="readonly")
        pass_entry.pack(pady=10, fill=tk.X, padx=60)

        # Strength + Copy
        btn_frame = tk.Frame(self.root, bg="#121212")
        btn_frame.pack(pady=10)

        self.strength_label = tk.Label(btn_frame, text="Strength: N/A", font=("Arial", 12, "bold"), fg="gray", bg="#121212")
        self.strength_label.pack(side=tk.LEFT, padx=20)

        copy_btn = tk.Button(btn_frame, text="Copy", font=("Arial", 12, "bold"), bg="#2196F3", fg="white", command=self.copy_password)
        copy_btn.pack(side=tk.RIGHT, padx=20)

        # Save Password
        save_frame = tk.LabelFrame(self.root, text=" Save Password ", font=("Arial", 12, "bold"), fg="#FF5722", bg="#1E1E1E", padx=20, pady=10)
        save_frame.pack(pady=15, fill=tk.X, padx=40)

        tk.Label(save_frame, text="Name:", fg="white", bg="#1E1E1E").grid(row=0, column=0, padx=5)
        self.name_entry = tk.Entry(save_frame, width=30)
        self.name_entry.grid(row=0, column=1, padx=10)

        save_btn = tk.Button(save_frame, text="Save", bg="#4CAF50", fg="white", command=self.save_password)
        save_btn.grid(row=0, column=2, padx=10)

        # Saved Passwords List
        list_frame = tk.LabelFrame(self.root, text=" Saved Passwords ", font=("Arial", 12, "bold"), fg="#9C27B0", bg="#1E1E1E")
        list_frame.pack(pady=10, fill=tk.BOTH, expand=True, padx=40)

        self.saved_list = scrolledtext.ScrolledText(list_frame, height=6, font=("Consolas", 10), bg="#0F0F0F", fg="#00FF88")
        self.saved_list.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.refresh_saved_list()

        # Footer
        footer = tk.Label(self.root, text="Made with ❤️ | 100% Secure & Offline", fg="gray", bg="#121212", font=("Arial", 9))
        footer.pack(side=tk.BOTTOM, pady=10)

    def update_length(self, val):
        self.length_label.config(text=str(int(float(val))))

    def generate_password(self):
        length = self.length_var.get()
        include = ""
        if self.upper.get(): include += string.ascii_uppercase
        if self.lower.get(): include += string.ascii_lowercase
        if self.digits.get(): include += string.digits
        if self.symbols.get(): include += "!@#$%^&*()_+-=[]{}|;:,.<>?"

        if not include:
            messagebox.showwarning("Error", "Please select at least one character type!")
            return

        # Remove confusing characters
        if self.exclude_similar.get():
            exclude = "lI1O0o[]{}|/\\"
            include = ''.join(c for c in include if c not in exclude)

        password = ''.join(random.choice(include) for _ in range(length))
        self.password_var.set(password)
        self.update_strength(password)

    def update_strength(self, pwd):
        score = 0
        feedback = []
        if len(pwd) >= 12: score += 2
        elif len(pwd) >= 8: score += 1
        if any(c.isupper() for c in pwd): score += 1
        if any(c.islower() for c in pwd): score += 1
        if any(c.isdigit() for c in pwd): score += 1
        if any(c in "!@#$%^&*()_+-=" for c in pwd): score += 2

        if score >= 6:
            color, text = "#00FF88", "Very Strong"
        elif score >= 4:
            color, text = "#8BC34A", "Strong"
        elif score >= 3:
            color, text = "#FFEB3B", "Medium"
        else:
            color, text = "#F44336", "Weak"

        self.strength_label.config(text=f"Strength: {text}", fg=color)

    def copy_password(self):
        pwd = self.password_var.get()
        if pwd and pwd != "Click Generate to create a password":
            pyperclip.copy(pwd)
            messagebox.showinfo("Copied!", "Password copied to clipboard!")

    def save_password(self):
        name = self.name_entry.get().strip()
        pwd = self.password_var.get()
        if not name or not pwd or pwd == "Click Generate to create a password":
            messagebox.showwarning("Error", "Generate a password and enter a name!")
            return
        self.saved_passwords[name] = pwd
        save_passwords(self.saved_passwords)
        self.name_entry.delete(0, tk.END)
        self.refresh_saved_list()
        messagebox.showinfo("Saved", f"Password saved as '{name}'")

    def refresh_saved_list(self):
        self.saved_list.delete(1.0, tk.END)
        for name, pwd in self.saved_passwords.items():
            self.saved_list.insert(tk.END, f"{name}: {pwd}\n")

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGenerator(root)
    root.mainloop()