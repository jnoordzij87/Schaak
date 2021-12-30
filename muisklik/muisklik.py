import pygame
import globale_variabelen
from stukken.stuk import Stuk
from veld.getekendveld import GetekendVeld
from zet.zet import Zet

class Muisklik():
    def __init__(self):
        pass

    def BehandelKlikGebeurtenis(self, event):
        if globale_variabelen.schaakmat == True:
            # bij een klikgebeurtenis na schaakmat: sluit spel af
            pygame.quit()
        # kijk waar op het scherm er is geklikt
        klikX, klikY = event.pos
        # vind uit welk veld is aangeklikt
        for veld in globale_variabelen.huidige_positie.bord.getekende_velden.values():
            if veld.vorm.collidepoint(klikX, klikY):
                # geselecteerde veld gevonden!
                self.BehandelVeldGeselecteerd(veld)

    def BehandelVeldGeselecteerd(self, veld: GetekendVeld):
        # kijk of er een stuk op het aangeklikte veld staat
        positie = globale_variabelen.huidige_positie
        stuk_op_veld = positie.staat_er_een_stuk_op_dit_veld(veld.coordinaat)
        if stuk_op_veld:
            # er is een stuk aangeklikt. behandel
            aangeklikte_stuk = positie.krijg_stuk_op_veld(veld.coordinaat)
            self.BehandelStukGeselecteerd(aangeklikte_stuk, veld)
        else:
            # er is een leeg veld aangeklikt
            # kijk of het om een verplaats actie gaat
            if self.IsVerplaatsActie(veld):
                # is verplaats actie. voer de verplaatsing uit
                geselecteerde_stuk = globale_variabelen.geselecteerdeStuk
                nieuw_veld = veld.coordinaat
                Zet(geselecteerde_stuk, nieuw_veld, positie).doe_zet()
            elif self.WasErEenStukGeselecteerd():
                # er is een veld aangeklikt dat niet tot de mogelijkheden van het geselecteerde stuk behoort
                # de-selecteer het stuk
                self.DeSelecteer()
            else:
                # er is een leeg veld aangeklikt, maar er was ook geen geselecteerd suk. doe niets
                pass

    def BehandelStukGeselecteerd(self, stuk: Stuk, veld: GetekendVeld):
        # we komen hier zowel bij een pakactie als bij gewone stukselectie, herken onderscheid
        if Muisklik().IsPakActie(stuk, veld):
            positie = globale_variabelen.huidige_positie
            vorige_geselecteerde_stuk = globale_variabelen.geselecteerdeStuk
            Zet(vorige_geselecteerde_stuk, veld.coordinaat, positie).doe_zet()
        else:
            # geen pakaktie, selecteer het nieuwe geselecteerde stuk
            self.Selecteer(stuk)

    def IsVerplaatsActie(self, veld: GetekendVeld):
        # kijk of er een stuk was geselecteerd
        if not self.WasErEenStukGeselecteerd():
            # er was geen stuk geselecteerd. kan dus ook geen verplaats actie zijn
            return False
        else:
            # er was een stuk geselecteerd. kan het geselecteerde stuk naar aangeklikte veld?
            positie = globale_variabelen.huidige_positie
            geselecteerde_stuk = globale_variabelen.geselecteerdeStuk
            kan_stuk_naar_veld = geselecteerde_stuk.kan_stuk_naar_veld(veld.coordinaat, positie)
            if kan_stuk_naar_veld:
                # is verplaats actie
                return True
            else:
                # geen verplaats actie
                return False

    def IsPakActie(self, aangeklikt_stuk: Stuk, aangeklikt_veld : GetekendVeld):
        if not self.WasErEenStukGeselecteerd():
            # als er geen stuk geselecteerd was kan het nooit gaan om een pakactie
            return False
        else:
            # er was een stuk geselecteerd
            # kijk of het vorige geselecteerde stuk het huidige geselecteerde stuk kan pakken
            vorig_geselecteerde_stuk = globale_variabelen.geselecteerdeStuk
            positie = globale_variabelen.huidige_positie
            if Zet(vorig_geselecteerde_stuk, aangeklikt_veld.coordinaat, positie).is_zet_geldig():
                return True
            else:
                return False

    def WasErEenStukGeselecteerd(self):
        return globale_variabelen.geselecteerdeStuk != None

    def Selecteer(self, stuk):
        # sta selectie alleen toe als het stuk van de speler aan zet is
        speler_aan_zet = globale_variabelen.huidige_positie.speler_aan_zet
        if stuk.is_stuk_van_speler(speler_aan_zet):
            # selectie toegestaan
            # wijs het stuk aan als het geselecteerde stuk
            globale_variabelen.geselecteerdeStuk = stuk
        else:
            # we mogen dit stuk niet selecteren. Behandel als deselectie-actie
            self.DeSelecteer()

    def DeSelecteer(self):
        globale_variabelen.geselecteerdeStuk = None