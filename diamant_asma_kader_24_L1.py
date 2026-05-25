import random
#definition de la classe representant un joueur et son score 
class Joueur:
    def __init__(self, nom, strategy):
        self.coffre = [] # liste d'entier
        self.sac = 0
        self.nom = nom
        self.strategy = strategy
        self.is_active = True

    #la fonction qui renvoie la stratégie d'un joueur
    def play(self, id_manche, rubis_au_sol, les_joueurs, tas_tri, defausse):
        return self.strategy.play(self.coffre, self.sac, rubis_au_sol,id_manche, les_joueurs, tas_tri, defausse)
    
#strategie de decision des joeuurs au hasard          
class RandomStrategy:
    def __init__(self):
        pass
    def play(self,
             mon_coffre, # liste d'entiers de taille nb_manches,stock apres sortie
             mon_sac, # entier : nombre de rubis, stock avant sortie
             rubis_au_sol, # rubis restants à partager
             id_manche, # entier : compris entre 1 et 5 ,il va saisir le nombre de manche
             les_joueurs,    # [ {"coffre":[2,5,0,0,0], "is_active" : True}
                             #,... ,
                             # {"coffre": [0,15,3,0,0], "is_active" : False} ]
             tas_tri, # le tas de cartes restantes (pas dans l'ordre de tirage)
             defausse # ce qui est déjà joué comme cartes,mon affichage de la carte
            ):
        return (random.randint(0, 6)> 4) #true pour sortir

#Strategie pour les joueurs (saisi au clavier) 
class StrategyH:
    def __init__(self):
        pass 
    def play(self, mon_coffre, mon_sac, rubis_au_sol, id_manche, les_joueurs, tas_tri, defausse):
        choix:str = str(input("Stop ou Encore (s / e) ? "))
        while choix != 'e' and choix != 's':
            choix:str = str(input("Stop ou Encore (s / e) ? "))
        if choix == 's':
            return True #pour sortir 
        else:
            return False #pour rester

class StrategyIA:
    def __init__(self):
        pass
    def play(self, mon_coffre, mon_sac, rubis_au_sol, id_manche, les_joueurs, tas_tri, defausse):
        return not self._play(mon_coffre, mon_sac, rubis_au_sol, id_manche, les_joueurs, tas_tri, defausse)
    # Gestion de décision de l'IA(True pour rester et False pour sortir)
    def _play(self, mon_coffre, mon_sac, rubis_au_sol, id_manche, les_joueurs, tas_tri, defausse):
        reliques = ["R_5", "R_7", "R_8", "R_10", "R_12"]
        pieges = ["serpent", "serpent", "serpent",
                  "araignée", "araignée", "araignée",
                  "boulets", "boulets", "boulets",
                  "laves", "laves", "laves",
                  "pics", "pics", "pics"]

        # Comptage des pièges et des reliques dans la défausse
        cpt_relique = sum(1 for carte in defausse if carte in reliques)
        cpt_piege = sum(1 for carte in defausse if carte in pieges)
        
        # Comptage des pièges restants dans le tas de cartes
        nb_pieges_restants = sum(1 for carte in tas_tri if carte in pieges)

        # Détermination de la dernière carte tirée
        derniere_carte = defausse[-1] if defausse else None

        # Logique pour les trois premières manches
        if id_manche < 3:
            #pour le premier tour ou si le sac est encore vide
            if len(defausse) == 0 or mon_sac == 0:
                return True
            if cpt_relique >= 1: #une relique à été ramassée
                return False
            #si la derniere carte est une rubis on reste
            if derniere_carte and (derniere_carte not in pieges) and (derniere_carte not in reliques):
                return True
            #si on a ramassé deux carte piege on sort
            if cpt_piege >= 2:
                return False
            #les rubis au sol sont 4 ou plus
            if rubis_au_sol >= 4:
                return False
            if mon_sac > 10: #si on a ramassée un certain nombre de rubis on sors 
                return False
            #aucun des cas precedent on reste
            return True

        # Logique pour les manches restantes
        else:
            #premier tour 
            if  len(defausse) == 0 or mon_sac == 0:
                return True
            if mon_sac >= 15 :
                return False
            if cpt_piege >= 3:
                return False
            #si les pieges ont diminier apres les autres manches on a moins de risque de rencontrer un piege
            if nb_pieges_restants < 15:
                #une relique à été ramassée on sors
                if cpt_relique >= 1:
                    return False
                if rubis_au_sol >= 5 :
                    return False
                if mon_sac >= 20:
                    return False
                if cpt_piege >= 3:
                    return False
                return True
            return False
            # True



