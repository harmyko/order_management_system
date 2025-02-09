import customtkinter as ctk
from tkinter import messagebox
import hashlib
import sqlite3

class Login_Window(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title('Login')
        self.geometry('175x150')
        self.resizable(False, False)

        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

        self.username_label = ctk.CTkLabel(self, text="Vartotojo vardas:")
        self.username_label.pack()
        self.username_entry = ctk.CTkEntry(self)
        self.username_entry.pack()

        self.password_label = ctk.CTkLabel(self, text="Slaptažodis:")
        self.password_label.pack()
        self.password_entry = ctk.CTkEntry(self, show="*")
        self.password_entry.pack()

        self.login_button = ctk.CTkButton(self, text="Login", command=self.login)
        self.login_button.pack(pady=20)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        conn = sqlite3.connect('vartotojai.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password_hash = ?", (username, password_hash))
        result = cursor.fetchone()
        conn.close()

        if result:
            self.open_app()
        else:
            messagebox.showerror("Prisijungti nepavyko", "Neteisingas vartotojo vardas arba slaptažodis.")

    def open_app(self):
        self.withdraw()
        app = App(self)
        app.mainloop()

class App(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('Užsakymai')
        self.geometry('1200x600')
        self.minsize(600, 400)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.new_order_button = ctk.CTkButton(self, text="Pridėti užsakymą", command=self.new_order)
        self.new_order_button.pack(pady=20)

    def new_order(self):
        pass

    def on_closing(self):
        self.destroy()
        self.master.destroy()

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    loginWindow = Login_Window()
    loginWindow.mainloop()
