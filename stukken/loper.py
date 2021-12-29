from stukken.stuk import Stuk
from globale_enums import StukType
from beweging.loperbeweging import LoperBeweging
from plaatjes.opzoeker import plaatjesOpzoeker

class Loper(Stuk):
    def __init__(self, kleur):
        super().__init__(StukType.Loper, kleur)
        self._plaatje = plaatjesOpzoeker[self.stuktype][self.kleur]

    def krijg_beweegopties_in_positie(self, positie):
        """Doorgeefluik naar bewegingsclass"""
        return LoperBeweging().krijg_beweegopties_in_positie(self, positie)