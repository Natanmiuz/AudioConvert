import tkinter as tk
from tkinter import filedialog, messagebox
import os
from core.convert import convert_audio

class AudioConverter:
    def __init__(self, master):
        self.master = master
        master.title("Conversor de Audio")
        master.geometry("500x300")
        master.resizable(False, False)
        
        # Variables
        self.input_path = ""
        self.output_format = tk.StringVar(value="mp3")
        
        # Crear widgets
        self.create_widgets()
        
    def create_widgets(self):
        # Configuración de colores
        bg_color = "#f0f0f0"
        btn_color = "#e1e1e1"
        self.master.config(bg=bg_color)
        
        # Marco principal
        main_frame = tk.Frame(self.master, bg=bg_color)
        main_frame.pack(pady=20, padx=30, fill="both", expand=True)
        
        # Título
        tk.Label(main_frame, text="Conversor de Formatos de Audio", 
                font=("Arial", 16, "bold"), bg=bg_color).pack(pady=(0, 20))
        
        # Botón para cargar archivo
        self.btn_load = tk.Button(main_frame, text="Seleccionar archivo de audio", 
                             command=self.load_file, bg=btn_color, width=25)
        self.btn_load.pack(pady=5)
        
        # Etiqueta de archivo seleccionado
        self.file_label = tk.Label(main_frame, text="No se ha seleccionado ningún archivo", 
                                bg=bg_color, wraplength=400)
        self.file_label.pack(pady=10)
        
        # Formato de salida
        format_frame = tk.Frame(main_frame, bg=bg_color)
        format_frame.pack(pady=10)
        
        tk.Label(format_frame, text="Formato de salida:", bg=bg_color).pack(side=tk.LEFT)
        
        format_options = ["mp3", "wav", "flac", "ogg", "aiff", "m4a"]
        self.format_menu = tk.OptionMenu(format_frame, self.output_format, *format_options)
        self.format_menu.config(width=8)
        self.format_menu.pack(side=tk.LEFT, padx=10)
        
        # Botón de conversión
        self.btn_convert = tk.Button(main_frame, text="Convertir", 
                                command=self.convert_file, bg="#4CAF50", fg="white",
                                state=tk.DISABLED, width=15)
        self.btn_convert.pack(pady=20)
        
        # Barra de estado
        self.status = tk.Label(main_frame, text="Listo", bg=bg_color, fg="gray", 
                            anchor="w", font=("Arial", 9))
        self.status.pack(side=tk.BOTTOM, fill=tk.X)
    
    def load_file(self):
        filetypes = (
            ('Archivos de audio', '*.mp3 *.wav *.flac *.ogg *.aiff *.m4a *.wma'),
            ('Todos los archivos', '*.*')
        )
        
        self.input_path = filedialog.askopenfilename(
            title="Seleccionar archivo de audio",
            filetypes=filetypes
        )
        
        if self.input_path:
            filename = os.path.basename(self.input_path)
            self.file_label.config(text=filename)
            self.btn_convert.config(state=tk.NORMAL)
            self.status.config(text="Archivo cargado: " + filename)
    
    def convert_file(self):
        if not self.input_path:
            return
        
        output_format = self.output_format.get().lower()
        
        try:
            self.status.config(text=f"Convirtiendo a {output_format.upper()}...", fg="blue")
            self.master.update()
            
            output_path = convert_audio(self.input_path, output_format)
            
            self.status.config(text=f"Conversión completada: {os.path.basename(output_path)}", fg="green")
            messagebox.showinfo("Éxito", f"Archivo convertido con éxito!\n{output_path}")
        
        except Exception as e:
            self.status.config(text=f"Error: {str(e)}", fg="red")
            messagebox.showerror("Error de Conversión", 
                               f"Detalles del error:\n{str(e)}\n\n"
                               "Asegúrate que FFmpeg está instalado y en el PATH.")