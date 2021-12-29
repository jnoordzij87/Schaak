import pygame
import globale_enums
import globale_variabelen
from bord.bord import Bord
import hulpfuncties
from positie.startpositie import StartPositie

pygame.init()

schermbreedte = 400
schermhoogte = 400

scherm = pygame.display.set_mode((schermbreedte, schermhoogte))
pygame.display.set_caption('Schaak')

#maak het bord
bord = Bord()
#maak startpositie en stel in als huidige positie
globale_variabelen.huidige_positie = StartPositie(bord)

#teken de velden van het bord op het scherm
bord.teken_velden(scherm, schermbreedte, schermhoogte)
#teken de stukken in de startpositie op het scherm
globale_variabelen.huidige_positie.teken_positie(scherm)

#hier gaan we de game-loop in
blijfDraaien = True
speler_aan_zet = globale_variabelen.huidige_positie.speler_aan_zet
while blijfDraaien == True:

    #kijk elke keer of er een speciale gebeurtenis heeft plaatsgevonden
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            #als we hier zijn is er op het kruisje geklikt
            blijfDraaien = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            hulpfuncties.BehandelKlikGebeurtenis(event)

    #check of speler aan zet is gewijzigd
    if speler_aan_zet != globale_variabelen.huidige_positie.speler_aan_zet:
        #verwerk wijziging
        speler_aan_zet = globale_variabelen.huidige_positie.speler_aan_zet
        hulpfuncties.BehandelSpelerAanZetVeranderd()

    #teken opnieuw alle elementen op het schaakbord
    if globale_variabelen.moet_bord_bijgewerkt_worden:
        bord.teken_velden(scherm, schermbreedte, schermhoogte)
        bord.teken_coordinaten(scherm)
        globale_variabelen.huidige_positie.teken_positie(scherm)
        #teken als laatst de stukopties
        if globale_variabelen.geselecteerdeStukOpties != None:
            bord.TekenStukOpties(globale_variabelen.geselecteerdeStukOpties, scherm)
        #bord is bijgewerkt
        globale_variabelen.moet_bord_bijgewerkt_worden = False

    #update het scherm
    pygame.display.flip()


#we komen hier alleen als we uit de game-loop zijn
pygame.quit()

