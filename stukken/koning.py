from stukken.stuk import Stuk
from globale_enums import Richtingen, StukType
import globale_variabelen

class Koning(Stuk):
    def __init__(self, kleur, veld):
        #geef de stukinformatie door aan de moederclass
        super().__init__(StukType.Koning, kleur, veld)
        self.Plaatje = globale_variabelen.plaatjes[self.stuktype][self.kleur]
        self.StelBeweegRichtingenIn()

    def StelBeweegRichtingenIn(self):
        self.BeweegRichtingen = [Richtingen.RechtsOnder,
                                 Richtingen.RechtsBoven,
                                 Richtingen.LinksBoven,
                                 Richtingen.LinksOnder,
                                 Richtingen.Boven,
                                 Richtingen.Onder,
                                 Richtingen.Links,
                                 Richtingen.Rechts]

    def KrijgVeldenWaarStukNaarToeKan(self):
        resultaat = []
        for beweegrichting in self.BeweegRichtingen:
            resultaat.extend(self.AlleVakjesInRichting(self.HuidigVeld.Coordinaat(), beweegrichting, maxaantal=1))
        return resultaat