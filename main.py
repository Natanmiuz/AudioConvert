import tkinter as tk
from gui.gui import AudioConverter

try:
  
    import ctypes
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

if __name__ == "__main__":
    root = tk.Tk()
    app = AudioConverter(root)
    root.mainloop()
