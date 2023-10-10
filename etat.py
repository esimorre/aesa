
class Etat:
    nom = None
    def __init__(self, value=0):
        self.ampleur = value

    @classmethod
    def create(cls, nom : str, value : int | float):
        if nom == 'ETO': return EtatETO(value)

        raise RuntimeError("Etat %s non reconnu" % nom)

    def effet_cible(self, coup):
        pass

    def effet_attaquant(self, coup):
        pass


class EtatETO(Etat):
    nom = 'ETO'
    label = 'Etourdissement' # TODO ?? préciser des noms "parlants"

# TODO add Etatxxx classes