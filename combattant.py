
class Combattant:
    def __init__(self, nom : str, qj=0): #TODO params valeurs par defaut
        self.nom = nom
        self.a_joue = False
        self.sante = 100.0 #TODO make prop
        self.vitesse_base = 30
        self.agilite_base = 30
        self.encombrement_total = 0
        self.precision = 30
        self.force = 40
        self.qj = qj
        self.rvj = max(0, (self.qj - 4)**2)
        self.buff = 0

        self.etats = set()

    @property
    def initiative(self):
        return self.vitesse_reelle + self.points_action * 10
    @property
    def vitesse_reelle(self):
        return self.vitesse_base - self.encombrement_reel - self.rvj
    @property
    def agilite_reelle(self):
        return self.agilite_base - self.encombrement_reel
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

        pa = int(pa * self.sante / 100)
        pa += self.buff # TODO ordre de calcul ??

        return pa
    @property
    def encombrement_reel(self):
        return self.encombrement_total - self.force / 10
