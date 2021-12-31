import os
import pygame
import playsound
import globale_enums
import globale_variabelen
from ai.ai import AI
from bord.bord import Bord
from positie.startpositie import StartPositie
from muisklik.muisklik import Muisklik

def InitialiseerBord(scherm, schermbreedte, schermhoogte):
    # maak het bord
    bord = Bord()
    # maak startpositie en stel in als huidige positie
    globale_variabelen.huidige_positie = StartPositie(bord)
    # teken de velden van het bord op het scherm
    bord.teken_velden(scherm, schermbreedte, schermhoogte)
    bord.teken_coordinaten(scherm)
    # teken de stukken in de startpositie op het scherm
    globale_variabelen.huidige_positie.teken_positie(scherm)

def UpdateVisueleElementen(scherm, schermbreedte, schermhoogte):
    bord = globale_variabelen.huidige_positie.bord
    # teken opnieuw alle elementen op het schaakbord
    bord.teken_velden(scherm, schermbreedte, schermhoogte)
    bord.teken_coordinaten(scherm)
    globale_variabelen.huidige_positie.teken_positie(scherm)
    # teken als laatst de stukopties
    if globale_variabelen.geselecteerdeStuk != None:
        #krijg stuk opties
        stuk = globale_variabelen.geselecteerdeStuk
        positie = globale_variabelen.huidige_positie
        stuk_opties = stuk.krijg_beweegopties_in_positie(positie)
        bord.TekenStukOpties(stuk_opties, scherm)

def IsSelectieGewijzigd(huidige_selectie):
    return globale_variabelen.geselecteerdeStuk != huidige_selectie

def IsSpelerAanZetGewijzigd(speler_aan_zet):
    return speler_aan_zet != globale_variabelen.huidige_positie.speler_aan_zet

def CheckPygameGebeurtenissen():
    # kijk elke keer of er een speciale gebeurtenis heeft plaatsgevonden
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # als we hier zijn is er op het kruisje geklikt
            return False
        if event.type == pygame.MOUSEBUTTONDOWN:
            # als we hier zijn is er in het scherm geklikt
            Muisklik().BehandelKlikGebeurtenis(event)
    return True

def BehandelSpelerAanZetVeranderd():
    if globale_variabelen.schaakmat == True:
        return
    huidigeSpeler = globale_variabelen.huidige_positie.speler_aan_zet
    if huidigeSpeler == globale_enums.Spelers.zwart:
        DoeEenWillekeurigeZet(huidigeSpeler)

def DoeEenWillekeurigeZet(speler):
    AI().doe_random_geldige_zet(speler)

def BehandelSchaakmat():
    globale_variabelen.schaakmat = True
    abspath = os.path.abspath('geluiden/Tada-sound.mp3')
    playsound.playsound(abspath)