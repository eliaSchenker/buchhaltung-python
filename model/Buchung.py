import datetime
import time


class Buchung:
    def __init__(self, konto1, konto2, date, beschreibung, betrag):
        self.konto1 = konto1
        self.konto2 = konto2
        self.date = date
        self.beschreibung = beschreibung
        self.betrag = betrag

    def getStringValuesArray(self):
        return [self.konto1, self.konto2, self.date.strftime("%d.%m.%Y"), self.beschreibung, str(self.betrag)]