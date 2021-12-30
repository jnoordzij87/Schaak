import random

import globale_enums
import globale_variabelen
from veld.getekendveld import GetekendVeld
from stukken.stuk import Stuk
import pygame
from zet.zet import Zet
from ai.ai import AI
from bord.bord import Bord
from positie.startpositie import StartPositie

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

def IsSelectieGewijzigd(huidige_selectie):
    return globale_variabelen.geselecteerdeStuk != huidige_selectie

def IsSpelerAanZetGewijzigd(speler_aan_zet):
    return speler_aan_zet != globale_variabelen.huidige_positie.speler_aan_zet

def CheckMuisKlikGebeurtenissen():
    # kijk elke keer of er een speciale gebeurtenis heeft plaatsgevonden
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # als we hier zijn is er op het kruisje geklikt
            return False
        if event.type == pygame.MOUSEBUTTONDOWN:
            # als we hier zijn is er in het scherm geklikt
            BehandelKlikGebeurtenis(event)
    return True

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

def IsPakActie(stuk : Stuk):
    positie = globale_variabelen.huidige_positie
    vorig_geselecteerde_stuk = globale_variabelen.geselecteerdeStuk
    nieuw_geselecteerde_stuk = stuk
    was_er_een_stuk_geselecteerd = vorig_geselecteerde_stuk != None
    if not was_er_een_stuk_geselecteerd:
        #als er geen stuk geselecteerd was kan het nooit gaan om een pakactie
        return False
    else:
        #er was een stuk geselecteerd
        #kijk of het vorige geselecteerde stuk het huidige geselecteerde stuk kan pakken
        nieuw_geselecteerde_stuk_coordinaat = positie.krijg_veld_van_stuk(nieuw_geselecteerde_stuk)
        kan_pakken = vorig_geselecteerde_stuk.kan_stuk_naar_veld(nieuw_geselecteerde_stuk_coordinaat, positie)
        return kan_pakken

def BehandelStukGeselecteerd(stuk : Stuk):
    #we komen hier zowel bij een pakactie als bij gewone stukselectie, herken onderscheid
    if IsPakActie(stuk):
        vorige_geselecteerde_stuk = globale_variabelen.geselecteerdeStuk
        nieuwe_geselecteerde_stuk = stuk
        positie = globale_variabelen.huidige_positie
        positie.pak_stuk(vorige_geselecteerde_stuk, nieuwe_geselecteerde_stuk)
    else:
        # geen pakaktie, selecteer het nieuwe geselecteerde stuk
        Selecteer(stuk)

def Selecteer(stuk):
    #sta selectie alleen toe als het stuk van de speler aan zet is
    speler_aan_zet = globale_variabelen.huidige_positie.speler_aan_zet
    if stuk.is_stuk_van_speler(speler_aan_zet):
        #selectie toegestaan
        #wijs het stuk aan als het geselecteerde stuk
        globale_variabelen.geselecteerdeStuk = stuk
    else:
        #we mogen dit stuk niet selecteren. Behandel als deselectie-actie
        DeSelecteer()

def DeSelecteer():
    globale_variabelen.geselecteerdeStuk = None
    globale_variabelen.geselecteerdeStukOpties = None
    globale_variabelen.moet_bord_bijgewerkt_worden = True

def WasErEenStukGeselecteerd():
    return globale_variabelen.geselecteerdeStuk != None

def BehandelGameOver():
    pygame.quit()

def DoeEenWillekeurigeZet(speler):
    AI().doe_random_geldige_zet(speler)

def BehandelSpelerAanZetVeranderd():
    huidigeSpeler = globale_variabelen.huidige_positie.speler_aan_zet
    if huidigeSpeler == globale_enums.Spelers.zwart:
        DoeEenWillekeurigeZet(huidigeSpeler)

def IsVerplaatsActie(veld : GetekendVeld):
    if not WasErEenStukGeselecteerd():
        return False
    else:
        #kan geselecteerde stuk naar aangeklikte veld?
        positie = globale_variabelen.huidige_positie
        geselecteerdeStuk = globale_variabelen.geselecteerdeStuk
        kan_stuk_naar_veld = geselecteerdeStuk.kan_stuk_naar_veld(veld.coordinaat, positie)
        if kan_stuk_naar_veld:
            #is verplaats actie
            return True
        else:
            return False

def BehandelVeldGeselecteerd(veld : GetekendVeld):
    # kijk of er een stuk op het aangeklikte veld staat
    positie = globale_variabelen.huidige_positie
    stuk_op_veld = positie.staat_er_een_stuk_op_dit_veld(veld.coordinaat)
    if stuk_op_veld:
        #er is een stuk aangeklikt. behandel
        aangeklikte_stuk = positie.krijg_stuk_op_veld(veld.coordinaat)
        BehandelStukGeselecteerd(aangeklikte_stuk)
    else:
        #er is een leeg veld aangeklikt
        #kijk of het om een verplaats actie gaat
        if IsVerplaatsActie(veld):
            #als we hier zijn weten we dat de zet geldig is (pin check al gebeurd)
            geselecteerde_stuk = globale_variabelen.geselecteerdeStuk
            huidig_veld = positie.krijg_veld_van_stuk(geselecteerde_stuk)
            nieuw_veld = veld.coordinaat
            Zet(positie, huidig_veld, nieuw_veld).doe_zet()
        elif WasErEenStukGeselecteerd():
            # er is een veld aangeklikt dat niet tot de mogelijkheden van het geselecteerde stuk behoort
            # de-selecteer het stuk
            DeSelecteer()
        else:
            #er is een leeg veld aangeklikt, maar er was ook geen geselecteerd suk. doe niets
            pass

def BehandelKlikGebeurtenis(event):
    """
    Deze functie doet alles wat er moet gebeuren als de gebruiker ergens heeft geklikt
    """
    #kijk waar op het scherm er is geklikt
    klikX, klikY = event.pos
    #vind uit welk veld is aangeklikt
    for veld in globale_variabelen.huidige_positie.bord.getekende_velden.values():
        if veld.vorm.collidepoint(klikX, klikY):
            # geselecteerde veld gevonden!
            BehandelVeldGeselecteerd(veld)