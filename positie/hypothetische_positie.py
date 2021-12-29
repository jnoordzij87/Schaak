from positie.positie import Positie
from globale_enums import StukType
from stukken.stuk import Stuk
import copy

class HypothetischePositie(Positie):
    def __init__(self, positie):
        self.hypo_positie = copy.deepcopy(positie)
        return

    @property
    def actieve_stukken(self) -> list[Stuk]:
        """Lijst met alle stukken op het bord"""
        return self.hypo_positie._actieve_stukken

    @property
    def veldbezetting(self) -> dict[str, Stuk]:
        """Dictionary met per veld opzoekbaar wat er op staat"""
        return self.hypo_positie._veldbezetting

    @property
    def speler_aan_zet(self):
        return self.hypo_positie._speler_aan_zet

    def verwijder_stuk(self, stuk):
        stuk_veld = self.hypo_positie.krijg_veld_van_stuk(stuk)
        self.hypo_positie.veldbezetting[stuk_veld] = None

    def is_positie_geldig(self):
        #Als koning van speler aan zet schaak staat, mag beurt niet worden beeindigd
        self.staat_koning_van_speler_aan_zet_schaak()

    def staat_koning_van_speler_aan_zet_schaak(self):
        #krijg veld van koning
        koning_coord = self.krijg_koningspositie_van_speler(self.hypo_positie.speler_aan_zet)
        #krijg stukken van andere speler
        speler_niet_aan_zet = self.krijg_andere_speler(self.speler_aan_zet)
        stukken_andere_speler = self.krijg_alle_stukken_van_speler(speler_niet_aan_zet)
        #kijk voor alle stukken van tegenstander of deze de koning zien
        for stuk in stukken_andere_speler:
            stuk_zicht = stuk.krijg_zicht_in_positie(self.hypo_positie)
            if koning_coord in stuk_zicht:
                #stuk ziet koning
                return True

    def krijg_koningspositie_van_speler(self, speler):
        for stuk in self.krijg_alle_stukken_van_speler(speler):
            if stuk.stuktype == StukType.Koning:
                koning_coord = self.krijg_veld_van_stuk(stuk)
                return koning_coord

