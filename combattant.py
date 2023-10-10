from etat import Etat
from enum import Enum

class EquipeCombattant(Enum):
    ALLIE = 1
    ENNEMI = 2

class Combattant:
    def __init__(self, nom : str, qa=0, qc=0, qb=0, qj=0): #TODO params valeurs par defaut
        self.nom = nom
        self.equipe = EquipeCombattant.ENNEMI # équipe ennemie par défaut
        self.a_joue = False
        self.robustesse = 45
        self.endurance_base = 30
        self.sante = 100.0 #TODO make prop ; DONE mais à vérifier
        self.vitesse_base = 30
        self.agilite_base = 30
        self.encombrement_total = 0
        self.precision = 30
        self.force = 40
        self.qa = qa # Qualité de l'Armure
        self.qc = qc # Qualité du Casque
        self.qb = qb # Qualité de la protection des Bras
        self.qj = qj # Qualité de la protection des Jambes
        self.rvj = max(0, (self.qj - 4)**2)
        self.buffpa = 0
        self.pm = 0 # Points de Magie
        self.points_esquive = 0 # Points d'Action investis dans l'esquive
        self.nb_esquive = 0 # Nombre d'esquives du tour # TODO : à réinitialiser à chaque tour
        self.pad = 0 # Points d'Action à déduire, incrémentée en combat
        self.points_parade = 0 # Points d'Action investis dans la parade
        self.nb_parade = 0 # Nombre de parades du tour
        self.bonus_parade = 0
        self.taille = 1 # Taille du combattant en hexagones
        self.resistancemagique = 0
        self.paab = 0 # Points d'Action Anti-Brûlure
        self.malusforce = 0
        self.malusagilite = 0
        self.malusprecision = 0
        self.rampant = False
        self.srp = 999 # Seuil de Résistance de Parade, à 999 si sans arme
        # TODO : ajouter :
        '''
        tous les champs de diminution de dégâts ou de jets des différentes protections :
        armure principale, bras, jambes, casque...
        ayant pour valeur par défaut un calcul à partir des champs qa/qc/qb/qj,
        mais pouvant être entrés librement.
        Comment écrire ces champs ?
        '''

        self.etats = set()

    @property
    def initiative(self):
        return self.vitesse_reelle + self.points_action * 10

    @property
    def pv(self):
        return self.robustesse
        #TODO : les PV sont égaux à la robustesse pour un combattant en pleine santé mais doivent diminuer indépendamment, comment faire ?
    @property
    def vitesse_reelle(self):
        return self.vitesse_base - self.encombrement_reel - self.rvj
    @property
    def agilite_reelle(self):
        return self.agilite_base - self.encombrement_reel
    @property
    def endurance_reelle(self):
        return self.endurance_base - self.encombrement_reel
    @property
    def points_action(self):
        pa = 1
        ar_vr = self.agilite_reelle + self.vitesse_reelle
        if ar_vr > 4: pa +=1
        if ar_vr > 9: pa +=1
        if ar_vr > 19: pa +=1
        if ar_vr > 29: pa +=1
        if ar_vr > 44: pa +=1
        if ar_vr > 59: pa +=1
        if ar_vr > 79: pa +=1
        if ar_vr > 99: pa +=1
        if ar_vr > 159: pa += (self.agilite_reelle + self.vitesse_reelle -120) / 40
            # TODO : pourquoi ne pas mettre juste (ar_vr - 120)/40 ??
            # RXIMore >> tu es sûr que ça revient au même ? faut écrire des tests pour ça ;)

        pa = int(pa * self.sante / 100)
        pa += self.buffpa # TODO ordre de calcul ??
                        # TODO le buff PA est le nb de PA ajouté manuellement par l'utilisateur, donc en dernier dans le calcul
        return pa
    @property
    def encombrement_reel(self):
        return self.encombrement_total - self.force / 10
    @property
    def dsa(self): # Diminution du Seuil d'Affaiblissement
        return max(0, (self.endurance_reelle - 38)/2)
    @property
    def sa(self): #SEUIL D'AFFAIBLISSEMENT : pourcentage de pv sous lequel la santé et les PA diminuent
        return 50 - self.dsa
    @property
    def sante(self):
        return min(100, self.pv*100 / (self.sa * self.robustesse / 100))
        #TODO erreur dans les spec !! corrigée ci-dessus
    @property
    def pat(self):
        return self.points_action - self.pad
    ''' PAT = Points d'Action temporaires '''
    @property
    def pesq(self):
        return int(2 + max(0, (self.endurance_reelle - 20)/20)) - self.nb_esquive
        ''' PESQ = Possibilités d'Esquive '''
        # TODO le champ doit pouvoir être modifié indépendamment
    @property
    def mje(self):
        return int(self.points_esquive + (self.agilite_reelle - 30) / 5)
        ''' MJE = Modificateur de Jet d'Esquive '''

    @property
    def ppar(self):
        return int(2 + max(0, (self.endurance_reelle - 20) / 20)) - self.nb_parade
        ''' PPAR = Possibilités de Parade '''
        # TODO le champ doit pouvoir être modifié indépendamment
    @property
    def cdh(self):
        return 30 / self.vitesse_reelle
        ''' CDH = Coût de Déplacement par Hexagone '''
        # TODO : affichage sous forme de fraction
    @property
    def cpf(self):
        return 15 / self.agilite_reelle
        ''' CPF = Coût de Pivotement par Face '''
        # TODO : affichage sous forme de fraction
    @property
    def resistance(self):
        return int(max(0, (self.robustesse - 40) / 10))
        # montant de réduction naturelle des dégâts
    @property
    def ddb(self):
        return int(max(0, self.robustesse - 50))
        ''' DDB = Diminution des Dégâts de Brûlure, exprimée en pourcentage '''
    @property
    def ddh(self):
        return int(max(0, self.robustesse - 50))
        ''' DDH = Diminution des Dégâts d'Hémorragie, exprimée en pourcentage '''
    @property
    def djb(self):
        return int(max(0, (self.robustesse - 40)/15))
        ''' DJB = Diminution du Jet de Brûlure '''
    @property
    def djh(self):
        return int(max(0, (self.robustesse - 40) / 20))
        ''' DJH = Diminution du Jet d'Hémorragie '''
    @property
    def djeto(self):
        return int(max(0, (self.robustesse - 40) / 20))
        ''' DJETO = Diminution du Jet d'Etourdissement '''
    @property
    def dja(self):
        return int(max(0, (self.robustesse - 30) / 30))
        ''' DJA = Diminution du Jet d'Assommage '''
    @property
    def djeng(self):
        return int(max(0, (self.robustesse-40)/25) + max(0, (self.endurance_reelle-30)/10))
        ''' DJENG = Diminution du Jet d'Engourdissement des attaques physiques '''
    @property
    def djen(self):
        return int(max(0, (self.force - 30) / 30))
        ''' DJEN = Diminution du Jet d'Entrave '''
    @property
    def djef(self):
        return int(max(0, (self.endurance_reelle - 30) / 10))
        ''' DJEF = Diminution du Jet d'Effroi '''
    @property
    def toursavivre(self):
        return int(5 + max(0, (self.endurance_reelle - 30)/10))
        ''' Nombre de tours restant à vivre à un combattant asphyxié/pétrifié '''
        # TODO : est-ce possible de décrémenter toursavivre si c'est une property ?? le but : le combattant meurt quand toursavivre tombe à zéro

    def ajoutEtat(self, type : str, valeur : int):
        self.etats.add(Etat.create(type, valeur))
#TODO : aucune idée de comment coder ça ! renvoie True s'il y a au moins un état
# #TODO : supprimerEtat
