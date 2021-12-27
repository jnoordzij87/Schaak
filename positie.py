from stukken.stuk import Stuk
from bord import Bord
from plaatjes.opzoeker import plaatjesOpzoeker
import pygame

class Positie:
    """
    In een positie beoog ik het volgende:
    -composiet met component bord
    -toegang tot verzameling van velden (via bord)
    -toegang tot verzameling van alle actieve stukken
    -voor elk veld: weten welk stuk er op staat
    -voor elk stuk: weten op welk veld het staat
    -verkrijgen van stuk bewegingsmogelijkheden
    -stukken en velden beoog ik hiermee onafhankelijk van elkaar te maken
    -wie is er aan zet
    -evaluatie of een positie geldig is of niet (mag een zet uitgevoerd worden)
    -is een positie schaak
    -is een positie schaakmat
    -positie mag input zijn voor updatebord(positie) / tekenbord(huidigepositie) (buiten deze class)
    """
    def __init__(self, bord : Bord):
        self._bord = bord
        self._stukken_in_het_spel = [] #lege lijst, wordt later gevuld
        self._veldbezetting = self._initialiseer_veldbezetting_dict()
        pass

    def teken_positie(self, scherm):
        """Tekent de stukken in het spel op de juiste positie op het scherm"""
        for stuk in self.stukken_in_het_spel:
            stuk_bordcoordinaat = self._krijg_stukpositie(stuk)
            stuk_schermpositie_x = self._bord.getekende_velden[stuk_bordcoordinaat].schermpositie_x
            stuk_schermpositie_y = self._bord.getekende_velden[stuk_bordcoordinaat].schermpositie_y
            stuk_plaatje = plaatjesOpzoeker[stuk.stuktype][stuk.kleur]
            #initialiseer het plaatje en schaal naar de grootte van het veld
            pygame.image.load(stuk_plaatje)
            pygame.transform.scale(stuk_plaatje,(stuk_plaatje.get_width() * 0.8, stuk_plaatje.get_height() * 0.8))
            #voeg het plaatje toe aan het scherm op de juiste positie
            scherm.blit(stuk_plaatje, (stuk_schermpositie_x, stuk_schermpositie_y))

    def _krijg_stukpositie(self, zoekstuk : Stuk) -> str:
        """
        :param zoekstuk: stuk om positie van op te zoeken
        :return: coordinaat, bijvoorbeeld 'A1'
        """
        for veld, stuk in self.veldbezetting.items():
            if stuk == zoekstuk:
                return veld

    def _initialiseer_veldbezetting_dict(self):
        """Initialiseer dictionary met lege veldbezetting"""
        self._veldbezetting = {}
        for veld in self._bord.velden:
            coord = veld.coordinaat
            self._veldbezetting[coord] = None

    @property
    def bord(self):
        return self._bord

    @property
    def stukken_in_het_spel(self) -> list(Stuk):
        """Lijst met alle stukken op het bord"""
        return self._stukken_in_het_spel

    @property
    def veldbezetting(self) -> dict(str, Stuk):
        """Dictionary met per veld opzoekbaar wat er op staat"""
        return self._veldbezetting