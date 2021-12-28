from beweging import Beweging
from globale_enums import Lineaire_Richtingen


class LineaireBeweging(Beweging):
    def __init__(self, richtingen):
        super().__init__()
        pass

    def krijg_beweegopties_voor_stuk_in_richting(self, stuk, richting, positie, maxaantal = None):
        """
        :return: een lijst met coordinaten in 1 richting, bijv ['E4', 'F4', 'G4', etc]
        """
        # aanpak: zolang we geen ongeldig vakje tegenkomen, bijv omdat we op rand van bord zijn gekomen
        # ga dan steeds door naar het volgende vakje in dezelfde richting
        resultaat = []
        teller = 0
        stuk_coord = positie.krijg_veld_van_stuk(stuk)
        eerstvolgende_vakje = self.krijg_eerstvolgende_vakje_in_richting(stuk, stuk_coord, richting)
        is_geldige_optie = positie._is_veld_geldige_optie_voor_stuk(stuk, eerstvolgende_vakje)
        while is_geldige_optie and teller != maxaantal:  # stop als dit niet waar is
            # als we hier zijn is het volgende vakje geldig, voeg toe aan lijst
            resultaat.append(eerstvolgende_vakje)
            # als er een stuk van een andere kleur op het zojuist toegevoegde vakje staat, dan is dit het laatste vakje in deze richting, check
            if positie._staat_er_een_stuk_van_andere_kleur_op_veld(stuk, eerstvolgende_vakje):
                break  # stap uit de loop
            # als we hier zijn, kijk naar het volgende vakje, en ga door
            eerstvolgende_vakje = positie.krijg_eerstvolgende_vakje_in_richting(eerstvolgende_vakje, richting)
            is_geldige_optie = positie._is_veld_geldige_optie_voor_stuk(stuk, eerstvolgende_vakje)
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