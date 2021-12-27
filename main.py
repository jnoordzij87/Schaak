import pygame
import globale_enums
import globale_variabelen
from bord import Bord
import hulpfuncties
from startpositie import StartPositie

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
globale_variabelen.huidige_positie.teken_positie()

#hier gaan we de game-loop in
blijfDraaien = True
while blijfDraaien == True:

    #kijk elke keer of er een speciale gebeurtenis heeft plaatsgevonden
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            #als we hier zijn is er op het kruisje geklikt
            blijfDraaien = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            hulpfuncties.BehandelKlikGebeurtenis(event)


    #teken opnieuw alle elementen op het schaakbord
    for veld in globale_variabelen.velden.values():
        #teken het vakje
        veld.Teken(scherm)

        #teken het coordinaat
        font = pygame.font.Font('freesansbold.ttf', 16)
        text = font.render(veld.Kolom + veld.Rij, True, globale_enums.vakjeskleuren.groen.value)
        scherm.blit(text, (veld.PosX,veld.PosY))

        #teken de plaatjes van de stukken
        if veld.Stuk != None:
            stukplaatje = pygame.image.load(veld.Stuk.Plaatje)
            stukplaatje = pygame.transform.scale(stukplaatje, (stukplaatje.get_width() * 0.8, stukplaatje.get_height() * 0.8))
            scherm.blit(stukplaatje, (veld.PosX, veld.PosY))

    #teken als laatst de stukopties
    if globale_variabelen.geselecteerdeStukOpties != None:
        bord.TekenStukOpties(globale_variabelen.geselecteerdeStukOpties, scherm)

    #update het scherm
    pygame.display.flip()

#we komen hier alleen als we uit de game-loop zijn
pygame.quit()

