import time

from controller.Konto import Konto
from controller.SaveLoadUtil import SaveLoadUtil
from model.Buchung import Buchung


class BuchhaltungsController:
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
            BuchhaltungsController.buchungen.append(Buchung(data[0], data[1], time.strptime(data[2], "%d.%m.%y"), data[3], int(data[4])))