from stukken.stuk import Stuk
from bord.bord import Bord
from plaatjes.opzoeker import plaatjesOpzoeker
from globale_enums import Lineaire_Richtingen, Spelers
import globale_variabelen
import pygame

class Positie:
    """
    In een positie beoog ik het volgende:
    -composiet met component bord
    -toegang tot verzameling van velden (via bord)
    -toegang tot verzameling van alle actieve stukken
    -voor elk veld: weten welk stuk er op staat
    -voor elk stuk: weten op welk veld het staat
    -verkrijgen van stuk bewegingsmogelijkheden -> verplaatst naar beweging
    -stukken en velden beoog ik hiermee onafhankelijk van elkaar te maken
    -wie is er aan zet
    -evaluatie of een positie geldig is of niet (mag een zet uitgevoerd worden)
    -is een positie schaak
    -is een positie schaakmat
    -positie mag input zijn voor updatebord(positie) / tekenbord(huidigepositie) (buiten deze class)
    """
    def __init__(self, bord : Bord):
        self._bord = bord
        self._actieve_stukken = [] #lijst wordt gevuld bij initialiseren startpositie
        self._veldbezetting = self._initialiseer_veldbezetting()
        self._speler_aan_zet = None

    @property
    def bord(self):
        return self._bord

    @property
    def actieve_stukken(self) -> list(Stuk):
        """Lijst met alle stukken op het bord"""
        return self._actieve_stukken

    @property
    def veldbezetting(self) -> dict(str, Stuk):
        """Dictionary met per veld opzoekbaar wat er op staat"""
        return self._veldbezetting

    @property
    def speler_aan_zet(self):
        return self._speler_aan_zet

    def pak_op_veld(self, pakkendestuk : Stuk, veld : str):
        gepakte_stuk = self.krijg_stuk_op_veld(veld)
        self.pak_stuk(pakkendestuk, gepakte_stuk)

    def pak_stuk(self, pakkendestuk : Stuk, gepaktestuk : Stuk):
        # Verwijder het gepaktestuk van de lijst met actieve stukken
        self.actieve_stukken.remove(gepaktestuk)
        # Verplaats het pakkende stuk naar het nieuwe veld
        pakkend_stuk_huidig_veld = self.krijg_veld_van_stuk(pakkendestuk)
        pakkend_stuk_nieuw_veld = self.krijg_veld_van_stuk(gepaktestuk)
        self.verplaats_stuk(pakkendestuk, pakkend_stuk_huidig_veld, pakkend_stuk_nieuw_veld)

    def verplaats_stuk(self, stuk : Stuk, oudeveld : str, nieuweveld : str):
        #update veldbezetting
        self.veldbezetting[oudeveld] = None
        self.veldbezetting[nieuweveld] = stuk
        #reset globale variabelen:
        globale_variabelen.geselecteerdeStuk = None
        globale_variabelen.geselecteerdeStukOpties = None
        #na het verplaatsen van een stuk is de andere speler aan de beurt
        self.verander_speler_aan_zet()

    def krijg_alle_stukken_van_speler(self, speler : Spelers):
        stukkenVanSpeler = []  #start lege lijst
        for stuk in self.actieve_stukken:
            if stuk.krijg_eigenaar_van_stuk() == speler:
                stukkenVanSpeler.append(stuk)
        return stukkenVanSpeler

    def krijg_veldopties_voor_stuk(self, stuk : Stuk) -> list(str):
        resultaat = []
        for beweegrichting in stuk.beweegrichtingen:
            beschikbare_velden_in_richting = self.krijg_veldopties_voor_stuk_in_richting(
                stuk,beweegrichting)
            resultaat.extend(beschikbare_velden_in_richting)
        return resultaat

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
            stuk_bordcoordinaat = self._krijg_stukpositie(stuk)
            stuk_schermpositie_x = self._bord.getekende_velden[stuk_bordcoordinaat].schermpositie_x
            stuk_schermpositie_y = self._bord.getekende_velden[stuk_bordcoordinaat].schermpositie_y
            stuk_plaatje = plaatjesOpzoeker[stuk.stuktype][stuk.kleur]
            #initialiseer het plaatje en schaal naar de grootte van het veld
            pygame.image.load(stuk_plaatje)
            pygame.transform.scale(stuk_plaatje,(stuk_plaatje.get_width() * 0.8, stuk_plaatje.get_height() * 0.8))
            #voeg het plaatje toe aan het scherm op de juiste positie
            scherm.blit(stuk_plaatje, (stuk_schermpositie_x, stuk_schermpositie_y))

    def _initialiseer_veldbezetting(self):
        """Initialiseer dictionary met lege veldbezetting"""
        veldbezetting = {}
        for veld in self._bord.velden:
            coord = veld.coordinaat
            veldbezetting[coord] = None
        return veldbezetting

    def verander_speler_aan_zet(self):
        huidigeSpeler = self.speler_aan_zet
        if huidigeSpeler == Spelers.wit:
            self.speler_aan_zet = Spelers.zwart
        if huidigeSpeler == Spelers.zwart:
            self.speler_aan_zet = Spelers.wit