class VeldBasis:
    def __init__(self, coordinaat, kleur):
        self._coordinaat = coordinaat
        self._kleur = kleur
        pass

    @property
    def coordinaat(self):
        """Tekstuele coordinaat van het veld, bijvoorbeeld 'A1'"""
        return self._coordinaat

    @property
    def kleur(self):
        """Toepassing van de globale enum veldkleur"""
        return self._kleur