from stukken.stuk import Stuk
from globale_enums import StukType
from beweging.torenbeweging import TorenBeweging
from plaatjes.opzoeker import plaatjesOpzoeker

class Toren(Stuk):
    def __init__(self, kleur):
        super().__init__(StukType.Toren, kleur)
        self._plaatje = plaatjesOpzoeker[self.stuktype][self.kleur]

    def krijg_beweegopties_in_positie(self, positie):
        return TorenBeweging().krijg_beweegopties_in_positie(self, positie)

    def krijg_zicht_in_positie(self, positie):
        return TorenBeweging().krijg_zicht_in_positie(self, positie)