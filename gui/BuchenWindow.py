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
        """
        Opens the AddBuchung Popup
        """
        self.addEditWindow = AddEditbuchung(self.addBuchungCallback)
        self.addEditWindow.setModal(True)
        self.addEditWindow.show()

    def addBuchungCallback(self):
        """
        Gets called when the user successfully added a Buchung in the popup
        """
        BuchhaltungsController.addBuchung(self.addEditWindow.getResult())
        self.refreshTable()

    def editBuchung(self):
        """
        Opens the EditBuchung Popup
        """
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
        """
        Gets called when the user successfully edited the Buchung in the popup
        """
        BuchhaltungsController.editBuchung(self.tableWidget.currentRow(), self.addEditWindow.getResult())
        self.refreshTable()

    def removeBuchung(self):
        """
        Removes a Buchung
        """
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
        """
        Opens the BuchenWindow mode
        """
        self.refreshTable()
        self.show()
