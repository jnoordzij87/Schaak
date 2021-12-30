import globale_variabelen
import hulpfuncties
import random
from zet.zet import Zet

class AI:
    def __init__(self):
        pass

    def doe_random_geldige_zet(self, speler):
        positie = globale_variabelen.huidige_positie
        stukken = positie.krijg_alle_stukken_van_speler(speler)
        random.shuffle(stukken)
        for stuk in stukken:
            stuk_huidig_veld = positie.krijg_veld_van_stuk(stuk)
            stuk_opties = stuk.krijg_beweegopties_in_positie(positie)
            random.shuffle(stuk_opties)
            for veld_optie in stuk_opties:
                zet = Zet(positie, stuk_huidig_veld, veld_optie)
                if zet.is_zet_geldig():
                    zet.doe_zet()
                    return
        #als we hier zijn is er geen stuk met een geldige zet: schaakmat!
        globale_variabelen.schaakmat = True

    def DoeEenWillekeurigeZet(self, speler):
        self.doe_random_geldige_zet(speler)
        return
        positie = globale_variabelen.huidige_positie
        stukken = positie.krijg_alle_stukken_van_speler(speler)
        # kies een willekeurig stuk, dat minstens 1 zet ter beschikking heeft
        # gebruik een while loop die doorgaat tot er een stuk is gevonden dat aan de vereisten voldoet
        stukMetGeldigeZetGevonden = False
        while not stukMetGeldigeZetGevonden:
            if len(stukken) == 0:
                BehandelGameOver()
                return
            if not stukken:
                BehandelGameOver()
                return
            # nog geen stuk met geldige zet gevonden. kies een random stuk
            stuk = random.choice(stukken)
            stukken.remove(stuk)
            # krijg de opties van het stuk
            opties = stuk.krijg_beweegopties_in_positie(positie)
            # als het stuk opties heeft, is er een geldig stuk gevonden
            if len(opties) > 0:
                # stuk met geldige zet gevonden, stap uit loop
                break
        # kies een willekeurige zet uit de opties van het stuk
        gekozenCoord = random.choice(opties)
        # check of de gekozen optie een gewone verplaatsing of een pakactie is
        staatErEenStukOpHetVeld = positie.staat_er_een_stuk_op_dit_veld(gekozenCoord)
        if staatErEenStukOpHetVeld:
            # het betreft een pakactie
            positie.pak_op_veld(stuk, gekozenCoord)
        else:
            # het betreft geen pakactie
            # verplaats het stuk naar het gekozen veld
            stuk_huidig_veld = positie.krijg_veld_van_stuk(stuk)
            positie.verplaats_stuk(stuk, stuk_huidig_veld, gekozenCoord)