import pygame
import globale_variabelen
import hulpfuncties


class Veld:
    def __init__(self, rij, kolom, posX, posY, kleur, vakjesgrootte, bord):
        self.Rij = rij
        self.Kolom = kolom
        self.PosX = posX
        self.PosY = posY
        self.Kleur = kleur
        self.VakjesGrootte = vakjesgrootte
        self.Bord = bord  # bewaar een referentie naar het bord object
        self.Stuk = None # houd bij of er een stuk op het veld staat
        self.IsGeselecteerd = False # houd bij of het veld is geselecteerd
        self.VormObject = None # bewaar een referentie naar het vorm object

    def HeeftStuk(self):
        return self.Stuk != None

    def HeeftStukVanSpelerAanZet(self):
        return self.Stuk != None

    def VerwijderStukVanVeld(self):
        self.Stuk = None

    def DeSelecteer(self):
        self.IsGeselecteerd = False

    def Selecteer(self):
        #deselecteer eerst alle andere velden
        #dit zorgt ervoor dat de groene kleur bij het vorige geselecteerde vakje verdwijnt
        for veld in globale_variabelen.velden.values():
            veld.DeSelecteer()
        #selecteer nu dit veld
        self.IsGeselecteerd = True

    def Coordinaat(self):
        return (self.Kolom + self.Rij)

    def Teken(self, scherm):
        #kijk of het vakje is geselecteerd. als dat zo is, teken het vakje met een groene kleur i.p.v. normale kleur
        if self.IsGeselecteerd:
            kleur = hulpfuncties.VakjesKleuren.Groen.value
        else:
            kleur = self.Kleur
        self.MaakVakje(scherm, kleur, self.PosX, self.PosY, self.VakjesGrootte, self.VakjesGrootte)
        pass

    def MaakVakje(self, scherm, kleur, posX, posY, breedte, hoogte):
        #sla het gemaakte vormopject op, zodat we dit kunnen gebruiken bij een muisklikgebeurtenis
        self.VormObject = pygame.draw.rect(scherm, kleur, (posX, posY, breedte, hoogte))

    def MiddelPunt(self):
        return ( (self.PosX + (0.5 * self.VakjesGrootte)) , (self.PosY + (0.5 * self.VakjesGrootte)) )