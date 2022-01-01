from datetime import datetime

from model.Konto import Konto
from controller.SaveLoadUtil import SaveLoadUtil
from model.Buchung import Buchung


class BuchhaltungsController:
    buchungen = []
    konten = []

    @staticmethod
    def loadKonten():
        lines = SaveLoadUtil.loadFile("konten.txt")
        BuchhaltungsController.konten = []
        for i in lines:
            data = i.split("|")
            aktivKonto = False
            if data[1] == 'A':
                aktivKonto = True
            BuchhaltungsController.konten.append(Konto(data[0], aktivKonto))

    @staticmethod
    def loadBuchungen():
        lines = SaveLoadUtil.loadFile("buchungen.txt")
        BuchhaltungsController.buchungen = []
        for i in lines:
            data = i.split("|")
            BuchhaltungsController.buchungen.append(
                Buchung(data[0], data[1], datetime.strptime(data[2], "%d.%m.%Y"), data[3], float(data[4])))

    @staticmethod
    def saveBuchungen():
        lines = []
        for i in BuchhaltungsController.buchungen:
            lines.append(i.konto1 + "|" + i.konto2 + "|" + i.date.strftime("%d.%m.%Y") + "|" + i.beschreibung + "|" + str(i.betrag))
        SaveLoadUtil.saveFile("buchungen.txt", lines)

    @staticmethod
    def addBuchung(buchung):
        BuchhaltungsController.buchungen.append(buchung)
        BuchhaltungsController.buchungen.sort(key=lambda x: x.date, reverse=True)
        BuchhaltungsController.saveBuchungen()

    @staticmethod
    def editBuchung(index, neueBuchung):
        BuchhaltungsController.buchungen[index] = neueBuchung
        BuchhaltungsController.buchungen.sort(key=lambda x: x.date, reverse=True)
        BuchhaltungsController.saveBuchungen()

    @staticmethod
    def removeBuchung(index):
        BuchhaltungsController.buchungen.pop(index)
        BuchhaltungsController.saveBuchungen()
