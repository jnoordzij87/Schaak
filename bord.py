import pygame
import globenums
import globvars
from veld import Veld
from stukken.pion import Pion
from stukken.loper import Loper
from stukken.dame import Dame
from stukken.koning import Koning
from stukken.toren import Toren


class Bord:
    def __init__(self):
        self.Velden = {}
        pass

    def MaakBord(self, scherm, schermbreedte, schermhoogte):
        rijen = ['1', '2', '3', '4', '5', '6', '7', '8']
        kolommen = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        vakjesgrootte = schermbreedte / 8
        posX = 0
        posY = schermhoogte - vakjesgrootte
        beginKleurRij = globenums.vakjeskleuren.wit.value
        for rij in rijen:
            kleur = beginKleurRij
            for kolom in kolommen:
                # stel coordinaat samen
                coord = kolom + rij
                # maak vakje
                veld = Veld(rij, kolom, posX, posY, kleur, vakjesgrootte, self)
                veld.Teken(scherm)
                globvars.velden[coord] = veld # bewaar veld in dictionary zodat deze snel opzoekbaar is, bijv voor bij het stukopties tekenen
                posX += vakjesgrootte
                kleur = self.VeranderKleur(kleur)
            posY -= vakjesgrootte
            posX = 0
            beginKleurRij = self.VeranderKleur(beginKleurRij)



    def TekenStukOpties(self, coordinaten, scherm):
        """
        :param coordinaten: coordinaten
        :return:
        """
        for coord in coordinaten:
            veld = globvars.velden[coord]
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

    def VeranderKleur(self, huidigeKleur):
        if huidigeKleur == globenums.vakjeskleuren.wit.value:
            return globenums.vakjeskleuren.blauw.value
        if huidigeKleur == globenums.vakjeskleuren.blauw.value:
            return globenums.vakjeskleuren.wit.value

    def MaakStartOpstelling(self):
        for veld in globvars.velden.values():
            coord = veld.Coordinaat()
            stuk = None
            """
            
            if coord == 'B1' or coord == 'G1':
                veld.Stuk = stukken.Paard_Wit
            
            
            
            
            if coord == 'B8' or coord == 'G8':
                veld.Stuk = stukken.Paard_Zwart
            
            
            
            """
            if coord == 'A1' or coord == 'H1':
                stuk = Toren(globenums.StukKleur.Wit, veld)
            if coord == 'A8' or coord == 'H8':
                stuk = Toren(globenums.StukKleur.Zwart, veld)
            if coord == 'E1':
                stuk = Koning(globenums.StukKleur.Wit, veld)
            if coord == 'E8':
                stuk = Koning(globenums.StukKleur.Zwart, veld)
            if coord == 'D8':
                stuk = Dame(globenums.StukKleur.Zwart, veld)
            if coord == 'D1':
                stuk = Dame(globenums.StukKleur.Wit, veld)
            if coord == 'C1' or coord == 'F1':
                stuk = Loper(globenums.StukKleur.Wit, veld)
            if coord == 'C8' or coord == 'F8':
                stuk = Loper(globenums.StukKleur.Zwart, veld)
            if '2' in coord:
                stuk = Pion(globenums.StukKleur.Wit, veld)
            if '7' in coord:
                stuk = Pion(globenums.StukKleur.Zwart, veld)

            #voeg het stuk toe aan de stukkenlijst
            if stuk != None:
                globvars.stukken.append(stuk)
                veld.Stuk = stuk