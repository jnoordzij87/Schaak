from lineaire_beweging import LineaireBeweging
from globale_enums import Lineaire_Richtingen

class KoningBeweging(LineaireBeweging):
    def __init__(self):
        super().__init__()
        pass

    @property
    def bewegingsrichtingen(self):
        richtingen = [
            Lineaire_Richtingen.RechtsOnder,
            Lineaire_Richtingen.RechtsBoven,
            Lineaire_Richtingen.LinksBoven,
            Lineaire_Richtingen.LinksOnder,
            Lineaire_Richtingen.Boven,
            Lineaire_Richtingen.Onder,
            Lineaire_Richtingen.Links,
            Lineaire_Richtingen.Rechts]
        return richtingen

    def krijg_beweegopties_in_positie(self, stuk, positie):
        resultaat = []
        for richting in self.bewegingsrichtingen:
            opties_in_richting = self.krijg_beweegopties_voor_stuk_in_richting(
                stuk, richting, positie, maxaantal=1)
            resultaat.extend(opties_in_richting)
        return resultaat