#choix aleatoire des cartes 
def tirage_cartes(cartes:list)->str:
    #on melange les cartes 
    random.shuffle(cartes)
    #on tire une parmis la liste au hasard
    return random.choice(cartes)
 
#fonction qui verifie si  la carte est un entier ou une chaine de caractere
def chaine_caractere(carte)->bool:
    if isinstance(carte, int):
        return False
    else: 
        return True

#ajout d'une relique parmis les cartes 
def ajoutRelique(cartes:list, r:str)->list:
    if r  in cartes:
        pass
    else:
        cartes.append(r)

#fonction qui permet de savoir si ils ont rencontrer des pieges au cours de la manche 
def estPieger(cartes_tirer:list, carte, reliques:list)->bool:
    piege = False
    #si la carte a deja été tirée au cours de cette manche
    if (carte not in reliques and chaine_caractere(carte)) and cartes_tirer.count(carte) == 2 :
        piege = True #piege rencontrer 
    return piege

#suppression d'une carte piege pour la partie
def suppression_pieges(cartes:list(),cartes_tirer:list()):  
    if cartes_tirer.count("serpent") == 2:
        cartes.remove("serpent")
    elif cartes_tirer.count("araignée") == 2:
        cartes.remove("araignée")
    elif cartes_tirer.count("boulets") == 2:
        cartes.remove("boulets")
    elif cartes_tirer.count("pics") == 2:
        cartes.remove("pics")
    elif cartes_tirer.count("laves") == 2:
        cartes.remove("laves")
    
#conversion des reliques en entier 
def convertion_Reliques(r:str())->int:
    if r =="R_5":
        return 5
    elif r == "R_7":
        return 7
    elif r  == "R_8":
        return 8
    elif r == "R_10":
        return 10
    elif r == "R_12":
        return 12

#ramassage d'une relique si un seul decide de sortir 
def ramasseRelique(cartes:list, cartes_tirer:list, relique:list)->int:
    gain = 0
    for carte in cartes_tirer:
        if carte in relique:
            gain += convertion_Reliques(carte)
    return gain
#si une carte piége à été tiré ou non
def supprimeRelique(cartes, carte):
    cartes.remove(carte)
    
#affichage d'une liste de joueurs 
def affichageJoueurs(Joueurs:list):
    for joueur in Joueurs:
        print(Joueurs[joueur].nom, "\n")

#partage des gains apres une manche ou bien à la sortie des joueurs
def PartageGains(Joueurs:list,cartes:list, cartes_tirer:list, joueurs_restants:list,joueurs_sortis:list, cartes_sol:int, relique_sol:int, nbJoueurs:int, carte:int, reliques:list):
    #si un seul joueur decident de sortir 
    if len(joueurs_sortis) == 1 :
        relique_sol += ramasseRelique(carte, cartes_tirer, reliques)
        Joueurs[joueurs_sortis[len(joueurs_sortis) - 1]].sac += relique_sol + cartes_sol 
        relique_sol = 0
        cartes_sol = 0
        for c in reliques:
            if c in cartes_tirer:
                supprimeRelique(cartes_tirer, c)
            if c in cartes:
                supprimeRelique(cartes, c)
    else:
        #si le nombre des joueurs sortant sont plus petit que les cartes au sol 
        #on parcourt la liste des joueurs sortant 
        for joueur in joueurs_sortis:
            Joueurs[joueur].sac += cartes_sol // len(joueurs_sortis) 
            #le reste des cartes au sol 
        cartes_sol = cartes_sol % len(joueurs_sortis)

    #on gere les restants si la carte est une rubis
    if  (not chaine_caractere(carte)) and len(joueurs_restants) > 0:
        #traitemant de ceux qui sont rester
        for joueur in joueurs_restants:
            Joueurs[joueur].sac += carte // len(joueurs_restants) 
        #on met le reste au sol
        #cartes_sol += carte % len(joueurs_restants)
    #on retourne les cartes aux sol, les reliques et les cartes 
    return cartes_sol, relique_sol, cartes
   
   
