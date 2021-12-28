from veld.veldbasis import VeldBasis
import pygame

class GetekendVeld(VeldBasis):
    """Een veld dat op het scherm getekend kan worden"""
    def __init__(self, scherm, schermpositie_x, schermpositie_y, vakjesgrootte, kleur):
        self._vorm
        self._schermpositie_x = schermpositie_x
        self._schermpositie_y = schermpositie_y
        self._vakgrootte = vakjesgrootte
        self._vorm = self._teken_veld(scherm, schermpositie_x, schermpositie_y, vakjesgrootte, vakjesgrootte, kleur)

    def _teken_veld(self, scherm, positie_x, positie_y, breedte, hoogte, kleur):
        return pygame.draw.rect(scherm, kleur, (positie_x, positie_y, breedte, hoogte))

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
        x = self.schermpositie_y + self._vakgrootte / 2