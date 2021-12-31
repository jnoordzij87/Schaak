from .lineaire_beweging import LineaireBeweging
from globale_enums import Lineaire_Richtingen
from zet.zet import Zet
import copy

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
        #bij een koning moet van de zichtvelden bekeken worden of ze niet tot schaak leiden
        beweegopties = []
        zichtvelden = self.krijg_zicht_in_positie(stuk, positie)
        huidig_veld = positie.krijg_veld_van_stuk(stuk)
        for zichtveld in zichtvelden:
            if Zet(stuk, zichtveld, positie).is_zet_geldig():
                beweegopties.append(zichtveld)
            #hypo_positie = copy.deepcopy(positie)
            #hypo_positie_koning = hypo_positie.veldbezetting[huidig_veld] #is door deepcopy niet hetzelfde object
            #hypo_positie.verplaats_hypothetisch(hypo_positie_koning, huidig_veld, zichtveld)
            #is_positie_geldig = hypo_positie.is_positie_geldig()
            #if is_positie_geldig:
            #    beweegopties.append[zichtveld]
        return beweegopties

    def krijg_zicht_in_positie(self, stuk, positie):
        #Wordt overschreven voor de koning omdat de koning maar 1 stap kan nemen
        resultaat = []
        for richting in self.bewegingsrichtingen:
            opties_in_richting = self.krijg_zicht_voor_stuk_in_richting(stuk, richting, positie, maxaantal=1)
            resultaat.extend(opties_in_richting)
        return resultaat

