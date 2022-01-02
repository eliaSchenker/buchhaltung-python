from datetime import datetime

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
import pyqtgraph as pg

from controller.BuchhaltungsController import BuchhaltungsController
from util.TimeAxisItem import TimeAxisItem

import colorsys


class StatisticWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Initialize Graph
        self.chart = pg.PlotWidget(axisItems={'bottom': TimeAxisItem(orientation='bottom')})
        self.chart.setBackground('w')
        self.chart.addLegend()

        self.kontoSelection = QListWidget()
        self.kontoSelection.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.kontoSelection.selectionModel().selectionChanged.connect(self.updateStatistic)

        self.setLayout(QHBoxLayout())
        self.layout().addWidget(self.chart)
        self.layout().addWidget(self.kontoSelection)

    def initializeKontoSelection(self):
        self.kontoSelection.clear()
        for i in BuchhaltungsController.konten:
            self.kontoSelection.addItem(i.kontenName)

    def updateStatistic(self):
        selectedItems = [item.text() for item in self.kontoSelection.selectedItems()]

        kontenSaldi = {}
        for i in BuchhaltungsController.konten:
            kontenSaldi[i.kontenName] = [i.aktivKonto, [[0, None]]]

        for i in BuchhaltungsController.buchungen[::-1]:
            timestamp = datetime.timestamp(i.date)
            if i.konto1 in kontenSaldi.keys():
                if kontenSaldi[i.konto1][0]:
                    kontenSaldi[i.konto1][1].append([kontenSaldi[i.konto1][1][-1][0] + i.betrag, timestamp])
                else:
                    kontenSaldi[i.konto1][1].append([kontenSaldi[i.konto1][1][-1][0] - i.betrag, timestamp])

            if i.konto2 in kontenSaldi.keys():
                if kontenSaldi[i.konto2][0]:
                    kontenSaldi[i.konto2][1].append([kontenSaldi[i.konto2][1][-1][0] - i.betrag, timestamp])
                else:
                    kontenSaldi[i.konto2][1].append([kontenSaldi[i.konto2][1][-1][0] + i.betrag, timestamp])

        self.chart.clear()

        kontenAmount = 0
        for i in kontenSaldi.keys():
            if i in selectedItems:
                kontenAmount += 1

        if kontenAmount != 0:
            step = 360 / kontenAmount
        else:
            step = 0

        kontenCounter = 0
        for i in kontenSaldi.keys():
            if i in selectedItems:
                value = kontenSaldi[i]
                dates = []
                data = []
                counter = 0
                for j in value[1]:
                    if counter != 0:
                        data.append(j[0])
                        dates.append(j[1])
                    counter += 1
                color = colorsys.hsv_to_rgb(step * kontenCounter / 360, 1, 1)
                self.chart.plot(dates, data, name=i, pen=pg.mkPen(color=(round(color[0] * 255),
                                                                         round(color[1] * 255),
                                                                         round(color[2] * 255))))
                kontenCounter += 1
        self.chart.autoRange()

    def openMode(self):
        self.initializeKontoSelection()
        self.updateStatistic()
        self.show()
