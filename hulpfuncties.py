import random

import globale_enums
import globale_variabelen
from veld.getekendveld import GetekendVeld
from stukken.stuk import Stuk

def BehandelStukGeselecteerd(stuk : Stuk):
    #maak onderscheid tussen een gewone selectie actie en een pakactie
    #een pakactie kunnen we als volgt herkennen:
    #1) als er voor deze stuk-selectie ook een stuk geselecteerd was,
    #2) en het huidige geselecteerde stuk is van een andere kleur als het vorige,
    #3) en het huidige geselecteerde stuk staat op een veld dat gezien wordt door het vorige,
    #dan wil de gebruiker het huidige geselecteerde stuk pakken.
    vorige_geselecteerde_stuk = globale_variabelen.geselecteerdeStuk
    nieuwe_geselecteerde_stuk = stuk
    positie = globale_variabelen.huidige_positie
    #check 1) kijk of er een stuk geselecteerd was
    if vorige_geselecteerde_stuk == None:
        #er was geen vorig stuk geselecteerd, doe een gewone selectie
        Selecteer(nieuwe_geselecteerde_stuk)
    else:
        #er was een vorig stuk geselecteerd. kijk of het gaat om een pakaktie
        #check 2) kijk of stuk van andere kleur is
        is_andere_kleur = vorige_geselecteerde_stuk.kleur != nieuwe_geselecteerde_stuk.kleur
        # check 3) kijk of het huidige geselecteerde stuk wordt 'gezien' door vorige stuk
        nieuwe_geselecteerde_stuk_veld = nieuwe_geselecteerde_stuk.HuidigVeld.Coordinaat()
        vorige_geselecteerde_stuk_opties = globale_variabelen.geselecteerdeStukOpties
        ziet_vorig_stuk_nieuw_stuk = nieuwe_geselecteerde_stuk_veld in vorige_geselecteerde_stuk_opties #dit kijkt of waarde in lijst voorkomt
        # combineer (2) en (3) om te kijken of het om een pak-actie gaat
        kan_vorig_stuk_nieuw_stuk_pakken = ziet_vorig_stuk_nieuw_stuk and is_andere_kleur #alleen waar als allebei waar is
        if kan_vorig_stuk_nieuw_stuk_pakken:
            #het gaat om een pakactie!
            positie.pak_stuk(vorige_geselecteerde_stuk, nieuwe_geselecteerde_stuk)
        else:
            #geen pakaktie, selecteer het nieuwe geselecteerde stuk
            Selecteer(stuk)

def Selecteer(stuk):
    #sta selectie alleen toe als het stuk van de speler aan zet is
    speler_aan_zet = globale_variabelen.huidige_positie.speler_aan_zet
    if stuk.is_stuk_van_speler(speler_aan_zet):
        #selectie toegestaan
        #wijs het stuk aan als het geselecteerde stuk
        globale_variabelen.geselecteerdeStuk = stuk
        globale_variabelen.geselecteerdeStukOpties = stuk.krijg_beweegopties_in_positie(globale_variabelen.huidige_positie)
    else:
        #we mogen dit stuk niet selecteren. Behandel als deselectie-actie
        DeSelecteer()

def DeSelecteer():
    globale_variabelen.geselecteerdeStuk = None
    globale_variabelen.geselecteerdeStukOpties = None

def WasErEenStukGeselecteerd():
    return globale_variabelen.geselecteerdeStuk != None

def DoeEenWillekeurigeZet(speler):
    positie = globale_variabelen.huidige_positie
    stukken = positie.krijg_alle_stukken_van_speler(speler)
    # kies een willekeurig stuk, dat minstens 1 zet ter beschikking heeft
    # gebruik een while loop die doorgaat tot er een stuk is gevonden dat aan de vereisten voldoet
    stukMetGeldigeZetGevonden = False
    while not stukMetGeldigeZetGevonden:
        # nog geen stuk met geldige zet gevonden. kies een random stuk
        stuk = random.choice(stukken)
        # krijg de opties van het stuk
        opties = positie.krijg_veldopties_voor_stuk(stuk)
        # als het stuk opties heeft, is er een geldig stuk gevonden
        if len(opties) > 0:
            stukMetGeldigeZetGevonden = True
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
    huidigeSpeler = globale_variabelen.spelerAanZet
    if huidigeSpeler == globale_enums.Spelers.zwart:
        DoeEenWillekeurigeZet(huidigeSpeler)

def BehandelVeldGeselecteerd(veld : GetekendVeld):
    #kijk of er een stuk op het veld staat
    stuk_op_veld = globale_variabelen.huidige_positie.staat_er_een_stuk_op_dit_veld(veld.coordinaat)
    if stuk_op_veld:
        stuk = globale_variabelen.huidige_positie.krijg_stuk_op_veld(veld.coordinaat)
        #er is een stuk aangeklikt. behandel
        BehandelStukGeselecteerd(stuk)
    else:
        #er is een leeg veld aangeklikt
        #kijk of het om een verplaats actie gaat
        if WasErEenStukGeselecteerd():
            #er was een stuk geselecteerd toen het lege veld werd aangeklikt
            #kijk of het stuk naar het aangeklikte veld verplaatst kan worden
            geselecteerdeStuk = globale_variabelen.geselecteerdeStuk
            if geselecteerdeStuk.kan_stuk_naar_veld(geselecteerdeStuk, veld, globale_variabelen.huidige_positie):
                # ja! het stuk kan naar het aangeklikte veld. verplaats het stuk!
                globale_variabelen.huidige_positie.verplaats_stuk(geselecteerdeStuk, veld)
            else:
                #er is een veld aangeklikt dat niet tot de mogelijkheden van het geselecteerde stuk behoort
                #de-selecteer het stuk
                DeSelecteer()

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