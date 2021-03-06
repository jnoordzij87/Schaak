from stukken.stuk import Stuk
from globale_enums import StukType
from beweging.damebeweging import DameBeweging
from plaatjes.opzoeker import plaatjesOpzoeker

class Dame(Stuk):
    def __init__(self, kleur):
        super().__init__(StukType.Dame, kleur)
        self._plaatje = plaatjesOpzoeker[self.stuktype][self.kleur]

    def krijg_beweegopties_in_positie(self, positie):
        return DameBeweging().krijg_beweegopties_in_positie(self, positie)

    def krijg_zicht_in_positie(self, positie):
        return DameBeweging().krijg_zicht_in_positie(self, positie)