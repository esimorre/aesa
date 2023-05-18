from typing import List

from combattant import Combattant


class Partie:
    def __init__(self, nom : str):
        self.nom = nom
        self.combattants : List[Combattant] = []
