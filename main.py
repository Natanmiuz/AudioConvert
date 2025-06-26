import sys
from gui.gui import AudioConverterApp
from PyQt5.QtWidgets import QApplication

 
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AudioConverterApp()
    window.show()
    sys.exit(app.exec_())