import random

import globale_enums
import globale_variabelen

def BehandelStukGeselecteerd(stuk):
    #maak onderscheid tussen een gewone selectie actie en een pakactie
    #een pakactie kunnen we als volgt herkennen:
    #1) als er voor deze stuk-selectie ook een stuk geselecteerd was,
    #2) en het huidige geselecteerde stuk is van een andere kleur als het vorige,
    #3) en het huidige geselecteerde stuk staat op een veld dat gezien wordt door het vorige,
    #dan wil de gebruiker het huidige geselecteerde stuk pakken.
    vorige_geselecteerde_stuk = globale_variabelen.geselecteerdeStuk
    nieuwe_geselecteerde_stuk = stuk
    #check 1) kijk of er een stuk geselecteerd was
    if vorige_geselecteerde_stuk == None:
        #er was geen vorig stuk geselecteerd, doe een gewone selectie
        SelecteerStuk(nieuwe_geselecteerde_stuk)
    else:
        #er was een vorig stuk geselecteerd. kijk of het gaat om een pakaktie
        #check 2) kijk of stuk van andere kleur is
        is_andere_kleur = vorige_geselecteerde_stuk.Kleur != nieuwe_geselecteerde_stuk.Kleur
        # check 3) kijk of het huidige geselecteerde stuk wordt 'gezien' door vorige stuk
        nieuwe_geselecteerde_stuk_veld = nieuwe_geselecteerde_stuk.HuidigVeld.Coordinaat()
        vorige_geselecteerde_stuk_opties = globale_variabelen.geselecteerdeStukOpties
        ziet_vorig_stuk_nieuw_stuk = nieuwe_geselecteerde_stuk_veld in vorige_geselecteerde_stuk_opties #dit kijkt of waarde in lijst voorkomt
        # combineer (2) en (3) om te kijken of het om een pak-actie gaat
        kan_vorig_stuk_nieuw_stuk_pakken = ziet_vorig_stuk_nieuw_stuk and is_andere_kleur #alleen waar als allebei waar is
        if kan_vorig_stuk_nieuw_stuk_pakken:
            #het gaat om een pakactie!
            PakStukOpVeld(vorige_geselecteerde_stuk, nieuwe_geselecteerde_stuk)
        else:
            #geen pakaktie, selecteer het nieuwe geselecteerde stuk
            SelecteerStuk(stuk)

def SelecteerStuk(stuk):
    #sta selectie alleen toe als het stuk van de speler aan zet is
    if IsStukVanSpelerAanZet(stuk):
        #selectie toegestaan
        #wijs het stuk aan als het geselecteerde stuk
        globale_variabelen.geselecteerdeStuk = stuk
        globale_variabelen.geselecteerdeStukOpties = stuk.KrijgVeldenWaarStukNaarToeKan()
    else:
        #we mogen dit stuk niet selecteren. Behandel als deselectie-actie
        DeSelecteer()

def DeSelecteer():
    globale_variabelen.geselecteerdeStuk = None
    globale_variabelen.geselecteerdeStukOpties = None

def WasErEenStukGeselecteerd():
    return globale_variabelen.geselecteerdeStuk != None

def StaatErEenStukOpVeld(coordinaat):
    stuk = KrijgStukOpVeld(coordinaat)
    return stuk != None

def KrijgStukOpVeld(coordinaat):
    for stuk in globale_variabelen.stukken:
        if stuk.HuidigVeld.Coordinaat() == coordinaat:
            return stuk
    #als we alle stukken hebben bekeken en geen gevonden, dan staat er geen stuk op dit veld
    return None

def KanStukNaarVeld(stuk, veld):
    #kijk of het aangeklikte veld tot de beweegopties van het stuk behoort
    #als in: zit de coordinaat van het veld in de lijst met beweegopties van het stuk?
    stukopties = stuk.KrijgVeldenWaarStukNaarToeKan()
    veldcoordinaat = veld.Coordinaat()
    zitVeldInStukOpties = veldcoordinaat in stukopties
    #geef het antwoord terug
    return zitVeldInStukOpties

def PakStukOpVeld(pakkendestuk, gepaktestuk):
    # Verwijder het gepaktestuk van de lijst met actieve stukken
    globale_variabelen.stukken.remove(gepaktestuk)
    #Verplaats het pakkende stuk naar het nieuwe veld
    Verplaats(pakkendestuk, gepaktestuk.HuidigVeld)

