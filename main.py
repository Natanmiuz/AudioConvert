from gui.gui import AudioConverter
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    app = AudioConverter(root)
    root.mainloop()