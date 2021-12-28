from stukken.stuk import Stuk
from globale_enums import Lineaire_Richtingen, StukType
import globale_variabelen

class Toren(Stuk):
    def __init__(self, kleur, veld):
        #geef de stukinformatie door aan de moederclass
        super().__init__(StukType.Toren, kleur, veld)
        self.Plaatje = globale_variabelen.plaatjes[self.stuktype][self.kleur]
        self.StelBeweegRichtingenIn()

    def StelBeweegRichtingenIn(self):
        self.BeweegRichtingen = [Lineaire_Richtingen.Boven,
                                 Lineaire_Richtingen.Onder,
                                 Lineaire_Richtingen.Links,
                                 Lineaire_Richtingen.Rechts]

    def krijg_veldopties(self):
        resultaat = []
        for beweegrichting in self.BeweegRichtingen:
            resultaat.extend(self.krijg_veldopties_in_richting(self.HuidigVeld.Coordinaat(), beweegrichting))
        return resultaat