import unittest

from attaque import AttaqueTete
from combattant import Combattant
from coup import Coup, Angle
from etat import EtatETO
from partie import Partie


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_coup(self):
        '''
        Un Use Case peut être implémenté dans une méthode de test TestCase
        :return: None
        '''
        gob1 = Combattant('Gobelin1')
        gob2 = Combattant('Gobelin2')

        gob1_pa = gob1.points_action
        self.assertEqual(gob1_pa , 6, "point d'action par défaut à 6 (TODO: buff NYI)")

        gob1.etats.add((EtatETO(20)))
        #gob2.etats.add((EtatETO(10))) on fait une méthode pour ça
        gob2.ajoutEtat('ETO', 10)

        with self.assertRaises(RuntimeError):
            gob1.ajoutEtat('Etat bidon', 40)

        p = Partie('test partie 1')
        p.combattants.append(gob1)
        p.combattants.append(gob2)

        gob1_attaq = AttaqueTete('fulguro-poing', pa=12, combattant=gob1)

        coup = Coup(cible=gob2, attaque=gob1_attaq)
        coup.execute(j20=12, angle=Angle.FLANC)


if __name__ == '__main__':
    unittest.main()
