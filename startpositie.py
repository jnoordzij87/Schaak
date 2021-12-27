from positie import Positie
from bord import Bord
import globale_enums
from stukken.pion import Pion
from stukken.loper import Loper
from stukken.dame import Dame
from stukken.koning import Koning
from stukken.toren import Toren

class StartPositie(Positie):
    def __init__(self, bord : Bord):
        super().__init__(bord)
        pass

    def _maak_startpositie(self):
        for veld in self.bord.velden:
            coord = veld.coordinaat
            stuk = None
            if coord == 'A1' or coord == 'H1':
                stuk = Toren(globale_enums.StukKleur.Wit, veld)
            if coord == 'A8' or coord == 'H8':
                stuk = Toren(globale_enums.StukKleur.Zwart, veld)
            if coord == 'E1':
                stuk = Koning(globale_enums.StukKleur.Wit, veld)
            if coord == 'E8':
                stuk = Koning(globale_enums.StukKleur.Zwart, veld)
            if coord == 'D8':
                stuk = Dame(globale_enums.StukKleur.Zwart, veld)
            if coord == 'D1':
                stuk = Dame(globale_enums.StukKleur.Wit, veld)
            if coord == 'C1' or coord == 'F1':
                stuk = Loper(globale_enums.StukKleur.Wit, veld)
            if coord == 'C8' or coord == 'F8':
                stuk = Loper(globale_enums.StukKleur.Zwart, veld)
            if '2' in coord:
                stuk = Pion(globale_enums.StukKleur.Wit, veld)
            if '7' in coord:
                stuk = Pion(globale_enums.StukKleur.Zwart, veld)

            #voeg het stuk toe aan de stukkenlijst
            if stuk != None:
                self.stukken_in_het_spel.append(stuk)
                self.veldbezetting[coord] = stuk