#deroulement d'une partie de la manche
def partie_manche(Joueurs:list, nbJoueurs:int, cartes:list, reliques:list, id_manche:int):
    # Initialisation des variables
    joueurs_restants = list(range(nbJoueurs)) #au debut de la manche
    cartes_tirer = [] #contient les cartes tirées dans la manche
    relique_sol = 0
    cartes_sol = 0 
    #permet de stoper une manche par apparition de piege ou decision des joueurs
    terminer:bool = True 

    # Tant que la manche n'est pas terminée
    while terminer:
        #vidage de la liste des sortant à chaque tour 
        joueurs_sortis = [] 
        
        # Tirage de la première carte
        carte = tirage_cartes(cartes)
        if not chaine_caractere(carte):
            cartes_sol += carte % len(joueurs_restants)
        print("La carte tirée est", carte)
        #ajout de la carte tiré
        cartes_tirer.append(carte) #si y a pas eu de piege 
        if not estPieger(cartes_tirer, carte, reliques):
            print("\n")
            # Decision de chaque de joueur encore dans la manche
            for joueur in joueurs_restants:
                choix = Joueurs[joueur].play(id_manche, cartes_sol, joueurs_restants, cartes, cartes_tirer)
                if choix :
                    print(Joueurs[joueur].nom, "décide de sortir \n")
                    joueurs_sortis.append(joueur)
                    Joueurs[joueur].is_active = False
                else:
                    Joueurs[joueur].is_active = True
                    print(Joueurs[joueur].nom, "décide de rester\n")
                        #partage des gains entre les joueurs 
            #si personne ne veut continuer 
            if len(joueurs_restants) == 0:
                if len(joueurs_sortis) > 0:
                    cartes_sol, relique_sol,cartes = PartageGains(Joueurs, cartes, cartes_tirer, joueurs_restants, joueurs_sortis, cartes_sol, relique_sol, nbJoueurs, carte, reliques)
            else:
                if len(joueurs_sortis) > 0 :
                    cartes_sol, relique_sol,cartes = PartageGains(Joueurs, cartes, cartes_tirer, joueurs_restants, joueurs_sortis, cartes_sol, relique_sol, nbJoueurs, carte, reliques)
                else:
                    if  (not chaine_caractere(carte)) :
                        #traitemant de ceux qui sont rester
                        for joueur in joueurs_restants:
                            Joueurs[joueur].sac += carte // len(joueurs_restants) #dans le cas où s'est une rubis
            print("\n")
            # Affichage du contenu des sac de tous les joueurs  après chaque partie de la manche en cours 
            for j in range(nbJoueurs):
                print("Après la partie de cette manche,", Joueurs[j].nom, "vous avez gagné", Joueurs[j].sac) 
            print("Les cartes au sol sont ", cartes_sol, "\n")

        
        #sinon les joueurs encore present perd tous leurs gains et la manche se termine
        else:
            for joueur in joueurs_restants:
                Joueurs[joueur].sac = 0
            #Premier cas d'arret 
            terminer = False
        
        #Mise à jour de la liste des joueurs apres decision
        joueurs_restants = [joueur for joueur in joueurs_restants if joueur not in joueurs_sortis]
       
        
        #deuxieme cas d'arret si tout le monde veut sortir 
        if len(joueurs_restants) == 0:
            terminer = False
        print("\n=================================\n")

    # Suppression des pièges tirés
    suppression_pieges(cartes, cartes_tirer)
    print("LES CARTES APRES SUPPRESSION OU NON DES PIEGES  ", cartes, "\n")

    # Ajout des gains des joueurs dans leurs coffres après la manche
    for joueur in range(nbJoueurs):
        Joueurs[joueur].coffre.append(Joueurs[joueur].sac)
        Joueurs[joueur].sac = 0
        Joueurs[joueur].is_active = True
    # Affichage des coffres des joueurs après la manche
    for joueur in range(nbJoueurs):
        print("APRES LA PARTIE DE LA MANCHE VOTRE COFFRE CONTIENT ", Joueurs[joueur].coffre)

    print("\n------------------- FIN DE LA MANCHE -----------------\n")



