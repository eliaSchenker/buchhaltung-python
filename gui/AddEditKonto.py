from PyQt5.QtWidgets import *

from model.Konto import Konto


class AddEditKonto(QDialog):
    def __init__(self, callback, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.callback = callback

        # Initialize GUI
        self.setLayout(QGridLayout())

        self.kontoNameInput = QLineEdit()
        self.aktivKonto = QCheckBox()

        doneBtn = QPushButton("Hinzufügen")
        doneBtn.clicked.connect(self.doneBtnClick)

        self.layout().addWidget(QLabel("Konto 1:"), 0, 0)
        self.layout().addWidget(self.kontoNameInput, 0, 1)
        self.layout().addWidget(QLabel("Aktivkonto?:"), 1, 0)
        self.layout().addWidget(self.aktivKonto, 1, 1)
        self.layout().addWidget(doneBtn)

    def doneBtnClick(self):
        self.callback()
        self.close()

    def getResult(self):
        return Konto(self.kontoNameInput.text(), self.aktivKonto.isChecked())