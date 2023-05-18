from coup import Coup


class Etat:
    nom = None
    def __init__(self, value=0):
        self.ampleur = value

    @classmethod
    def create(cls, nom, value):
        if nom == 'ETO': return EtatETO(value)

        return None

    def effet_cible(self, coup : Coup):
        pass

    def effet_attaquant(self, coup: Coup):
        pass


class EtatETO(Etat):
    nom = 'ETO'
    label = 'Etourdissement' # TODO ?? préciser des noms "parlants"

# TODO add Etatxxx classes