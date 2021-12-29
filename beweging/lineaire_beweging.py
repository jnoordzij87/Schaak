from .beweging import Beweging
from globale_enums import Lineaire_Richtingen


class LineaireBeweging(Beweging):
    def __init__(self):
        super().__init__()
        pass

    def krijg_zicht_in_positie(self, stuk, positie):
        resultaat = []
        for richting in self.bewegingsrichtingen:
            opties_in_richting = self.krijg_zicht_voor_stuk_in_richting(stuk, richting, positie, maxaantal=None)
            resultaat.extend(opties_in_richting)
        return resultaat

    def krijg_zicht_voor_stuk_in_richting(self, stuk, richting, positie, maxaantal = None):
        """
        :return: een lijst met coordinaten in 1 richting, bijv ['E4', 'F4', 'G4', etc]
        """
        # aanpak: zolang we geen ongeldig vakje tegenkomen, bijv omdat we op rand van bord zijn gekomen
        # ga dan steeds door naar het volgende vakje in dezelfde richting
        resultaat = []
        teller = 0
        stuk_coord = positie.krijg_veld_van_stuk(stuk)
        eerstvolgende_vakje = self.krijg_eerstvolgende_vakje_in_richting(positie, stuk_coord, richting)
        is_geldige_optie = self._is_veld_geldig_en_niet_bezet(stuk, eerstvolgende_vakje, positie)
        while is_geldige_optie and teller != maxaantal:  # stop als dit niet waar is
            # als we hier zijn is het volgende vakje geldig, voeg toe aan lijst
            resultaat.append(eerstvolgende_vakje)
            # als er een stuk van een andere kleur op het zojuist toegevoegde vakje staat, dan is dit het laatste vakje in deze richting, check
            if self._staat_er_een_stuk_van_andere_kleur_op_veld(stuk, eerstvolgende_vakje, positie):
                break  # stap uit de loop
            # als we hier zijn, kijk naar het volgende vakje, en ga door
            eerstvolgende_vakje = self.krijg_eerstvolgende_vakje_in_richting(positie, eerstvolgende_vakje, richting)
            is_geldige_optie = self._is_veld_geldig_en_niet_bezet(stuk, eerstvolgende_vakje, positie)
            teller += 1
        # als uit loop: geef resultaat terug
        return resultaat

    def krijg_eerstvolgende_vakje_in_richting(self, positie, coordinaat, richting):
        kolom = coordinaat[0]
        rij = int(coordinaat[1])
        if richting == Lineaire_Richtingen.Links:
            kolom = positie.bord.KolomLinks(kolom)
        if richting == Lineaire_Richtingen.Rechts:
            kolom = positie.bord.KolomRechts(kolom)
        if richting == Lineaire_Richtingen.Boven:
            rij = positie.bord.RijOmhoog(rij)
        if richting == Lineaire_Richtingen.Onder:
            rij = positie.bord.RijOmlaag(rij)
        if richting == Lineaire_Richtingen.LinksBoven:
            kolom = positie.bord.KolomLinks(kolom)
            rij = positie.bord.RijOmhoog(rij)
        if richting == Lineaire_Richtingen.LinksOnder:
            kolom = positie.bord.KolomLinks(kolom)
            rij = positie.bord.RijOmlaag(rij)
        if richting == Lineaire_Richtingen.RechtsBoven:
            kolom = positie.bord.KolomRechts(kolom)
            rij = positie.bord.RijOmhoog(rij)
        if richting == Lineaire_Richtingen.RechtsOnder:
            kolom = positie.bord.KolomRechts(kolom)
            rij = positie.bord.RijOmlaag(rij)
        # als volgende veld ongeldig is: geef niks terug
        if kolom == None or rij == None:
            return None
        #als we hier zijn hebben we een geldige coordinaat
        eerstvolgendevakje = kolom + str(rij)
        return eerstvolgendevakje
