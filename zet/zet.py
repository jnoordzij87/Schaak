from globale_enums import StukType
import copy

class Zet():
    def __init__(self, positie, oud_veld, nieuw_veld):
        self.positie = positie
        self.oud_veld = oud_veld
        self.nieuw_veld = nieuw_veld
        self.stuk = positie.krijg_stuk_op_veld(oud_veld)

    def is_zet_geldig(self):
        """Checkt of een zet uitgevoerd mag worden"""
        hypothetische_positie = copy.copy(self.positie)
        self.doe_zet_in_positie(hypothetische_positie)
        self.is_positie_geldig(hypothetische_positie)
        pass

    def is_positie_geldig(self, positie):
        return self.staat_koning_van_huidige_speler_schaak(positie)

    def staat_koning_van_huidige_speler_schaak(self, positie):
        #krijg veld van koning
        koning_coord = None
        for stuk in positie.krijg_alle_stukken_van_speler(positie.speler_aan_zet):
            if stuk.stuktype == StukType.Koning:
                koning_coord = positie.krijg_veld_van_stuk(stuk)
        #kijk voor alle stukken van tegenstander of deze de koning zien
        for stuk in positie.krijg_alle_stukken_van_speler(positie.krijg_andere_speler(positie.speler_aan_zet)):
            if koning_coord in stuk.krijg_beweegopties_in_positie(positie, controleer_schaak = False):
                #stuk ziet koning
                return True

    def is_pakactie(self):
        staat_stuk_op_nieuw_veld = self.positie.staat_er_een_stuk_op_dit_veld(self.nieuw_veld)
        if staat_stuk_op_nieuw_veld:
            return True
        else:
            return False

    def doe_zet_in_positie(self, positie):
        if self.is_pakactie():
            self.pak_op_veld_in_positie(positie)
        else:
            self.verplaats_stuk_in_positie(positie)

    def verplaats_stuk_in_positie(self, positie):
        #update veldbezetting in positie
        positie.veldbezetting[self.oud_veld] = None
        positie.veldbezetting[self.nieuw_veld] = self.stuk

    def pak_op_veld_in_positie(self, positie):
        # Verwijder het gepaktestuk van de lijst met actieve stukken
        gepakte_stuk = positie.krijg_stuk_op_veld(self.nieuw_veld)
        positie.actieve_stukken.remove(gepakte_stuk)
        # Verplaats het pakkende stuk
        self.verplaats_stuk_in_positie(positie)






