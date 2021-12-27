from stukken.stuk import Stuk
from plaatjes.opzoeker import plaatjesOpzoeker
from globale_enums import StukKleur, Richtingen, StukType

class Pion(Stuk):
    def __init__(self, kleur, veld):
        #geef de stukinformatie door aan de moederclass
        super().__init__(StukType.Pion, kleur, veld)
        self.Plaatje = plaatjesOpzoeker[self.stuktype][self.kleur]
        self.StelBeweegRichtingenIn()

    def StelBeweegRichtingenIn(self):
        # stel in welke richting de pion op kan lopen
        if self.kleur == StukKleur.Wit:
            self.BeweegRichtingen = [Richtingen.Boven]  # afspraak: een witte pion loopt omhoog
        if self.kleur == StukKleur.Zwart:
            self.BeweegRichtingen = [Richtingen.Onder]  # afspraak: een zwarte pion loopt omlaag

    def KrijgVeldenWaarStukNaarToeKan(self):
        resultaat = []
        for beweegrichting in self.BeweegRichtingen:
            if not self.heeft_al_eens_bewogen:
                resultaat = self.AlleVakjesInRichting(self.HuidigVeld.Coordinaat(), beweegrichting, maxaantal=2)
            else:
                resultaat = self.AlleVakjesInRichting(self.HuidigVeld.Coordinaat(), beweegrichting, maxaantal=1)
        return resultaat