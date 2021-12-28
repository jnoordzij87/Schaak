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