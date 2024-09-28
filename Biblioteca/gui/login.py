import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

from database.database import DatabaseConnection


class LoginFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.db = DatabaseConnection()
        self.create_background()
        self.create_widgets()

    def create_background(self):
        try:
            # Cargar y redimensionar la imagen de fondo
            image_path = r"C:\Users\311\Downloads\Biblioteca\images\hola.jpg"
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"La imagen no se encuentra en: {image_path}")

            background_image = Image.open(image_path)
            background_image = background_image.resize((800, 600), Image.LANCZOS)
            self.bg_image = ImageTk.PhotoImage(background_image)

            # Crear un label para el fondo
            self.background_label = tk.Label(self, image=self.bg_image)
            self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            print(f"Error al cargar la imagen de fondo: {e}")
            # Si hay un error, establecer un color de fondo por defecto
            self.configure(bg="#0b2363")

    def create_widgets(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        container = ttk.Frame(self)
        container.grid(row=0, column=0)

        # Cambiar el color de fondo del frame principal a beige
        self.frame = ttk.Frame(container, padding="20", style='Beige.TFrame')
        self.frame.grid(row=0, column=0)

        style = ttk.Style()
        style.configure('TLabel', background='#f0f0f0')
        style.configure('Beige.TFrame', background='#f5f5dc')
        style.configure('TFrame', background='#f0f0f0')

        ttk.Label(self.frame, text="Login", font=("arial", 20, "bold")).grid(column=0, row=0, columnspan=2, pady=(0, 20))

        ttk.Label(self.frame, text="User Type:", font=("arial", 10)).grid(column=0, row=1, sticky=tk.W, pady=5)
        self.user_type = ttk.Combobox(self.frame, values=['estudiante', 'directivo', 'docente', 'publico_general'],
                                      width=30)
        self.user_type.grid(column=1, row=1, sticky=(tk.W, tk.E), pady=5)

        ttk.Label(self.frame, text="Email:", font=("arial", 10)).grid(column=0, row=2, sticky=tk.W, pady=5)
        self.email = ttk.Entry(self.frame, width=30)
        self.email.grid(column=1, row=2, sticky=(tk.W, tk.E), pady=5)

        ttk.Label(self.frame, text="Password:", font=("arial", 10)).grid(column=0, row=3, sticky=tk.W, pady=5)
        self.password = ttk.Entry(self.frame, show="*", width=30)
        self.password.grid(column=1, row=3, sticky=(tk.W, tk.E), pady=5)

        ttk.Button(self.frame, text="Login", command=self.login).grid(column=0, row=4, columnspan=2, pady=(20, 10))
        ttk.Button(self.frame, text="Register", command=self.show_register).grid(column=0, row=5, columnspan=2)

        self.message = ttk.Label(self.frame, text="")
        self.message.grid(column=0, row=6, columnspan=2, pady=(10, 0))

    def login(self):
        user_type = self.user_type.get()
        email = self.email.get().strip()
        password = self.password.get().strip()

        if not email or not password:
            self.message.config(text="Please enter email and password.")
            return

        try:
            with DatabaseConnection() as db:
                results = db.call_procedure('VerificarUsuario', [email, password, user_type])

                if results:
                    result = results[0]
                    if result[0] == 1:
                        self.message.config(text="Login successful!")
                        self.master.show_frame("usermanagement")
                    else:
                        self.message.config(text="Invalid email or password.")
                else:
                    self.message.config(text="No results returned from the procedure.")
        except Exception as e:
            self.message.config(text=f"An error occurred: {e}")

    def show_register(self):
        self.master.show_frame("registration")
