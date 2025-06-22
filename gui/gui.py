import os
from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFileDialog, QComboBox, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPalette, QColor, QIcon, QCursor
from core.convert import convert_audio




class AudioConverterApp(QMainWindow):
    def __init__(self):
        super().__init__()  
        self.setWindowTitle("Audio Converter")
        #self.setWindowIcon(QIcon("favico.ico"))  #ESTA PORQUERIA NO SE PONE AHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH ¿COMO SE PONE EL ICONO?
        self.setWindowIcon(QIcon.fromTheme("folder"))
        self.setGeometry(100, 100, 600, 400)
        self.setMinimumSize(500, 350)
        self.setup_ui()
        self.apply_dark_theme()
        
        self.input_path = ""
        self.output_path = ""
        
        
    def apply_dark_theme(self):
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(35, 35, 35))
        dark_palette.setColor(QPalette.WindowText, QColor(220, 220, 220))
        dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
        dark_palette.setColor(QPalette.AlternateBase, QColor(45, 45, 45))
        dark_palette.setColor(QPalette.ToolTipBase, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ToolTipText, Qt.white)
        dark_palette.setColor(QPalette.Text, QColor(220, 220, 220))
        dark_palette.setColor(QPalette.Button, QColor(70, 70, 70))
        dark_palette.setColor(QPalette.ButtonText, QColor(220, 220, 220))
        dark_palette.setColor(QPalette.BrightText, Qt.red)
        dark_palette.setColor(QPalette.Highlight, QColor(142, 45, 197))
        dark_palette.setColor(QPalette.HighlightedText, Qt.white)
        dark_palette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(127, 127, 127))
        
        self.setPalette(dark_palette)
        

        self.setStyleSheet("""
            QWidget {
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            
            QGroupBox {
                border: 1px solid #444;
                border-radius: 6px;
                margin-top: 10px;
                padding-top: 15px;
                font-weight: bold;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
            
            QPushButton {
                background-color: #5c5c5c;
                color: #fff;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                min-width: 100px;
            }
            
            QPushButton:hover {
                background-color: #6c6c6c;
            }
            
            QPushButton:pressed {
                background-color: #4c4c4c;
            }
            
            QPushButton:disabled {
                background-color: #3a3a3a;
                color: #888;
            }
            
            QComboBox {
                background-color: #3a3a3a;
                color: #fff;
                border: 1px solid #444;
                border-radius: 4px;
                padding: 5px;
            }
            
            QComboBox::drop-down {
                width: 20px;
                border-left: 1px solid #444;
            }
            
            QComboBox QAbstractItemView {
                background-color: #3a3a3a;
                color: #fff;
                selection-background-color: #8e2dc5;
                border: 1px solid #444;
            }
            
            QLabel {
                color: #ddd;
            }
        """)

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 15, 20, 10)
        main_layout.setSpacing(15)
        
        title = QLabel("Audio Converter ")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #8e2dc5; margin-bottom: 10px;")
        main_layout.addWidget(title)
        
        input_layout = QHBoxLayout()
        
        self.input_label = QLabel("No file selected")
        self.input_label.setStyleSheet("padding: 5px; border: 1px dashed #555; border-radius: 4px;")
        self.input_label.setMinimumHeight(30)
        input_layout.addWidget(self.input_label, 5)
        
        self.btn_select = QPushButton("Select File")
        self.btn_select.setCursor(Qt.PointingHandCursor) 
        self.btn_select.clicked.connect(self.select_file)
        input_layout.addWidget(self.btn_select, 1)
        
        main_layout.addLayout(input_layout)
  
        output_layout = QHBoxLayout()
    
        self.output_label = QLabel("Default output folder")
        self.output_label.setStyleSheet("padding: 5px; border: 1px dashed #555; border-radius: 4px;")
        self.output_label.setMinimumHeight(30)
        output_layout.addWidget(self.output_label, 5)
        
        self.btn_output = QPushButton("Select Folder")
        self.btn_output.setCursor(Qt.PointingHandCursor) 
        self.btn_output.clicked.connect(self.select_output_folder)
        output_layout.addWidget(self.btn_output, 1)
        
        main_layout.addLayout(output_layout)
        
        format_layout = QHBoxLayout()
        format_layout.addWidget(QLabel("Output Format:"))
        
        self.format_combo = QComboBox()
        self.format_combo.addItems(["MP3", "WAV", "FLAC", "OGG", "AIFF", "M4A"])
        self.format_combo.setCurrentIndex(0)
        self.format_combo.setCursor(Qt.PointingHandCursor)  
        format_layout.addWidget(self.format_combo, 1)
        
        main_layout.addLayout(format_layout)
        
        self.btn_convert = QPushButton("Convert Audio")
        self.btn_convert.setEnabled(False)
        self.btn_convert.setCursor(Qt.PointingHandCursor) 
        self.btn_convert.setStyleSheet("""
            background-color: #8e2dc5;
            color: white;
            font-weight: bold;
            padding: 10px;
            font-size: 14px;
        """)
        self.btn_convert.clicked.connect(self.convert_file)
        main_layout.addWidget(self.btn_convert)
        
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet("color: #aaa; font-size: 10pt; padding: 5px;")
        self.status_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.status_label)
        
   #     try:
    #        self.setWindowIcon(QIcon("icon/icon.png"))
     #   except:
      #      pass

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Audio File",
            "",
            "Audio Files (*.mp3 *.wav *.flac *.ogg *.aiff *.m4a *.wma);;All Files (*)"
        )
        
        if file_path:
            self.input_path = file_path
            filename = os.path.basename(file_path)
            self.input_label.setText(filename)
            self.input_label.setToolTip(file_path)
            self.btn_convert.setEnabled(True)
            self.status_label.setText(f"Loaded: {filename}")
            self.status_label.setStyleSheet("color: #a0ffa0; font-size: 10pt; padding: 5px;")
            
            if not self.output_path:
                self.output_label.setText("Default output folder")
                self.output_label.setToolTip("")

    def select_output_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if folder:
            self.output_path = folder
            display_text = folder
            if len(folder) > 40:
                display_text = f"...{folder[-37:]}"
            self.output_label.setText(display_text)
            self.output_label.setToolTip(folder)

    def convert_file(self):
        if not self.input_path:
            return
            
        output_format = self.format_combo.currentText().lower()
        
        try:
            self.status_label.setText(f"Converting to {output_format.upper()}...")
            self.status_label.setStyleSheet("color: #88aaff; font-size: 10pt; padding: 5px;")
            self.btn_convert.setEnabled(False)
            QApplication.processEvents()  
            
            output_path = convert_audio(
                self.input_path, 
                output_format,
                output_dir=self.output_path if self.output_path else None
            )
            
            filename = os.path.basename(output_path)
            self.status_label.setText(f"Conversion successful: {filename}")
            self.status_label.setStyleSheet("color: #a0ffa0; font-size: 10pt; padding: 5px;")
            self.btn_convert.setEnabled(True)
            
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Success")
            msg.setText(f"File converted successfully!\n{filename}")
            msg.setStandardButtons(QMessageBox.Open | QMessageBox.Ok)
            msg.setDefaultButton(QMessageBox.Ok)
            msg.button(QMessageBox.Open).setText("Open Folder")
            
            response = msg.exec_()
            if response == QMessageBox.Open:
                folder = os.path.dirname(output_path)
                os.startfile(folder) 
        
        except Exception as e:
            self.status_label.setText(f"Error: {str(e)}")
            self.status_label.setStyleSheet("color: #ff8888; font-size: 10pt; padding: 5px;")
            self.btn_convert.setEnabled(True)
            QMessageBox.critical(self, "Conversion Error", 
                f"Error details:\n{str(e)}\n\n"
                "Please ensure FFmpeg is installed and available in your system PATH.")