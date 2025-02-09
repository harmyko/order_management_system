import customtkinter as ctk
import sqlite3
from tkinter import messagebox, Listbox
import hashlib
from datetime import datetime

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

        self.login_button = ctk.CTkButton(self, text="Prisijungti", command=self.login)
        self.login_button.pack(pady=20)

        # self.bind('<Return>', lambda event: self.login())
        self.bind('<Return>', lambda event: self.open_app())

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

        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

        self.create_widgets()

    def create_widgets(self):
        self.form_frame = ctk.CTkFrame(self)
        self.form_frame.pack(pady=20, padx=20, fill='both', expand=True)

        self.id_label = ctk.CTkLabel(self.form_frame, text="Užsakymo ID:")
        self.id_label.grid(row=0, column=0, padx=5, pady=5)
        self.id_entry = ctk.CTkEntry(self.form_frame, width=50)
        self.id_entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        self.id_entry.insert(0, self.get_next_id())

        self.view_orders_button = ctk.CTkButton(self.form_frame, width=270, text="Peržiūrėti užsakymus", command=self.open_orders_window)
        self.view_orders_button.grid(row=0, column=2, columnspan=2, pady=10, sticky='e')


        self.name_label = ctk.CTkLabel(self.form_frame, text="Vardas:")
        self.name_label.grid(row=1, column=0, padx=5, pady=5)
        self.name_entry = ctk.CTkEntry(self.form_frame)
        self.name_entry.grid(row=1, column=1, padx=5, pady=5)

        self.phone_label = ctk.CTkLabel(self.form_frame, text="Telefono numeris:")
        self.phone_label.grid(row=1, column=2, padx=5, pady=5)
        self.phone_entry = ctk.CTkEntry(self.form_frame)
        self.phone_entry.grid(row=1, column=3, padx=5, pady=5)
        self.phone_entry.insert(0, "+3706")

        self.email_label = ctk.CTkLabel(self.form_frame, text="El. paštas:")
        self.email_label.grid(row=2, column=0, padx=5, pady=5)
        self.email_entry = ctk.CTkEntry(self.form_frame, width=410)
        self.email_entry.grid(row=2, column=1, padx=5, pady=5, columnspan=3)

        self.date_label = ctk.CTkLabel(self.form_frame, text="Data:")
        self.date_label.grid(row=3, column=0, padx=5, pady=5)
        self.date_entry = ctk.CTkEntry(self.form_frame)
        self.date_entry.grid(row=3, column=1, padx=5, pady=5)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d %H:%M"))

        self.state_label = ctk.CTkLabel(self.form_frame, text="Užsakymo būsena:")
        self.state_label.grid(row=3, column=2, padx=5, pady=5)
        self.state_entry = ctk.CTkComboBox(self.form_frame, values=["Užregistruotas", "Vykdomas", "Baigtas"])
        self.state_entry.grid(row=3, column=3, padx=5, pady=5)

        self.description_label = ctk.CTkLabel(self.form_frame, text="Aprašymas:")
        self.description_label.grid(row=4, column=0, padx=5, pady=5)
        self.description_entry = ctk.CTkTextbox(self.form_frame, width=400, height=100)
        self.description_entry.grid(row=4, column=1, padx=5, pady=5, columnspan=3)

        self.submit_button = ctk.CTkButton(self.form_frame, width=420, text="Pridėti naują užsakymą", command=self.submit_order)
        self.submit_button.grid(row=5, column=0, columnspan=4, pady=10, sticky='e')

        self.update_button = ctk.CTkButton(self.form_frame, width=420, text="Atnaujinti užsakymą", command=self.submit_order)
        self.update_button.grid(row=6, column=0, columnspan=4, pady=0, sticky='e')

    def get_next_id(self):
        conn = sqlite3.connect('orders.db')
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(id) FROM orders")
        result = cursor.fetchone()
        conn.close()
        if result[0] is not None:
            return result[0] + 1
        else:
            return 1

    def submit_order(self):
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()
        date = self.date_entry.get()
        state = self.state_entry.get()
        description = self.description_entry.get("1.0", 'end').strip()

        conn = sqlite3.connect('orders.db')
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                phone_number TEXT,
                email_address TEXT,
                date TEXT,
                current_order_state TEXT,
                description TEXT
            )
        """)
        cursor.execute("INSERT INTO orders (name, phone_number, email_address, date, current_order_state, description) VALUES (?, ?, ?, ?, ?, ?)",
                       (name, phone, email, date, state, description))
        conn.commit()
        conn.close()

        messagebox.showinfo("Užsakymas pridėtas", "Naujas užsakymas buvo sėkmingai pridėtas į užsakymų sąrašą.")
        self.clear_entries()

        self.id_entry.delete(0, 'end')
        self.id_entry.insert(0, self.get_next_id())

    def clear_entries(self):
        self.name_entry.delete(0, 'end')
        self.phone_entry.delete(0, 'end')
        self.phone_entry.insert(0, "+3706")
        self.email_entry.delete(0, 'end')
        self.date_entry.delete(0, 'end')
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d %H:%M"))
        self.state_entry.set('')
        self.description_entry.delete("1.0", 'end')

    def open_orders_window(self):
        orders_window = OrdersWindow(self)
        orders_window.grab_set()

    def on_closing(self):
        self.destroy()
        self.master.destroy()

class OrdersWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('Peržiūrėti užsakymus')
        self.geometry('800x400')
        self.minsize(600, 400)

        self.create_widgets()

    def create_widgets(self):
        self.orders_listbox = Listbox(self)
        self.orders_listbox.pack(fill='both', expand=True, padx=20, pady=20)

        self.load_orders()

        self.select_button = ctk.CTkButton(self, text="Pasirinkti užsakymą", command=self.select_order)
        self.select_button.pack(pady=10)

    def load_orders(self):
        conn = sqlite3.connect('orders.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, phone_number, email_address, date, current_order_state, description FROM orders")
        orders = cursor.fetchall()
        conn.close()

        for order in orders:
            self.orders_listbox.insert('end', f"ID: {order[0]}, Vardas: {order[1]}, Telefonas: {order[2]}, El. paštas: {order[3]}, Data: {order[4]}, Būsena: {order[5]}, Aprašymas: {order[6]}")

    def select_order(self):
        selected_order = self.orders_listbox.get(self.orders_listbox.curselection())
        order_id = selected_order.split(",")[0].split(":")[1].strip()

        conn = sqlite3.connect('orders.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
        order = cursor.fetchone()
        conn.close()

        self.master.id_entry.delete(0, 'end')
        self.master.id_entry.insert(0, order[0])
        self.master.name_entry.delete(0, 'end')
        self.master.name_entry.insert(0, order[1])
        self.master.phone_entry.delete(0, 'end')
        self.master.phone_entry.insert(0, order[2])
        self.master.email_entry.delete(0, 'end')
        self.master.email_entry.insert(0, order[3])
        self.master.date_entry.delete(0, 'end')
        self.master.date_entry.insert(0, order[4])
        self.master.state_entry.set(order[5])
        self.master.description_entry.delete("1.0", 'end')
        self.master.description_entry.insert("1.0", order[6])

        self.destroy()

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    loginWindow = Login_Window()
    loginWindow.mainloop()
