import globale_enums
from veld.veldbasis import VeldBasis
import pygame

class GetekendVeld(VeldBasis):
    """Een veld dat op het scherm getekend kan worden"""
    def __init__(self, scherm, schermpositie_x, schermpositie_y, vakjesgrootte, coordinaat, kleur):
        super().__init__(coordinaat, kleur)
        self._vorm = None
        self._schermpositie_x = schermpositie_x
        self._schermpositie_y = schermpositie_y
        self._vakgrootte = vakjesgrootte
        self._rgb_kleur = self._converteer_naar_rgb_kleur(kleur)
        self._vorm = self._teken_veld(scherm)


    def _teken_veld(self, scherm):
        posX = self._schermpositie_x
        posY = self._schermpositie_y
        grootte = self._vakgrootte
        kleur = self.rgb_kleur
        return pygame.draw.rect(scherm, kleur, (posX, posY, grootte, grootte))

    @property
    def vorm(self):
        return self._vorm

    @property
    def schermpositie_x(self):
        return self._schermpositie_x

    @property
    def schermpositie_y(self):
        return self._schermpositie_y

    @property
    def middelpunt(self):
        x = self.schermpositie_x + self._vakgrootte / 2
        y = self.schermpositie_y + self._vakgrootte / 2
        return [x,y]

    @property
    def rgb_kleur(self):
        return self._rgb_kleur

    def _converteer_naar_rgb_kleur(self, kleur):
        if kleur == globale_enums.veld_kleuren.wit:
            return globale_enums.veld_rgb_kleuren.wit.value
        if kleur == globale_enums.veld_kleuren.zwart:
            return globale_enums.veld_rgb_kleuren.blauw.value