from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QWidget, QLabel, QListWidget, QPushButton, QVBoxLayout

from controller.BuchhaltungsController import BuchhaltungsController
from gui.BuchenWindow import BuchenWindow
from gui.KontenWindow import KontenWindow


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__()
        # Prepare GUI
        mainLayout = QVBoxLayout(*args, **kwargs)
        mainWidget = QWidget()
        mainWidget.setLayout(mainLayout)
        mainLayout.addWidget(QLabel("Buchhaltung"))
        self.modeList = QListWidget()
        mainLayout.addWidget(self.modeList)
        openModeBtn = QPushButton("Öffnen")
        openModeBtn.clicked.connect(self.openCurrentMode)
        mainLayout.addWidget(openModeBtn)

        # Fill modes
        self.modes = [["Buchen", BuchenWindow()], ["Konten", KontenWindow()]]
        for i in self.modes:
            self.modeList.addItem(i[0])

        BuchhaltungsController.loadBuchungen()
        BuchhaltungsController.loadKonten()

        self.setCentralWidget(mainWidget)
        self.show()

    def openCurrentMode(self):
        if len(self.modeList.selectedIndexes()) == 1:
            self.modes[self.modeList.currentRow()][1].openMode()
