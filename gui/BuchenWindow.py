from PyQt5.QtWidgets import *

from controller.BuchhaltungsController import BuchhaltungsController
from controller.SaveLoadUtil import SaveLoadUtil


class BuchenWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setLayout(QVBoxLayout())

        self.setWindowTitle("Buchen")

        #Initialize the table
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setHorizontalHeaderLabels(["Konto 1", "Konto 2", "Datum", "Beschreibung", "Betrag"])
        self.layout().addWidget(self.tableWidget)

    def fillTable(self):
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


    def openMode(self):
        self.fillTable()
        self.show()
