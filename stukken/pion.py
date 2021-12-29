from stukken.stuk import Stuk
from globale_enums import StukType
from beweging.pionbeweging import PionBeweging
from plaatjes.opzoeker import plaatjesOpzoeker

class Pion(Stuk):
    def __init__(self, kleur):
        super().__init__(StukType.Pion, kleur)
        self._plaatje = plaatjesOpzoeker[self.stuktype][self.kleur]

    def krijg_beweegopties_in_positie(self, positie):
        """Doorgeefluik naar bewegingsclass"""
        return PionBeweging(self.kleur).krijg_beweegopties_in_positie(self, positie)