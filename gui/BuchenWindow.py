from PyQt5.QtWidgets import *

from controller.BuchhaltungsController import BuchhaltungsController
from gui.AddEditBuchung import AddEditbuchung


class BuchenWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setLayout(QVBoxLayout())

        self.setWindowTitle("Buchen")

        # Add Menu
        topMenu = QWidget()
        topMenu.setLayout(QHBoxLayout())
        addBuchungBtn = QPushButton("Buchung hinzufügen")
        editBuchungBtn = QPushButton("Buchung editieren")
        removeBuchungBtn = QPushButton("Buchung entfernen")

        addBuchungBtn.clicked.connect(self.addBuchung)
        editBuchungBtn.clicked.connect(self.editBuchung)
        removeBuchungBtn.clicked.connect(self.removeBuchung)

        topMenu.layout().addWidget(addBuchungBtn)
        topMenu.layout().addWidget(editBuchungBtn)
        topMenu.layout().addWidget(removeBuchungBtn)

        self.layout().addWidget(topMenu)

        # Initialize the table
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setHorizontalHeaderLabels(["Konto 1", "Konto 2", "Datum", "Beschreibung", "Betrag"])
        self.layout().addWidget(self.tableWidget)

    def refreshTable(self):
        """
        Fills the buchungen table with data
        """
        if BuchhaltungsController.buchungen is not None:
            self.tableWidget.setRowCount(len(BuchhaltungsController.buchungen))

            verticalLabels = []

            for i in range(len(BuchhaltungsController.buchungen)):
                verticalLabels.append("")
                array = BuchhaltungsController.buchungen[i].getStringValuesArray()
                for j in range(len(array)):
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(array[j])))
            self.tableWidget.setVerticalHeaderLabels(verticalLabels)
            self.tableWidget.resizeColumnsToContents()

    def addBuchung(self):
        self.addEditWindow = AddEditbuchung(self.addBuchungCallback)
        self.addEditWindow.setModal(True)
        self.addEditWindow.show()

    def addBuchungCallback(self):
        BuchhaltungsController.addBuchung(self.addEditWindow.getResult())
        self.refreshTable()

    def editBuchung(self):
        if self.tableWidget.currentRow() == -1:
            msg = QMessageBox()
            msg.setWindowTitle("Warnung")
            msg.setText("Editieren nicht möglich, keine Buchung selektiert.")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()
        else:
            self.addEditWindow = AddEditbuchung(self.editBuchungCallback, buchung=BuchhaltungsController.buchungen[self.tableWidget.currentRow()])
            self.addEditWindow.setModal(True)
            self.addEditWindow.show()

    def editBuchungCallback(self):
        BuchhaltungsController.editBuchung(self.tableWidget.currentRow(), self.addEditWindow.getResult())
        self.refreshTable()

    def removeBuchung(self):
        if self.tableWidget.currentRow() == -1:
            msg = QMessageBox()
            msg.setWindowTitle("Warnung")
            msg.setText("Löschen nicht möglich, keine Buchung selektiert.")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()
        else:
            reply = QMessageBox.question(self, '',
                                         "Sind Sie sicher, dass Sie die selektierte Buchung löschen wollen?",
                                         QMessageBox.Yes,
                                         QMessageBox.No)

            if reply == QMessageBox.Yes:
                BuchhaltungsController.removeBuchung(self.tableWidget.currentRow())
                self.refreshTable()

    def openMode(self):
        self.refreshTable()
        self.show()
