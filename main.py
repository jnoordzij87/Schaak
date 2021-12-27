import pygame
import globenums
import globvars
from bord import Bord
import hulpfuncties

pygame.init()

schermbreedte = 400
schermhoogte = 400

scherm = pygame.display.set_mode((schermbreedte, schermhoogte))
pygame.display.set_caption('Schaak')

bord = Bord()
bord.MaakBord(scherm, schermbreedte, schermhoogte)
bord.MaakStartOpstelling()

#hier gaan we de game-loop in
blijfDraaien = True
while blijfDraaien == True:

    #kijk elke keer of er een speciale gebeurtenis heeft plaatsgevonden
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            #afsluitgebeurtenis
            blijfDraaien = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            hulpfuncties.BehandelKlikGebeurtenis(event)


    #teken opnieuw alle elementen op het schaakbord
    for veld in globvars.velden.values():
        #teken het vakje
        veld.Teken(scherm)

        #teken het coordinaat
        font = pygame.font.Font('freesansbold.ttf', 16)
        text = font.render(veld.Kolom + veld.Rij, True, globenums.vakjeskleuren.groen.value)
        scherm.blit(text, (veld.PosX,veld.PosY))

        #teken de plaatjes van de stukken
        if veld.Stuk != None:
            stukplaatje = pygame.image.load(veld.Stuk.Plaatje)
            stukplaatje = pygame.transform.scale(stukplaatje, (stukplaatje.get_width() * 0.8, stukplaatje.get_height() * 0.8))
            scherm.blit(stukplaatje, (veld.PosX, veld.PosY))

    #teken als laatst de stukopties
    if globvars.geselecteerdeStukOpties != None:
        bord.TekenStukOpties(globvars.geselecteerdeStukOpties, scherm)

    #update het scherm
    pygame.display.flip()

#we komen hier alleen als we uit de game-loop zijn
pygame.quit()

