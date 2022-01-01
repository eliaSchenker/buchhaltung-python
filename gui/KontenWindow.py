from PyQt5.QtWidgets import QWidget


class KontenWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def openMode(self):
        print("Opening Konten")