def Verplaats(stuk, veld):
    #deze functie is erg onduidelijk en moet nodig verbeterd worden!!!

    if isinstance(veld, str): # dit kijkt of 'veld' van het type string is
        #ERROR. het type van de veld-parameter is verkeerd. Het is geen veldobject maar een coordinaat
        #haal eerst het veldobject op o.b.v. het coordinaat
        coord = veld
        veld = globale_variabelen.velden[coord]
        #veld is nu een veldobject. we kunnen verder

    # zeg tegen het veld waar het stuk op stond dat er nu geen stuk meer op staat
    stuk.HuidigVeld.Stuk = None
    # zeg tegen het veld waar het stuk naar toe gaat dat nu dit stuk er op staat
    veld.Stuk = stuk
    # zeg tegen het stuk op welk veld het nu staat
    stuk.ZetNieuwVeld(veld)

    # reset de globale variabelen:
    # na het verplaatsen van een stuk is er geen stuk meer geselecteerd
    globale_variabelen.geselecteerdeStuk = None
    # reset de stukopties
    globale_variabelen.geselecteerdeStukOpties = None

    # na het verplaatsen van een stuk is de andere speler aan de beurt
    VeranderSpelerAanZet()

def KrijgStukkenVanSpeler(speler):
    stukkenVanSpeler = [] #start lege lijst
    for stuk in globale_variabelen.stukken:
        if stuk.VanWelkeSpelerIsDitStuk() == speler:
            stukkenVanSpeler.append(stuk)
    return stukkenVanSpeler

def DoeEenWillekeurigeZet(speler):
    stukken = KrijgStukkenVanSpeler(speler)
    # kies een willekeurig stuk, dat minstens 1 zet ter beschikking heeft
    # gebruik een while loop die doorgaat tot er een stuk is gevonden dat aan de vereisten voldoet
    stukMetGeldigeZetGevonden = False
    while not stukMetGeldigeZetGevonden:
        # nog geen stuk met geldige zet gevonden. kies een random stuk
        stuk = random.choice(stukken)
        # krijg de opties van het stuk
        opties = stuk.KrijgVeldenWaarStukNaarToeKan()
        # als het stuk opties heeft, is er een geldig stuk gevonden
        if len(opties) > 0:
            #er zit meer dan 1 optie in de lijst, stap uit de loop
            stukMetGeldigeZetGevonden = True
    #kies een willekeurige zet uit de opties van het stuk
    gekozenCoord = random.choice(opties)
    gekozenVeld = KrijgVeldObjectOpBasisVanCoordinaat(gekozenCoord)
    #check of de gekozen optie een gewone verplaatsing of een pakactie is
    staatErEenStukOpHetVeld = gekozenVeld.HeeftStuk()
    if staatErEenStukOpHetVeld:
        #het betreft een pakactie
        PakStukOpVeld(stuk, gekozenVeld.Stuk)
    else:
        #het betreft geen pakactie
        #verplaats het stuk naar het gekozen veld
        Verplaats(stuk, gekozenVeld)

def BehandelSpelerAanZetVeranderd():
    huidigeSpeler = globale_variabelen.spelerAanZet
    if huidigeSpeler == globale_enums.Spelers.Zwart:
        DoeEenWillekeurigeZet(huidigeSpeler)

def VeranderSpelerAanZet():
    huidigeSpeler = globale_variabelen.spelerAanZet
    if huidigeSpeler == globale_enums.Spelers.Wit:
        globale_variabelen.spelerAanZet = globale_enums.Spelers.Zwart
    if huidigeSpeler == globale_enums.Spelers.Zwart:
        globale_variabelen.spelerAanZet = globale_enums.Spelers.Wit
    BehandelSpelerAanZetVeranderd()

def IsStukVanSpelerAanZet(stuk):
    eigenaarVanStuk = stuk.VanWelkeSpelerIsDitStuk()
    spelerAanZet = globale_variabelen.spelerAanZet
    return eigenaarVanStuk == spelerAanZet

def BehandelVeldGeselecteerd(veld):
    #kijk of er een stuk op het veld staat
    if veld.HeeftStuk():
        #er is een stuk aangeklikt. behandel
        BehandelStukGeselecteerd(veld.Stuk)
    else:
        #er is een leeg veld aangeklikt
        #kijk of het om een verplaats actie gaat
        if WasErEenStukGeselecteerd():
            #er was een stuk geselecteerd toen het lege veld werd aangeklikt
            #kijk of het stuk naar het aangeklikte veld verplaatst kan worden
            geselecteerdeStuk = globale_variabelen.geselecteerdeStuk
            if KanStukNaarVeld(geselecteerdeStuk, veld):
                # ja! het stuk kan naar het aangeklikte veld. verplaats het stuk!
                Verplaats(geselecteerdeStuk, veld)
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
    for veld in globale_variabelen.velden.values():
        if veld.VormObject.collidepoint(klikX, klikY):
            # geselecteerde veld gevonden!
            BehandelVeldGeselecteerd(veld)

def KrijgVeldObjectOpBasisVanCoordinaat(coordinaat):
    return globale_variabelen.velden[coordinaat]