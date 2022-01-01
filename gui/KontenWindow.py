from PyQt5.QtWidgets import *

from controller.BuchhaltungsController import BuchhaltungsController
from gui.AddEditKonto import AddEditKonto


class KontenWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setLayout(QVBoxLayout())

        self.setWindowTitle("Buchen")

        # Add Menu
        topMenu = QWidget()
        topMenu.setLayout(QHBoxLayout())
        addKontoBtn = QPushButton("Konto hinzufügen")
        removeKontoBtn = QPushButton("Konto entfernen")

        addKontoBtn.clicked.connect(self.addKonto)
        removeKontoBtn.clicked.connect(self.removeKonto)

        topMenu.layout().addWidget(addKontoBtn)
        topMenu.layout().addWidget(removeKontoBtn)

        self.layout().addWidget(topMenu)

        # Initialize the table
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(["Konto", "Saldo"])
        self.layout().addWidget(self.tableWidget)

    def refreshTable(self):
        if BuchhaltungsController.konten is not None:
            self.tableWidget.setRowCount(len(BuchhaltungsController.konten))

            verticalLabels = []

            BuchhaltungsController.calculateSaldi()

            for i in range(len(BuchhaltungsController.konten)):
                verticalLabels.append("")
                self.tableWidget.setItem(i, 0, QTableWidgetItem(str(BuchhaltungsController.konten[i].kontenName)))
                self.tableWidget.setItem(i, 1, QTableWidgetItem(str(BuchhaltungsController.konten[i].saldo)))
            self.tableWidget.setVerticalHeaderLabels(verticalLabels)
            self.tableWidget.resizeColumnsToContents()

    def addKonto(self):
        self.addEditWindow = AddEditKonto(self.addKontoCallback)
        self.addEditWindow.setModal(True)
        self.addEditWindow.show()

    def addKontoCallback(self):
        BuchhaltungsController.addKonto(self.addEditWindow.getResult())
        self.refreshTable()

    def removeKonto(self):
        if self.tableWidget.currentRow() == -1:
            msg = QMessageBox()
            msg.setWindowTitle("Warnung")
            msg.setText("Löschen nicht möglich, kein Konto selektiert.")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()
        else:
            reply = QMessageBox.question(self, '',
                                         "Sind Sie sicher, dass Sie das selektierte Konto löschen wollen?",
                                         QMessageBox.Yes,
                                         QMessageBox.No)

            if reply == QMessageBox.Yes:
                BuchhaltungsController.removeKonto(self.tableWidget.currentRow())
                self.refreshTable()

    def openMode(self):
        self.refreshTable()
        self.show()