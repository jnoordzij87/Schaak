import pygame
import globale_enums
import globale_variabelen
import hulpfuncties

pygame.init()
schermbreedte, schermhoogte = 400, 400
scherm = pygame.display.set_mode((schermbreedte, schermhoogte))
pygame.display.set_caption('Schaak')
hulpfuncties.InitialiseerBord(scherm, schermbreedte, schermhoogte)

#ga de game-loop in
houdspeldraaiend = True
huidige_selectie = None
speler_aan_zet = globale_enums.Spelers.wit
while houdspeldraaiend == True:
    #aan het begin van de loop is het bord up to date
    moet_bord_geupdate_worden = False
    #controleer muisklikgebeurtenissen
    houdspeldraaiend = hulpfuncties.CheckPygameGebeurtenissen()
    if globale_variabelen.schaakmat == True:
        continue

    #controleer gewijzigde selectie. update bord als nodig
    if hulpfuncties.IsSelectieGewijzigd(huidige_selectie):
        #stuk selectie gewijzigd
        moet_bord_geupdate_worden = True
        #update selectie
        huidige_selectie = globale_variabelen.geselecteerdeStuk
    #controleer gewijzigde speler aan zet. behandel als nodig
    if hulpfuncties.IsSpelerAanZetGewijzigd(speler_aan_zet):
        moet_bord_geupdate_worden = True
        hulpfuncties.BehandelSpelerAanZetVeranderd()
    #update bord als nodig
    if moet_bord_geupdate_worden == True:
        hulpfuncties.UpdateVisueleElementen(scherm, schermbreedte, schermhoogte)
    #update het scherm
    pygame.display.flip()

    if globale_variabelen.schaakmat == True:
        hulpfuncties.BehandelSchaakmat()

#we komen hier als we uit de game-loop zijn
pygame.quit()

