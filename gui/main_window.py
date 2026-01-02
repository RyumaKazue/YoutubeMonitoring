from PySide6.QtWidgets import QApplication
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QIODevice
from PySide6.QtWidgets import QPushButton
import sys

class main_window:
    def __init__(self, ui_path):
        self.loader = QUiLoader()
        self.app = QApplication()
        self.window = None
        self.startAndPauseButton = None
        self.stopButton = None

        self.load_ui(ui_path)

    def load_ui(self, ui_file_path):
        ui_file = QFile(ui_file_path)
        if not ui_file.open(QIODevice.ReadOnly):
            raise FileNotFoundError(f"Cannot open {ui_file_path}")
        
        self.window = self.loader.load(ui_file)
        self.startAndPauseButton = self.window.findChild(QPushButton, "StartAndPauseBt")
        self.stopButton = self.window.findChild(QPushButton, "StopBt")

        ui_file.close()

    def setStartAndPauseButtonHandler(self, handler):
        if not self.startAndPauseButton:
            raise RuntimeError("UI not loaded or StartAndPause button not found")
        self.startAndPauseButton.clicked.connect(handler)

    def setStopButtonHandler(self, handler):
        if not self.stopButton:
            raise RuntimeError("UI not loaded or Stop button not found")
        self.stopButton.clicked.connect(handler)

    def show(self):
        if not self.window:
            print("Error: UI not loaded")

        self.window.show()

    def run(self):
        sys.exit(self.app.exec())

