from enum import Enum

from attaque import Attaque
from combattant import Combattant

class Angle(Enum):
    FACE = 0
    FACE_NEGLIGEE = 1
    FLANC = 2
    MORT = 3


class Coup:
    def __init__(self, cible : Combattant, attaque: Attaque):
        self.attaquant = attaque.combattant
        self.cible = cible
        self.attaque = attaque
        self.angle = 0
        self.j20 = 0

    def execute(self, j20=0, angle : Angle = Angle.FACE):
        print('--> Coup porté par %s sur %s lors d''une attaque %s' %
              (self.attaquant.nom, self.cible.nom, self.attaque.nom))
