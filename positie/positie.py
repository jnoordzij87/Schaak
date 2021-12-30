import copy

from stukken.stuk import Stuk
from bord.bord import Bord
from plaatjes.opzoeker import plaatjesOpzoeker
from globale_enums import Lineaire_Richtingen, Spelers, StukType
import globale_variabelen
import pygame

class Positie:
    def __init__(self, bord : Bord):
        self._bord = bord
        self._actieve_stukken = [] #lijst wordt gevuld bij initialiseren startpositie
        self._veldbezetting = self._initialiseer_veldbezetting()
        self._speler_aan_zet = None
        self.staat_speler_aan_zet_schaak = False

    #TODO: haal bord weg uit positie class. vind t toch onlogisch
    @property
    def bord(self):
        return self._bord

    @property
    def actieve_stukken(self) -> list[Stuk]:
        """Lijst met alle stukken op het bord"""
        return self._actieve_stukken

    @property
    def veldbezetting(self) -> dict[str, Stuk]:
        """Dictionary met per veld opzoekbaar wat er op staat"""
        return self._veldbezetting

    @property
    def speler_aan_zet(self):
        return self._speler_aan_zet

    def is_positie_geldig(self):
        #Als koning van speler aan zet schaak staat, mag beurt niet worden beeindigd
        koning_staat_schaak = self.staat_koning_van_speler_aan_zet_schaak()
        return not koning_staat_schaak

    def staat_koning_van_speler_aan_zet_schaak(self):
        #krijg veld van koning
        koning_coord = self.krijg_koningspositie_van_speler(self.speler_aan_zet)
        #krijg stukken van andere speler
        speler_niet_aan_zet = self.krijg_andere_speler(self.speler_aan_zet)
        stukken_andere_speler = self.krijg_alle_stukken_van_speler(speler_niet_aan_zet)
        #kijk voor alle stukken van tegenstander of deze de koning zien
        for stuk in stukken_andere_speler:
            stuk_zicht = stuk.krijg_zicht_in_positie(self)
            if koning_coord in stuk_zicht:
                #stuk ziet koning
                return True
        #als we hier zijn, zijn alle stukken gecheckt en staat koning niet schaak
        return False

    def krijg_koningspositie_van_speler(self, speler):
        for stuk in self.krijg_alle_stukken_van_speler(speler):
            if stuk.stuktype == StukType.Koning:
                koning_coord = self.krijg_veld_van_stuk(stuk)
                return koning_coord

    def krijg_alle_stukken_van_speler(self, speler : Spelers):
        stukkenVanSpeler = []  #start lege lijst
        for stuk in self.actieve_stukken:
            if stuk.eigenaar == speler:
                stukkenVanSpeler.append(stuk)
        return stukkenVanSpeler

    def krijg_stuk_op_veld(self, veld : str) -> Stuk:
        """
        :param veld: bordcoordinaat
        :return: Stuk of None
        """
        return self.veldbezetting[veld]

    def staat_er_een_stuk_op_dit_veld(self, veld : str) -> bool:
        """
        :param veld: bordcoordinaat
        :return: True / False
        """
        staat_stuk_op_veld = self.krijg_stuk_op_veld(veld) != None
        return staat_stuk_op_veld

    def krijg_veld_van_stuk(self, zoekstuk : Stuk) -> str:
        """
        :param zoekstuk: stuk om positie van op te zoeken
        :return: coordinaat, bijvoorbeeld 'A1'
        """
        for veld, stuk in self.veldbezetting.items():
            if stuk == zoekstuk:
                return veld

    def teken_positie(self, scherm):
        """Tekent de stukken in het spel op de juiste positie op het scherm"""
        for stuk in self.actieve_stukken:
            veld = self.krijg_veld_van_stuk(stuk)
            veld_schermpositie_x = self._bord.getekende_velden[veld].schermpositie_x
            veld_schermpositie_y = self._bord.getekende_velden[veld].schermpositie_y
            stuk_plaatje = plaatjesOpzoeker[stuk.stuktype][stuk.kleur]
            #initialiseer het plaatje en schaal naar de grootte van het veld
            surface = pygame.image.load(stuk_plaatje)
            pygame.transform.scale(surface,(surface.get_width() * 0.8, surface.get_height() * 0.8))
            #voeg het plaatje toe aan het scherm op de juiste positie
            scherm.blit(surface, (veld_schermpositie_x, veld_schermpositie_y))

    def _initialiseer_veldbezetting(self):
        """Initialiseer dictionary met lege veldbezetting"""
        veldbezetting = {}
        for veld in self._bord.velden:
            coord = veld.coordinaat
            veldbezetting[coord] = None
        return veldbezetting

    def krijg_andere_speler(self, speler):
        if speler == Spelers.wit:
            return Spelers.zwart
        if speler == Spelers.zwart:
            return Spelers.wit

    def verander_speler_aan_zet(self, ):
        huidige_speler_aan_zet = self.speler_aan_zet
        nieuwe_speler_aan_zet = self.krijg_andere_speler(huidige_speler_aan_zet)
        self._speler_aan_zet = nieuwe_speler_aan_zet

