from enum import Enum

import globale_enums
import hulpfuncties
from globale_enums import Richtingen

class Stuk:
    def __init__(self, stuktype, stukkleur, veld):
        self.StukType = stuktype
        self.HuidigVeld = veld
        self.Kleur = stukkleur
        self.HeeftAlEensBewogen = False

    def VanWelkeSpelerIsDitStuk(self):
        if self.Kleur == globale_enums.StukKleur.Wit:
            return globale_enums.Spelers.Wit
        if self.Kleur == globale_enums.StukKleur.Zwart:
            return globale_enums.Spelers.Zwart

    def ZetNieuwVeld(self, veld):
        self.HuidigVeld = veld
        self.HuidigCoordinaat = veld.Coordinaat()
        self.HeeftAlEensBewogen = True

    def KrijgVeldenWaarStukNaarToeKan(self):
        #overschrijf deze functie in de ervende class!
        pass

    def AlleVakjesInRichting(self, coordinaat, richting, maxaantal = None):
        """
        :return: een lijst met coordinaten in 1 richting, bijv ['E4', 'F4', 'G4', etc]
        """
        resultaat = []  # een lijst
        # aanpak:
        # zolang we geen ongeldig vakje tegenkomen
        # bijv omdat we op rand van bord zijn gekomen
        # ga dan steeds door naar het volgende vakje in dezelfde richting
        teller = 0
        volgendeVakje = self.EerstVolgendeVakjeInRichting(coordinaat, richting)
        while volgendeVakje != None and teller != maxaantal:  # deze loop stopt als het volgende vakje ongeldig is
            # het volgende vakje is geldig, voeg toe aan lijst
            resultaat.append(volgendeVakje)
            teller += 1
            # als er een stuk van een andere kleur op dit vakje staat, is dit het laatste vakje in deze richting
            if self.StaatErEenStukVanAndereKleurOpVeld(volgendeVakje):
                break #stap uit de loop
            # als we hier zijn, kijk naar het volgende vakje en blijf doorgaan
            volgendeVakje = self.EerstVolgendeVakjeInRichting(volgendeVakje, richting)
        # als we hier zijn, zijn we uit de loop: geef het resultaat terug
        return resultaat

    def StaatErEenStukVanZelfdeKleurOpVeld(self, coordinaat):
        if hulpfuncties.StaatErEenStukOpVeld(coordinaat):
            #er staat een stuk op het veld, kijk of het van dezelfde kleur is
            stukopveld = hulpfuncties.KrijgStukOpVeld(coordinaat)
            if stukopveld.Kleur == self.Kleur:
                #het stuk heeft dezelfde kleur
                return True
        else:
            #er staat geen stuk op het veld
            return False

    def StaatErEenStukVanAndereKleurOpVeld(self, coordinaat):
        if hulpfuncties.StaatErEenStukOpVeld(coordinaat):
            #er staat een stuk op het veld, kijk of het van dezelfde kleur is
            stukopveld = hulpfuncties.KrijgStukOpVeld(coordinaat)
            if stukopveld.Kleur == self.Kleur:
                #het stuk heeft dezelfde kleur
                return False
            else:
                #het stuk heeft een andere kleur
                return True
        else:
            #er staat geen stuk op het veld
            return False

    def EerstVolgendeVakjeInRichting(self, coordinaat, richting):
        kolom = coordinaat[0]
        rij = int(coordinaat[1])
        if richting == Richtingen.Links:
            kolom = self.KolomLinks(kolom)
        if richting == Richtingen.Rechts:
            kolom = self.KolomRechts(kolom)
        if richting == Richtingen.Boven:
            rij = self.RijOmhoog(rij)
        if richting == Richtingen.Onder:
            rij = self.RijOmlaag(rij)
        if richting == Richtingen.LinksBoven:
            kolom = self.KolomLinks(kolom)
            rij = self.RijOmhoog(rij)
        if richting == Richtingen.LinksOnder:
            kolom = self.KolomLinks(kolom)
            rij = self.RijOmlaag(rij)
        if richting == Richtingen.RechtsBoven:
            kolom = self.KolomRechts(kolom)
            rij = self.RijOmhoog(rij)
        if richting == Richtingen.RechtsOnder:
            kolom = self.KolomRechts(kolom)
            rij = self.RijOmlaag(rij)
        # als volgende veld ongeldig is: geef niks terug
        if kolom == None or rij == None:
            return None
        #als we hier zijn hebben we een geldige coordinaat
        eerstvolgendevakje = kolom + str(rij)
        #als volgende veld bezet is door eigen stuk: geef niks terug
        if hulpfuncties.StaatErEenStukOpVeld(eerstvolgendevakje):
            #er staat een stuk op het veld, kijk of het van dezelfde kleur is
            stukopvakje = hulpfuncties.KrijgStukOpVeld(eerstvolgendevakje)
            if stukopvakje.Kleur == self.Kleur:
                #het stuk heeft dezelfde kleur, het veld is niet beschikbaar
                return None
        #als we hier zijn is het vakje geldig, geef terug
        return eerstvolgendevakje

    def RijOmhoog(self, rijnummer):
        if rijnummer == 8:
            # kan niet verder omhoog, we zitten op de rand van het bord
            # geef niets terug
            return None
        else:
            return rijnummer + 1

    def RijOmlaag(self, rijnummer):
        if rijnummer == 1:
            # kan niet verder omlaag, we zitten op de rand van het bord
            # geef niets terug
            return None
        else:
            return rijnummer - 1



    def KolomLinks(self, letter):
        kolomnummer = self.GetalVanLetterInAlfabet(letter)
        if kolomnummer == 1:
            # kan niet verder naar links, we zitten op de rand van het bord
            # geef niets terug
            return None
        nieuwekolomNummer = kolomnummer - 1
        nieuwekolomLetter = self.LetterInAlfabetVanGetal(nieuwekolomNummer)
        return nieuwekolomLetter

    def KolomRechts(self, letter):
        kolomnummer = self.GetalVanLetterInAlfabet(letter)
        if kolomnummer == 8:
            # kan niet verder naar rechts, we zitten op de rand van het bord
            # geef niets terug
            return None
        nieuwekolomNummer = kolomnummer + 1
        nieuwekolomLetter = self.LetterInAlfabetVanGetal(nieuwekolomNummer)
        return nieuwekolomLetter

    def GetalVanLetterInAlfabet(self, letter):
        alfabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        positie = alfabet.find(letter)
        return positie + 1  # wij willen beginnen te tellen bij 1

    def LetterInAlfabetVanGetal(self, getal):
        alfabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        getal = getal - 1  # python begint te tellen bij 0, wij beginnen bij 1, dus verander naar 1 minder
        letter = alfabet[getal]
        return letter