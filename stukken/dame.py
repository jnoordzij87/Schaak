from stukken.stuk import Stuk
from globale_enums import Lineaire_Richtingen, StukType
import globale_variabelen

class Dame(Stuk):
    def __init__(self, kleur, veld):
        #geef de stukinformatie door aan de moederclass
        super().__init__(StukType.Dame, kleur, veld)
        self.Plaatje = globale_variabelen.plaatjes[self.stuktype][self.kleur]
        self.StelBeweegRichtingenIn()

    def StelBeweegRichtingenIn(self):
        self.BeweegRichtingen = [Lineaire_Richtingen.RechtsOnder,
                                 Lineaire_Richtingen.RechtsBoven,
                                 Lineaire_Richtingen.LinksBoven,
                                 Lineaire_Richtingen.LinksOnder,
                                 Lineaire_Richtingen.Boven,
                                 Lineaire_Richtingen.Onder,
                                 Lineaire_Richtingen.Links,
                                 Lineaire_Richtingen.Rechts]

    def krijg_veldopties(self):
        resultaat = []
        for beweegrichting in self.BeweegRichtingen:
            huidige_veld = globale_variabelen.huidige_positie.krijg_veld_van_stuk() #mag dit niet in class?
            beschikbare_velden = self.krijg_veldopties_in_richting(self.HuidigVeld.Coordinaat(), beweegrichting)
            resultaat.extend()
        return resultaat