#la fonction principale du jeu
def jeu(Joueurs:list, nbJoueurs:int):
   
    # Les constantes
    cartes = [1,2,3,4,5,5,7,7,9,11,11,13,14,15,17,
            "serpent","serpent","serpent","araignée","araignée","araignée",
            "boulets","boulets","boulets","laves","laves","laves",
            "pics","pics","pics"]  
    reliques = ["R_5", "R_7", "R_8", "R_10", "R_12"] 
     
    for id_manche in range(5):
        ajoutRelique(cartes, reliques[id_manche])
        print("\n  ----------- MANCHE", id_manche + 1, "----------------- \n")
        print("Les cartes sont :", cartes, "\n")
        partie_manche(Joueurs, nbJoueurs, cartes, reliques, id_manche)

   

#les joueurs avec des strategies differentes
def ens_joueurs(les_joueurs:list)->list:
    IA = StrategyIA()
    joueur2 = RandomStrategy()
    joueur3 = RandomStrategy()
    joueur4 = RandomStrategy()
    joueur5 = RandomStrategy()
    joueur6 = RandomStrategy()
    joueur7 = RandomStrategy()
    joueur8 = RandomStrategy()
    p1 = Joueur("IA",IA)
    p2 = Joueur("j1",joueur2)
    p3 = Joueur("j2",joueur3)
    p4 = Joueur("j3",joueur4)
    p5 = Joueur("j4",joueur5)
    p6 = Joueur("j5",joueur6)
    p7 = Joueur("j6",joueur7)
    p8 = Joueur("j7",joueur8)
    les_joueurs.append(p1)
    les_joueurs.append(p2)
    les_joueurs.append(p3)
    les_joueurs.append(p4)
    les_joueurs.append(p5)
    les_joueurs.append(p6)
    les_joueurs.append(p7)
    les_joueurs.append(p8)



#le programme principale
print("\n\n~~~~~~~~~~~~~~~~~~~~~~~~ BIENVENU DANS LE JEU DIAMANT ~~~~~~~~~~~~~~~~~~~~~~~~~~~\n \n ")

nbJoueurs:int = int(input("Donner le nombre de joueurs qui veulent participer "))
while nbJoueurs < 2: 
    print("Le nombre de joueurs doit être plus grand \n ")
    nbJoueurs:int = int(input("Donner le nombre de joueurs qui veulent participer "))

les_joueurs:list = list()
ens_joueurs(les_joueurs)
#appel de la fonction pour jouer une partie
jeu(les_joueurs, nbJoueurs)

#affichage des scores de chaque joueurs
for j in range(nbJoueurs ):
    print(les_joueurs[j].nom,"a eu",sum(les_joueurs[j].coffre),"rubis ")
print("\n")

#recherche du gagnant de la partie (son score et nom)
max_gagnant = 0
le_gagnant = ""
for j in range(nbJoueurs ):
    if(sum(les_joueurs[j].coffre) > max_gagnant):
        max_gagnant = sum(les_joueurs[j].coffre)
        le_gagnant = les_joueurs[j].nom
    
print("FELICITATIONS",le_gagnant,"VOUS AVEZ GAGNER LA PARTIE EN COLLECTANT",max_gagnant,"RUBIS")










