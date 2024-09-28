import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from PIL import Image, ImageTk
import os
from database.database import DatabaseConnection


class RegistrationFrame(tk.Frame):
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
            self.configure(bg="#f0f0f0")

    def create_widgets(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        container = ttk.Frame(self)
        container.grid(row=0, column=0)

        # Crear un estilo personalizado para el formulario de registro
        style = ttk.Style()
        style.configure('Custom.TFrame', background='#f5f5dc')  # Color específico para el formulario
        style.configure('Custom.TLabel', background='#f5f5dc')

        # Crear el frame principal del formulario con el color personalizado
        self.form_frame = ttk.Frame(container, padding="20", style='Custom.TFrame')  # Aplicar el estilo al formulario
        self.form_frame.grid(row=0, column=0, pady=20, padx=20)

        # Título del formulario de registro con el nuevo estilo
        ttk.Label(self.form_frame, text="Registration", font=("Arial", 20), style='Custom.TLabel').grid(column=0, row=0, columnspan=2, pady=(0, 20))

        self.fields = [
            ("User Type", ttk.Combobox(self.form_frame, values=['estudiante', 'directivo', 'docente', 'publico_general'], width=30)),
            ("Name", ttk.Entry(self.form_frame, width=30)),
            ("Surname", ttk.Entry(self.form_frame, width=30)),
            ("Birth Date", DateEntry(self.form_frame, date_pattern='yyyy-mm-dd', width=28)),
            ("Document Type", ttk.Combobox(self.form_frame, values=['CC', 'CE', 'PA', 'TI', 'PPT', 'PEP'], width=30)),
            ("Document Number", ttk.Entry(self.form_frame, width=30)),
            ("Email", ttk.Entry(self.form_frame, width=30)),
            ("Password", ttk.Entry(self.form_frame, show="*", width=30)),
            ("Phone", ttk.Entry(self.form_frame, width=30))
        ]

        for i, (text, entry) in enumerate(self.fields, start=1):
            # Aplicar el estilo a los labels de los campos del formulario
            ttk.Label(self.form_frame, text=text, style='Custom.TLabel').grid(column=0, row=i, sticky=tk.W, pady=5)
            entry.grid(column=1, row=i, sticky=(tk.W, tk.E), pady=5)
            setattr(self, text.lower().replace(" ", "_"), entry)

        # Crear un contenedor para los botones dentro del formulario y centrarlos
        buttons_frame = ttk.Frame(self.form_frame, style='Custom.TFrame')  # Aplicar el mismo color de fondo a los botones
        buttons_frame.grid(column=0, row=len(self.fields) + 1, columnspan=2, pady=(20, 10))

        # Agregar los botones dentro del contenedor centrado
        ttk.Button(buttons_frame, text="Register", command=self.register).grid(column=0, row=0, padx=(0, 10))  # Botón Register con espacio a la derecha
        ttk.Button(buttons_frame, text="Back to Login", command=self.show_login).grid(column=1, row=0, padx=(10, 0))  # Botón Back to Login con espacio a la izquierda

        # Mensaje de éxito o error en el formulario con el nuevo estilo
        self.message = ttk.Label(self.form_frame, text="", style='Custom.TLabel')
        self.message.grid(column=0, row=len(self.fields) + 3, columnspan=2, pady=(10, 0))

    def register(self):
        values = [getattr(self, field.lower().replace(" ", "_")).get() for field, _ in self.fields]
        cursor = self.db.call_procedure('InsertarUsuario', values)
        self.message.config(text="Registration successful! You can now login.")

    def show_login(self):
        self.master.show_frame("login")
