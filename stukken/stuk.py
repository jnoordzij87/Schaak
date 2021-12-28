from globale_enums import Spelers, Lineaire_Richtingen, StukKleur, StukType

class Stuk:
    def __init__(self, stuktype, stukkleur, veld):
        self._beweegrichtingen = None
        self.stuktype = stuktype
        self.kleur = stukkleur
        self.heeft_al_eens_bewogen = False

    @property
    def beweegrichtingen(self) -> list(Lineaire_Richtingen):
        return self._beweegrichtingen

    def is_stuk_van_speler(self, speler : Spelers):
        eigenaar = self.krijg_eigenaar_van_stuk()
        return eigenaar == speler

    def krijg_eigenaar_van_stuk(self):
        if self.kleur == StukKleur.Wit:
            return Spelers.wit
        if self.kleur == StukKleur.Zwart:
            return Spelers.zwart