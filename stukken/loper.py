from stukken.stuk import Stuk
from globale_enums import StukType
from beweging.loperbeweging import LoperBeweging
from plaatjes.opzoeker import plaatjesOpzoeker

class Loper(Stuk):
    def __init__(self, kleur):
        super().__init__(StukType.Loper, kleur)
        self._plaatje = plaatjesOpzoeker[self.stuktype][self.kleur]

    def krijg_beweegopties_in_positie(self, positie):
        return LoperBeweging().krijg_beweegopties_in_positie(self, positie)

    def krijg_zicht_in_positie(self, positie):
        return LoperBeweging().krijg_zicht_in_positie(self, positie)