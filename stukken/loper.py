from stukken.stuk import Stuk
from globale_enums import Lineaire_Richtingen, StukType
import globale_variabelen

class Loper(Stuk):
    def __init__(self, kleur, veld):
        #geef de stukinformatie door aan de moederclass
        super().__init__(StukType.Loper, kleur, veld)
        self.Plaatje = globale_variabelen.plaatjes[self.stuktype][self.kleur]
        self.StelBeweegRichtingenIn()

    def StelBeweegRichtingenIn(self):
        self.BeweegRichtingen = [Lineaire_Richtingen.RechtsOnder,
                                 Lineaire_Richtingen.RechtsBoven,
                                 Lineaire_Richtingen.LinksBoven,
                                 Lineaire_Richtingen.LinksOnder]

    def krijg_veldopties(self, veldbezetting : dict(str, Stuk)):
        resultaat = []
        for beweegrichting in self.BeweegRichtingen:
            resultaat.extend(self.krijg_veldopties_in_richting(self.HuidigVeld.Coordinaat(), beweegrichting))
        return resultaat