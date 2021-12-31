import random
import globale_variabelen
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
                zet = Zet(stuk, veld_optie, positie)
                if zet.is_zet_geldig():
                    zet.doe_zet()
                    return

        #als we hier zijn is er geen stuk met een geldige zet: schaakmat!
        globale_variabelen.schaakmat = True #TODO: add Pat