from enum import Enum

from combattant import Combattant


class ZoneAttaque(Enum):
    NON_CIBLE = 0
    TETE = 1
    BRAS = 2
    JAMBE = 3


class Attaque:
    zone : ZoneAttaque = ZoneAttaque.NON_CIBLE

    def __init__(self, nom : str, pa : int, combattant : Combattant = None):
        self.nom = nom
        self.pa = pa
        self.combattant = combattant

class AttaqueTete(Attaque):
    zone = ZoneAttaque.TETE

class AttaqueBras(Attaque):
    zone = ZoneAttaque.BRAS

class AttaqueJambe(Attaque):
    zone = ZoneAttaque.JAMBE
