from .lineaire_beweging import LineaireBeweging
from globale_enums import Lineaire_Richtingen

class LoperBeweging(LineaireBeweging):
    def __init__(self):
        super().__init__()
        pass

    @property
    def bewegingsrichtingen(self):
        richtingen = [
            Lineaire_Richtingen.RechtsOnder,
            Lineaire_Richtingen.RechtsBoven,
            Lineaire_Richtingen.LinksBoven,
            Lineaire_Richtingen.LinksOnder]
        return richtingen

