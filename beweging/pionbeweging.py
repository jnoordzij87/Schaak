from .lineaire_beweging import LineaireBeweging
from globale_enums import Lineaire_Richtingen, StukKleur

class PionBeweging(LineaireBeweging):
    """De essentie van een beweging-class is de functie krijg_beweegopties_in_positie"""
    def __init__(self, pionkleur):
        self._basisrichting = self._krijg_basisrichting(pionkleur)
        super().__init__()
        pass

    @property
    def basisrichting(self):
        """De voorwaartse richting van de pion"""
        return self._basisrichting

    def krijg_zicht_in_positie(self, stuk, positie):
        resultaat = []
        voorwaartse_opties = self.krijg_voorwaartse_opties(stuk, positie)
        pakopties = self.krijg_pakopties(stuk, positie)
        resultaat.extend(voorwaartse_opties)
        resultaat.extend(pakopties)
        return resultaat

    def _krijg_basisrichting(self, kleur):
        if kleur == StukKleur.Wit:
            basisrichting = Lineaire_Richtingen.Boven
        if kleur == StukKleur.Zwart:
            basisrichting = Lineaire_Richtingen.Onder
        return basisrichting

    def krijg_voorwaartse_opties(self, stuk, positie):
        if not stuk.heeft_al_eens_bewogen:
            voorwaartse_opties = self.krijg_zicht_voor_stuk_in_richting(
                stuk, self._basisrichting, positie, maxaantal = 2)
        else:
            voorwaartse_opties = self.krijg_zicht_voor_stuk_in_richting(
                stuk, self._basisrichting, positie, maxaantal = 1)
        #check of er geen stuk op het voorwaartse veld staat (pionnen slaan niet voorwaarts)
        geldige_opties = []
        for optie in voorwaartse_opties:
            if not positie.staat_er_een_stuk_op_dit_veld(optie):
                geldige_opties.append(optie)
        return geldige_opties

    def krijg_pakopties(self, stuk, positie):
        resultaat = []
        huidige_coord = positie.krijg_veld_van_stuk(stuk)
        for richting in self.krijg_pakrichtingen():
            eerstvolgende_vakje = self.krijg_eerstvolgende_vakje_in_richting(positie, huidige_coord, richting)
            if eerstvolgende_vakje != None:
                if positie.staat_er_een_stuk_op_dit_veld(eerstvolgende_vakje):
                    #het is een pakoptie als het een stuk van de tegenstander is
                    if positie.krijg_stuk_op_veld(eerstvolgende_vakje).kleur != stuk.kleur:
                        resultaat.append(eerstvolgende_vakje)
        return resultaat

    def krijg_pakrichtingen(self):
        if self._basisrichting == Lineaire_Richtingen.Boven:
            pakrichtingen = [
                Lineaire_Richtingen.LinksBoven,
                Lineaire_Richtingen.RechtsBoven]
        if self._basisrichting == Lineaire_Richtingen.Onder:
            pakrichtingen = [
                Lineaire_Richtingen.LinksOnder,
                Lineaire_Richtingen.RechtsOnder]
        return pakrichtingen





