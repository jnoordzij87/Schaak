from zet.zet import Zet


class Beweging:
    def __init__(self):
        pass

    def krijg_beweegopties_in_positie(self, stuk, positie):
        beweegopties = self.krijg_zicht_in_positie(stuk, positie)
        geldige_opties = []
        for doelveld in beweegopties:
            huidigveld = positie.krijg_veld_van_stuk(stuk)
            is_optie_geldig = Zet(stuk, doelveld, positie).is_zet_geldig()
            if is_optie_geldig:
                geldige_opties.append(doelveld)
        return geldige_opties

    def krijg_zicht_in_positie(self, stuk, positie):
        # wordt overschreven per ervend stuk
        return []

    def _is_veld_geldig_en_niet_bezet(self, stuk, coordinaat, positie):
        is_veld_geldig = self._is_veld_geldig(coordinaat)
        if not is_veld_geldig:
            return False
        is_veld_bezet = self._is_veld_bezet(stuk, coordinaat, positie)
        if is_veld_bezet:
            return False
        else:
            return True

    def _is_veld_geldig(self, coordinaat):
        return coordinaat != None

    def _is_veld_bezet(self, stuk, coordinaat, positie):
        # kijk of het doelveld bezet is door een eigen stuk
        bezet_door_eigen_stuk = self._staat_er_een_stuk_van_zelfde_kleur_op_veld(stuk, coordinaat, positie)
        return bezet_door_eigen_stuk

    #TODO: haal dit weg en schrijf duidelijkere is veld bezet functie
    def _staat_er_een_stuk_van_andere_kleur_op_veld(self, stuk, veld, positie):
        staat_stuk_op_veld = positie.staat_er_een_stuk_op_dit_veld(veld)
        if not staat_stuk_op_veld:
            return False
        else:
            stuk_op_veld = positie.krijg_stuk_op_veld(veld)
            andere_kleur = stuk_op_veld.kleur != stuk.kleur
            return andere_kleur

    # TODO: haal dit weg en schrijf duidelijkere is veld bezet functie
    def _staat_er_een_stuk_van_zelfde_kleur_op_veld(self, stuk, veld, positie):
        staat_stuk_op_veld = positie.staat_er_een_stuk_op_dit_veld(veld)
        if not staat_stuk_op_veld:
            return False
        else:
            stuk_op_veld = positie.krijg_stuk_op_veld(veld)
            zelfde_kleur = stuk_op_veld.kleur == stuk.kleur
            return zelfde_kleur