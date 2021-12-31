class Buchung:
    def __init__(self, konto1, konto2, date, beschreibung, betrag):
        self.konto1 = konto1
        self.konto2 = konto2
        self.data = date
        self.beschreibung = beschreibung
        self.betrag = betrag