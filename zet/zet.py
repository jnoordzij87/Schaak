import globale_variabelen
from globale_enums import StukType
import copy

class Zet():
    def __init__(self, positie, oud_veld, nieuw_veld):
        self.echte_positie = positie
        self.oud_veld = oud_veld
        self.nieuw_veld = nieuw_veld

    def doe_zet(self):
        self.doe_zet_in_positie(self.echte_positie)
        self.echte_positie.verander_speler_aan_zet()
        globale_variabelen.huidige_positie = self.echte_positie
        globale_variabelen.geselecteerdeStuk = None

    def geeft_verplaatste_stuk_schaak(self, positie):
        verplaatste_stuk = positie.krijg_stuk_op_veld(self.nieuw_veld)
        zicht_verplaatste_stuk = verplaatste_stuk.krijg_zicht_in_positie(positie)
        andere_speler = positie.krijg_andere_speler(positie.speler_aan_zet)
        koning_coord = positie.krijg_koningspositie_van_speler(andere_speler)
        return koning_coord in zicht_verplaatste_stuk

    def is_zet_geldig(self):
        hypothetische_positie = copy.deepcopy(self.echte_positie)
        self.doe_zet_in_positie(hypothetische_positie)
        is_zet_geldig = self.is_positie_geldig(hypothetische_positie)
        return is_zet_geldig

    def doe_zet_in_positie(self, positie):
        if self.is_pakactie(positie):
            self.pak_op_veld_in_positie(positie)
        else:
            self.verplaats_stuk_in_positie(positie)

    def is_positie_geldig(self, positie):
        staat_eigen_koning_schaak = self.staat_koning_van_speler_aan_zet_schaak(positie)
        return not staat_eigen_koning_schaak

    def is_pakactie(self, positie):
        staat_stuk_op_veld = positie.staat_er_een_stuk_op_dit_veld(self.nieuw_veld)
        if staat_stuk_op_veld:
            return True
        else:
            return False

    def verplaats_stuk_in_positie(self, positie):
        #update veldbezetting in positie
        stuk = positie.krijg_stuk_op_veld(self.oud_veld)
        positie.veldbezetting[self.oud_veld] = None
        positie.veldbezetting[self.nieuw_veld] = stuk
        stuk.heeft_al_eens_bewogen = True

    def pak_op_veld_in_positie(self, positie):
        # Verwijder het gepaktestuk van de lijst met actieve stukken
        gepakte_stuk = positie.krijg_stuk_op_veld(self.nieuw_veld)
        positie.actieve_stukken.remove(gepakte_stuk)
        # Verplaats het pakkende stuk
        self.verplaats_stuk_in_positie(positie)

    def staat_koning_van_speler_aan_zet_schaak(self, positie):
        # krijg veld van koning
        koning_coord = positie.krijg_koningspositie_van_speler(positie.speler_aan_zet)
        # krijg stukken van andere speler
        speler_niet_aan_zet = positie.krijg_andere_speler(positie.speler_aan_zet)
        stukken_andere_speler = positie.krijg_alle_stukken_van_speler(speler_niet_aan_zet)
        # kijk voor alle stukken van tegenstander of deze de koning zien
        for stuk in stukken_andere_speler:
            stuk_zicht = stuk.krijg_zicht_in_positie(positie)
            if koning_coord in stuk_zicht:
                # stuk ziet koning, koning staat schaak
                return True
        # als we hier zijn, zijn alle stukken gecheckt en staat koning niet schaak
        return False




