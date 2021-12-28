from stukken.stuk import Stuk
from globale_enums import StukType
from beweging.damebeweging import DameBeweging
from plaatjes.opzoeker import plaatjesOpzoeker

class Dame(Stuk):
    def __init__(self, kleur):
        super().__init__(StukType.Dame, kleur)
        self._plaatje = plaatjesOpzoeker[self.stuktype][self.kleur]
        self._bewegingstype = DameBeweging()

    def krijg_beweegopties_in_positie(self, positie):
        """Doorgeefluik naar bewegingsclass"""
        return self._bewegingstype.krijg_beweegopties_in_positie()