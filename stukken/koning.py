from stukken.stuk import Stuk
from globale_enums import StukType
from beweging.koningbeweging import KoningBeweging
from plaatjes.opzoeker import plaatjesOpzoeker

class Koning(Stuk):
    def __init__(self, kleur):
        super().__init__(StukType.Koning, kleur)
        self._plaatje = plaatjesOpzoeker[self.stuktype][self.kleur]

    def krijg_beweegopties_in_positie(self, positie):
        return KoningBeweging().krijg_beweegopties_in_positie(self, positie)

    def krijg_zicht_in_positie(self, positie):
        return KoningBeweging().krijg_zicht_in_positie(self, positie)