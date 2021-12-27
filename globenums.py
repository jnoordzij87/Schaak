#globale enums
from enum import Enum

class vakjeskleuren(Enum):
    wit = (255, 255, 255)
    blauw = (0, 0, 128)
    groen = (0, 255, 0)
    rood = (255, 0, 0)

class Spelers(Enum):
    Wit = 1
    Zwart = 2

class StukKleur(Enum):
    Wit = 1
    Zwart = 2

class StukType(Enum):
    Koning = 1
    Dame = 2
    Toren = 3
    Loper = 4
    Paard = 5
    Pion = 6

class Richtingen(Enum):
    Boven = 1
    Onder = 2
    Rechts = 3
    Links = 4
    LinksBoven = 5
    LinksOnder = 6
    RechtsBoven = 7
    RechtsOnder = 8