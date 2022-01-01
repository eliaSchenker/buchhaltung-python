import datetime

from PyQt5.QtWidgets import *

from controller.BuchhaltungsController import BuchhaltungsController
from model.Buchung import Buchung


class AddEditbuchung(QDialog):
    def __init__(self, callback, buchung=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.callback = callback

        #Initialize GUI
        self.setLayout(QGridLayout())

        self.konto1Input = QLineEdit()
        self.konto2Input = QLineEdit()
        self.dateInput = QCalendarWidget()
        self.beschreibung = QLineEdit()
        self.betrag = QDoubleSpinBox()
        doneBtn = QPushButton()
        doneBtn.clicked.connect(self.doneBtnClick)

        self.layout().addWidget(QLabel("Konto 1:"), 0, 0)
        self.layout().addWidget(self.konto1Input, 0, 1)
        self.layout().addWidget(QLabel("Konto 2:"), 1, 0)
        self.layout().addWidget(self.konto2Input, 1, 1)
        self.layout().addWidget(QLabel("Datum:"), 2, 0)
        self.layout().addWidget(self.dateInput, 2, 1)
        self.layout().addWidget(QLabel("Beschreibung:"), 3, 0)
        self.layout().addWidget(self.beschreibung, 3, 1)
        self.layout().addWidget(QLabel("Betrag:"), 4, 0)
        self.layout().addWidget(self.betrag, 4, 1)
        self.layout().addWidget(doneBtn)

        self.setInputAutocomplete()

        if buchung is None:
            self.setWindowTitle("Buchung hinzufügen")
            self.dateInput.showToday()
            doneBtn.setText("Hinzufügen")
        else:
            self.setWindowTitle("Buchung editieren")
            doneBtn.setText("Editieren")

            #Set the values of the Buchung
            self.konto1Input.setText(buchung.konto1)
            self.konto2Input.setText(buchung.konto2)
            self.dateInput.setSelectedDate(buchung.date)
            self.beschreibung.setText(buchung.beschreibung)
            self.betrag.setValue(buchung.betrag)


    def setInputAutocomplete(self):
        """
        Sets the autocomplete for the Konto1, Konto2 and Beschreibung input fields
        """
        kontenNames = []
        for i in BuchhaltungsController.konten:
            if i.kontenName not in kontenNames:
                kontenNames.append(i.kontenName)
        kontoCompleter = QCompleter(kontenNames)
        self.konto1Input.setCompleter(kontoCompleter)
        self.konto2Input.setCompleter(kontoCompleter)

        beschreibungen = []
        for i in BuchhaltungsController.buchungen:
            if i.beschreibung not in beschreibungen:
                beschreibungen.append(i.beschreibung)
        self.beschreibung.setCompleter(QCompleter(beschreibungen))

    def doneBtnClick(self):
        self.callback()
        self.close()

    def getResult(self):
        date = datetime.datetime.fromordinal(self.dateInput.selectedDate().toPyDate().toordinal())
        return Buchung(self.konto1Input.text(), self.konto2Input.text(), date, self.beschreibung.text(), self.betrag.value())