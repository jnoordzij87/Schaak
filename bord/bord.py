import pygame
import globale_enums
import globale_variabelen
from veld.getekendveld import GetekendVeld
from veld.veldbasis import VeldBasis
from stukken.pion import Pion
from stukken.loper import Loper
from stukken.dame import Dame
from stukken.koning import Koning
from stukken.toren import Toren


class Bord:
    def __init__(self):
        self._rijen = ['1', '2', '3', '4', '5', '6', '7', '8']
        self._kolommen = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        self._maak_velden()
        pass

    @property
    def velden(self) -> list(VeldBasis):
        """Lijst met alle velden van het bord"""
        return self._velden

    @property
    def getekende_velden(self) -> dict(str, GetekendVeld):
        """Dictionary met alle getekende veldvormen, geindexeerd per coordinaat"""
        return self._getekende_velden

    def _maak_velden(self):
        """Maakt 64 velden met coordinaten en kleuren en slaat deze op in een lijst"""
        self._velden = [] #maak lege lijst
        beginkleur_rij = globale_enums.vakjeskleuren.wit.value
        for rij in self._rijen:
            kleur_kolom = beginkleur_rij
            for kolom in self._kolommen:
                # stel coordinaat samen (bijv 'A1')
                coordinaat = kolom + rij
                veld = VeldBasis(coordinaat, kleur_kolom)
                self._velden.append(veld) #voeg veld toe aan lijst
                kleur_kolom = self._verander_van_kleur(kleur_kolom) #verander van kleur voor het volgende vakje
            beginkleur_rij = self._verander_van_kleur(beginkleur_rij) #begin de volgende rij met een andere beginkleur


    def teken_velden(self, scherm, schermbreedte, schermhoogte):
        """Tekent de velden van het bord op het scherm en slaat op in lijst"""
        self._getekende_velden = {}
        vakjesgrootte = schermbreedte / 8
        #teken de velden per rij, van links naar rechts, van beneden naar boven
        #om de vorm te tekenen hebben we een xy positie op het scherm nodig
        #dit is de linkerbovenhoek van het vakje
        positie_x = 0  # linkerkant van het scherm
        positie_y = schermhoogte - vakjesgrootte  # bovenkant van de onderste rij
        teller = 0
        for rij in self._rijen:
            for kolom in self._kolommen:
                veld = self.velden[teller]
                coord = veld.coordinaat
                getekend_veld = GetekendVeld(scherm, positie_x, positie_y, vakjesgrootte)
                self.getekende_velden[coord] = getekend_veld
                teller = teller + 1

    def TekenStukOpties(self, coordinaten, scherm):
        """
        :param coordinaten: coordinaten
        :return:
        """
        for coord in coordinaten:
            veld = self.getekende_velden[coord]
            #krijg het middelpunt van het veld
            middelpunt = veld.middelpunt
            mpX = middelpunt[0]
            mpY = middelpunt[1]
            #teken iets
            pygame.draw.rect(scherm, (255, 0, 0), (mpX, mpY, 10, 10))

    def _verander_van_kleur(self, huidigeKleur):
        if huidigeKleur == globale_enums.vakjeskleuren.wit.value:
            return globale_enums.vakjeskleuren.blauw.value
        if huidigeKleur == globale_enums.vakjeskleuren.blauw.value:
            return globale_enums.vakjeskleuren.wit.value

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