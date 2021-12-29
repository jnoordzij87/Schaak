from stukken.stuk import Stuk
import globale_variabelen


class Beweging:
    def __init__(self):
        self._bewegingsrichtingen = self.krijg_bewegingsrichtingen()
        pass

    def krijg_bewegingsrichtingen(self):
        #overschrijf per stuk
        pass

    def _is_veld_geldige_optie_voor_stuk(self, stuk, coordinaat, positie):
        if coordinaat == None:
            #het veld is niet geldig (buiten rand van bord)
            return False
        bezet_door_eigen_stuk = self._staat_er_een_stuk_van_zelfde_kleur_op_veld(stuk, coordinaat, positie)
        if bezet_door_eigen_stuk:
            return False
        else:
            return True

    def _staat_er_een_stuk_van_andere_kleur_op_veld(self, stuk, veld, positie):
        staat_stuk_op_veld = positie.staat_er_een_stuk_op_dit_veld(veld)
        if not staat_stuk_op_veld:
            return False
        else:
            stuk_op_veld = positie.krijg_stuk_op_veld(veld)
            andere_kleur = stuk_op_veld.kleur != stuk.kleur
            return andere_kleur

    def _staat_er_een_stuk_van_zelfde_kleur_op_veld(self, stuk, veld, positie):
        staat_stuk_op_veld = positie.staat_er_een_stuk_op_dit_veld(veld)
        if not staat_stuk_op_veld:
            return False
        else:
            stuk_op_veld = positie.krijg_stuk_op_veld(veld)
            zelfde_kleur = stuk_op_veld.kleur == stuk.kleur
            return zelfde_kleur