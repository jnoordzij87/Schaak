import random

import globale_enums
import globale_variabelen
from veld.getekendveld import GetekendVeld
from stukken.stuk import Stuk
import pygame
from zet.zet import Zet

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
        globale_variabelen.geselecteerdeStukOpties = stuk.krijg_beweegopties_in_positie(globale_variabelen.huidige_positie)
        globale_variabelen.moet_bord_bijgewerkt_worden = True
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
    positie = globale_variabelen.huidige_positie
    stukken = positie.krijg_alle_stukken_van_speler(speler)
    bekeken_stukken = []
    # kies een willekeurig stuk, dat minstens 1 zet ter beschikking heeft
    # gebruik een while loop die doorgaat tot er een stuk is gevonden dat aan de vereisten voldoet
    stukMetGeldigeZetGevonden = False
    while not stukMetGeldigeZetGevonden:
        if len(stukken) == 0:
            BehandelGameOver()
        # nog geen stuk met geldige zet gevonden. kies een random stuk
        stuk = random.choice(stukken)
        stukken.remove(stuk)
        # krijg de opties van het stuk
        opties = stuk.krijg_beweegopties_in_positie(positie)
        # als het stuk opties heeft, is er een geldig stuk gevonden
        if len(opties) > 0:
            #stuk met geldige zet gevonden, stap uit loop
            break
    #kies een willekeurige zet uit de opties van het stuk
    gekozenCoord = random.choice(opties)
    # check of de gekozen optie een gewone verplaatsing of een pakactie is
    staatErEenStukOpHetVeld = positie.staat_er_een_stuk_op_dit_veld(gekozenCoord)
    if staatErEenStukOpHetVeld:
        #het betreft een pakactie
        positie.pak_op_veld(stuk, gekozenCoord)
    else:
        #het betreft geen pakactie
        #verplaats het stuk naar het gekozen veld
        stuk_huidig_veld = positie.krijg_veld_van_stuk(stuk)
        positie.verplaats_stuk(stuk, stuk_huidig_veld, gekozenCoord)

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
            #check of zet geldig is
            geselecteerdeStuk = globale_variabelen.geselecteerdeStuk
            stuk_huidig_veld = positie.krijg_veld_van_stuk(geselecteerdeStuk)
            aangeklikte_veld = veld.coordinaat
            positie.verplaats_stuk(geselecteerdeStuk, stuk_huidig_veld, aangeklikte_veld)
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