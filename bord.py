import pygame
import globale_enums
import globale_variabelen
from veld import Veld
from getekendveld import GetekendVeld
from veldbasis import VeldBasis
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
        for rij in self._rijen:
            beginkleur_rij = globale_enums.vakjeskleuren.wit.value
            for kolom in self._kolommen:
                kleur = beginkleur_rij
                # stel coordinaat samen (bijv 'A1')
                coordinaat = kolom + rij
                veld = VeldBasis(coordinaat, kleur)
                self._velden.append(veld) #voeg veld toe aan lijst
                kleur = self._verander_van_kleur(kleur) #verander van kleur voor het volgende vakje
            beginKleurRij = self._verander_van_kleur(beginKleurRij) #begin de volgende rij met een andere beginkleur


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



    def MaakBord(self, scherm, schermbreedte, schermhoogte):
        rijen = ['1', '2', '3', '4', '5', '6', '7', '8']
        kolommen = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        vakjesgrootte = schermbreedte / 8
        posX = 0
        posY = schermhoogte - vakjesgrootte
        beginKleurRij = globale_enums.vakjeskleuren.wit.value
        for rij in rijen:
            kleur = beginKleurRij
            for kolom in kolommen:
                # stel coordinaat samen
                coord = kolom + rij
                # maak vakje
                veld = Veld(rij, kolom, posX, posY, kleur, vakjesgrootte, self)
                veld.Teken(scherm)
                globale_variabelen.velden[coord] = veld # bewaar veld in dictionary zodat deze snel opzoekbaar is, bijv voor bij het stukopties tekenen
                posX += vakjesgrootte
                kleur = self._verander_van_kleur(kleur)
            posY -= vakjesgrootte
            posX = 0
            beginKleurRij = self._verander_van_kleur(beginKleurRij)



    def TekenStukOpties(self, coordinaten, scherm):
        """
        :param coordinaten: coordinaten
        :return:
        """
        for coord in coordinaten:
            veld = globale_variabelen.velden[coord]
            #krijg het middelpunt van het veld
            middelpunt = veld.MiddelPunt()
            mpX = middelpunt[0]
            mpY = middelpunt[1]
            #teken iets
            try:
                pygame.draw.rect(scherm, (255, 0, 0), (mpX, mpY, 10, 10))
            except Exception as e:
                print(e)
        pass

    def _verander_van_kleur(self, huidigeKleur):
        if huidigeKleur == globale_enums.vakjeskleuren.wit.value:
            return globale_enums.vakjeskleuren.blauw.value
        if huidigeKleur == globale_enums.vakjeskleuren.blauw.value:
            return globale_enums.vakjeskleuren.wit.value

    def MaakStartOpstelling(self):
        for veld in globale_variabelen.velden.values():
            coord = veld.Coordinaat()
            stuk = None
            """
            if coord == 'B1' or coord == 'G1':
                veld.Stuk = stukken.Paard_Wit
            if coord == 'B8' or coord == 'G8':
                veld.Stuk = stukken.Paard_Zwart
            """
            if coord == 'A1' or coord == 'H1':
                stuk = Toren(globale_enums.StukKleur.Wit, veld)
            if coord == 'A8' or coord == 'H8':
                stuk = Toren(globale_enums.StukKleur.Zwart, veld)
            if coord == 'E1':
                stuk = Koning(globale_enums.StukKleur.Wit, veld)
            if coord == 'E8':
                stuk = Koning(globale_enums.StukKleur.Zwart, veld)
            if coord == 'D8':
                stuk = Dame(globale_enums.StukKleur.Zwart, veld)
            if coord == 'D1':
                stuk = Dame(globale_enums.StukKleur.Wit, veld)
            if coord == 'C1' or coord == 'F1':
                stuk = Loper(globale_enums.StukKleur.Wit, veld)
            if coord == 'C8' or coord == 'F8':
                stuk = Loper(globale_enums.StukKleur.Zwart, veld)
            if '2' in coord:
                stuk = Pion(globale_enums.StukKleur.Wit, veld)
            if '7' in coord:
                stuk = Pion(globale_enums.StukKleur.Zwart, veld)

            #voeg het stuk toe aan de stukkenlijst
            if stuk != None:
                globale_variabelen.stukken.append(stuk)
                veld.Stuk = stuk