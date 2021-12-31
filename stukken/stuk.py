from globale_enums import Spelers, StukKleur

class Stuk:
    def __init__(self, stuktype, stukkleur):
        self.stuktype = stuktype
        self.kleur = stukkleur
        self.heeft_al_eens_bewogen = False

    @property
    def eigenaar(self):
        if self.kleur == StukKleur.Wit:
            return Spelers.wit
        if self.kleur == StukKleur.Zwart:
            return Spelers.zwart

    def kan_stuk_naar_veld(self, coordinaat, positie):
        stukopties = self.krijg_beweegopties_in_positie(positie)
        is_mogelijk = coordinaat in stukopties
        return is_mogelijk

    def krijg_beweegopties_in_positie(self, positie):
        #wordt overschreven per ervend stuk
        return []

    def krijg_zicht_in_positie(self, positie):
        # wordt overschreven per ervend stuk
        return []

    def is_stuk_van_speler(self, speler : Spelers):
        return self.eigenaar == speler
