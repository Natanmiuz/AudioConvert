import tkinter as tk
from gui.gui import AudioConverter

# Corrección para que la GUI no se vea borrosa en pantallas con escalado (Windows)
try:
    import ctypes
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

if __name__ == "__main__":
    root = tk.Tk()
    app = AudioConverter(root)
    root.mainloop()
