from stukken.stuk import Stuk
from plaatjes.opzoeker import plaatjesOpzoeker
from globale_enums import StukKleur, Lineaire_Richtingen, StukType

class Pion(Stuk):
    def __init__(self, kleur, veld):
        #geef de stukinformatie door aan de moederclass
        super().__init__(StukType.Pion, kleur, veld)
        self.Plaatje = plaatjesOpzoeker[self.stuktype][self.kleur]
        self.StelBeweegRichtingenIn()

    def StelBeweegRichtingenIn(self):
        # stel in welke richting de pion op kan lopen
        if self.kleur == StukKleur.Wit:
            self.BeweegRichtingen = [Lineaire_Richtingen.Boven]  # afspraak: een witte pion loopt omhoog
        if self.kleur == StukKleur.Zwart:
            self.BeweegRichtingen = [Lineaire_Richtingen.Onder]  # afspraak: een zwarte pion loopt omlaag

    def krijg_veldopties(self):
        resultaat = []
        for beweegrichting in self.BeweegRichtingen:
            if not self.heeft_al_eens_bewogen:
                resultaat = self.krijg_veldopties_in_richting(self.HuidigVeld.Coordinaat(), beweegrichting, maxaantal=2)
            else:
                resultaat = self.krijg_veldopties_in_richting(self.HuidigVeld.Coordinaat(), beweegrichting, maxaantal=1)
        return resultaat