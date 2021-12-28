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

    def krijg_veldopties_voor_stuk_in_richting(self, stuk : Stuk, richting : Lineaire_Richtingen, maxaantal = None):
        """
        :return: een lijst met coordinaten in 1 richting, bijv ['E4', 'F4', 'G4', etc]
        """
        #aanpak: zolang we geen ongeldig vakje tegenkomen, bijv omdat we op rand van bord zijn gekomen
        #ga dan steeds door naar het volgende vakje in dezelfde richting
        resultaat = []
        teller = 0
        stuk_coord = self.krijg_veld_van_stuk(stuk)
        eerstvolgende_vakje = self.krijg_eerstvolgende_vakje_in_richting(stuk, stuk_coord, richting)
        is_geldige_optie = self._is_veld_geldige_optie_voor_stuk(stuk, eerstvolgende_vakje)
        while is_geldige_optie and teller != maxaantal: #stop als dit niet waar is
            #als we hier zijn is het volgende vakje geldig, voeg toe aan lijst
            resultaat.append(eerstvolgende_vakje)
            #als er een stuk van een andere kleur op het zojuist toegevoegde vakje staat, dan is dit het laatste vakje in deze richting, check
            if self._staat_er_een_stuk_van_andere_kleur_op_veld(stuk, eerstvolgende_vakje):
                break  #stap uit de loop
            #als we hier zijn, kijk naar het volgende vakje, en ga door
            eerstvolgende_vakje = self.krijg_eerstvolgende_vakje_in_richting(eerstvolgende_vakje, richting)
            is_geldige_optie = self._is_veld_geldige_optie_voor_stuk(stuk, eerstvolgende_vakje)
            teller += 1
        #als uit loop: geef resultaat terug
        return resultaat

    def _is_veld_geldige_optie_voor_stuk(self, stuk, coordinaat):
        bezet_door_eigen_stuk = self._staat_er_een_stuk_van_zelfde_kleur_op_veld(stuk, coordinaat)
        return coordinaat != None and not bezet_door_eigen_stuk

    def _staat_er_een_stuk_van_andere_kleur_op_veld(self, stuk, veld):
        staat_stuk_op_veld = self.staat_er_een_stuk_op_dit_veld(veld)
        if not staat_stuk_op_veld:
            return False
        else:
            stuk_op_veld = self.krijg_stuk_op_veld(veld)
            andere_kleur = stuk_op_veld.kleur != stuk.kleur
            return andere_kleur

    def _staat_er_een_stuk_van_zelfde_kleur_op_veld(self, stuk, veld):
        staat_stuk_op_veld = self.staat_er_een_stuk_op_dit_veld(veld)
        if not staat_stuk_op_veld:
            return False
        else:
            stuk_op_veld = self.krijg_stuk_op_veld(veld)
            zelfde_kleur = stuk_op_veld.kleur == stuk.kleur
            return zelfde_kleur

    def krijg_eerstvolgende_vakje_in_richting(self, stuk, coordinaat, richting):
        kolom = coordinaat[0]
        rij = int(coordinaat[1])
        if richting == Lineaire_Richtingen.Links:
            kolom = self.bord.KolomLinks(kolom)
        if richting == Lineaire_Richtingen.Rechts:
            kolom = self.bord.KolomRechts(kolom)
        if richting == Lineaire_Richtingen.Boven:
            rij = self.bord.RijOmhoog(rij)
        if richting == Lineaire_Richtingen.Onder:
            rij = self.bord.RijOmlaag(rij)
        if richting == Lineaire_Richtingen.LinksBoven:
            kolom = self.bord.KolomLinks(kolom)
            rij = self.bord.RijOmhoog(rij)
        if richting == Lineaire_Richtingen.LinksOnder:
            kolom = self.bord.KolomLinks(kolom)
            rij = self.bord.RijOmlaag(rij)
        if richting == Lineaire_Richtingen.RechtsBoven:
            kolom = self.bord.KolomRechts(kolom)
            rij = self.bord.RijOmhoog(rij)
        if richting == Lineaire_Richtingen.RechtsOnder:
            kolom = self.bord.KolomRechts(kolom)
            rij = self.bord.RijOmlaag(rij)
        # als volgende veld ongeldig is: geef niks terug
        if kolom == None or rij == None:
            return None
        #als we hier zijn hebben we een geldige coordinaat
        eerstvolgendevakje = kolom + str(rij)
        return eerstvolgendevakje


    def kan_stuk_naar_veld(self, stuk : Stuk, veld : str):
        # kijk of het aangeklikte veld tot de beweegopties van het stuk behoort
        # als in: zit de coordinaat van het veld in de lijst met beweegopties van het stuk?
        stukopties = stuk.krijg_veldopties()
        veldcoordinaat = veld.Coordinaat()
        zitVeldInStukOpties = veldcoordinaat in stukopties
        # geef het antwoord terug
        return zitVeldInStukOpties

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
        l
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

    def verander_speler_aan_zet(self):
        huidigeSpeler = self.speler_aan_zet
        if huidigeSpeler == Spelers.wit:
            self.speler_aan_zet = Spelers.zwart
        if huidigeSpeler == Spelers.zwart:
            self.speler_aan_zet = Spelers.wit