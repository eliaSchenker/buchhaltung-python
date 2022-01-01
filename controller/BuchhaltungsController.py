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
    def saveKonten():
        lines = []
        for i in BuchhaltungsController.konten:
            kontenZeichen = 'P'
            if i.aktivKonto:
                kontenZeichen = 'A'
            lines.append(i.kontenName + "|" + kontenZeichen)
        SaveLoadUtil.saveFile("konten.txt", lines)

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
            lines.append(
                i.konto1 + "|" + i.konto2 + "|" + i.date.strftime("%d.%m.%Y") + "|" + i.beschreibung + "|" + str(
                    i.betrag))
        SaveLoadUtil.saveFile("buchungen.txt", lines)

    @staticmethod
    def calculateSaldi():
        for i in BuchhaltungsController.konten:
            i.saldo = 0
        for i in BuchhaltungsController.buchungen:
            for j in BuchhaltungsController.konten:
                if j.kontenName == i.konto1:
                    if j.aktivKonto:
                        j.saldo += i.betrag
                    else:
                        j.saldo -= i.betrag
                    break

            for j in BuchhaltungsController.konten:
                if j.kontenName == i.konto2:
                    if j.aktivKonto:
                        j.saldo -= i.betrag
                    else:
                        j.saldo += i.betrag
                    break
        for i in BuchhaltungsController.konten:
            i.saldo = round(i.saldo * 100) / 100

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

    @staticmethod
    def addKonto(konto):
        BuchhaltungsController.konten.append(konto)
        BuchhaltungsController.saveKonten()

    @staticmethod
    def removeKonto(index):
        BuchhaltungsController.konten.pop(index)
        BuchhaltungsController.saveKonten()
