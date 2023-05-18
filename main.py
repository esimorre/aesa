from attaque import AttaqueTete
from combattant import Combattant
from coup import Coup, Angle
from partie import Partie
from etat import EtatETO

if __name__ == '__main__':
    print('Hello AESA')
    gob1 = Combattant('Gobelin1')
    gob2 = Combattant('Gobelin2')

    gob1.etats.add((EtatETO(20)))
    gob2.etats.add((EtatETO(10)))

    p = Partie('test partie 1')
    p.combattants.append(gob1)
    p.combattants.append(gob2)

    gob1_attaq = AttaqueTete('fulguro-poing', pa=12, combattant=gob1)

    coup = Coup(cible=gob2, attaque=gob1_attaq)
    coup.execute(j20=12, angle=Angle.FLANC)

