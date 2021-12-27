from stukken.stuk import Stuk
from globenums import Richtingen, StukType
import globvars

class Toren(Stuk):
    def __init__(self, kleur, veld):
        #geef de stukinformatie door aan de moederclass
        super().__init__(StukType.Toren, kleur, veld)
        self.Plaatje = globvars.plaatjes[self.StukType][self.Kleur]
        self.StelBeweegRichtingenIn()

    def StelBeweegRichtingenIn(self):
        self.BeweegRichtingen = [Richtingen.Boven,
                                 Richtingen.Onder,
                                 Richtingen.Links,
                                 Richtingen.Rechts]

    def KrijgVeldenWaarStukNaarToeKan(self):
        resultaat = []
        for beweegrichting in self.BeweegRichtingen:
            resultaat.extend(self.AlleVakjesInRichting(self.HuidigVeld.Coordinaat(), beweegrichting))
        return resultaat