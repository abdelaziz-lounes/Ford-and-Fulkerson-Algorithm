import networkx as nx  # Importer la bibliotheque NetworkX pour la manipulation de graphes
import matplotlib.pyplot as plt  # Importer Matplotlib pour dessiner le graphe
from collections import defaultdict  # Importer defaultdict pour creer des dictionnaires avec valeurs par defaut

# Utiliser tkinter pour ouvrir un explorateur de fichiers (uniquement en local, pas sur Colab)
try:
    from tkinter import Tk
    from tkinter.filedialog import askopenfilename
except ImportError:
    Tk, askopenfilename = None, None  # tkinter n'est pas disponible sur Colab ou certaines installations


# Classe qui represente un graphe oriente avec des capacites sur les aretes
class Graphe:

    def __init__(self, sommets):
        # Utilisation de defaultdict pour representer le graphe sous forme de liste d'adjacence
        # Chaque sommet u est lie a ses voisins v avec une capacite correspondante
        self.graphe = defaultdict(dict)
        self.V = sommets  # Nombre de sommets dans le graphe (sert juste a titre indicatif)


    # Fonction pour ajouter une arete entre deux sommets avec une capacite donnee
    def ajouter_arete(self, u, v, capacite):
      self.graphe[u][v] = capacite  # Ajoute une arete allant de u a v avec la capacite specifiee
      # Assurez-vous que l'arete inverse est ajoutee avec une capacite de 0
      if v not in self.graphe or u not in self.graphe[v]:
          self.graphe[v][u] = 0  # Capacite inverse initialisee a 0


    # Fonction BFS (Recherche en largeur) pour trouver un chemin augmentant
    # Cette fonction cherche un chemin de la source au puits en utilisant les capacites residuelles
    def bfs(self, source, puits, parent):
        visite = {i: False for i in self.graphe}  # Dictionnaire pour marquer les sommets visites
        file = [source]  # Initialisation de la file avec la source comme premier element
        visite[source] = True  # Marquer la source comme visitee

        # Boucle de parcours en largeur
        while file:
            u = file.pop(0)  # Extraire le premier element de la file

            # Parcourir les voisins de u
            for v, capacite in self.graphe[u].items():
                # Si v n'a pas ete visite et que l'arete u -> v a une capacite residuelle positive
                if not visite[v] and capacite > 0:
                    file.append(v)  # Ajouter v a la file pour traitement ulterieur
                    visite[v] = True  # Marquer v comme visite
                    parent[v] = u  # Enregistrer d'où l'on vient (le parent de v est u)
                    # Si on atteint le puits, retourner True pour indiquer qu'un chemin a ete trouve
                    if v == puits:
                        return True
        # Si on n'a pas trouve de chemin vers le puits, retourner False
        return False


    # Implementation de l'algorithme de Ford-Fulkerson pour calculer le flot maximal
    def ford_fulkerson(self, source, puits):
        parent = {}  # Dictionnaire pour enregistrer le chemin trouve par BFS
        flot_maximal = 0  # Initialiser le flot maximal a zero

        # Repeter tant qu'il existe un chemin augmentant
        while self.bfs(source, puits, parent):
            # Trouver le flot minimal le long du chemin trouve
            flot_chemin = float('Inf')  # Initialiser a une grande valeur (l'infini)
            s = puits  # On commence par le puits et on remonte vers la source

            # Remonter le chemin depuis le puits jusqu'a la source pour trouver la capacite minimale
            while s != source:
                flot_chemin = min(flot_chemin, self.graphe[parent[s]][s])  # Mise a jour du flot minimal
                s = parent[s]  # Continuer a remonter vers la source

            # Mettre a jour les capacites residuelles le long du chemin
            v = puits
            while v != source:
                u = parent[v]
                self.graphe[u][v] -= flot_chemin  # Reduire la capacite dans le sens direct
                # Ajouter cette capacite dans le sens inverse pour permettre un eventuel flux inverse
                self.graphe[v][u] = self.graphe.get(v, {}).get(u, 0) + flot_chemin
                v = parent[v]  # Continuer a remonter vers la source

            # Ajouter le flot du chemin trouve au flot maximal
            flot_maximal += flot_chemin

        # Retourner le flot maximal une fois qu'il n'existe plus de chemin augmentant
        return flot_maximal


    # Fonction pour visualiser le graphe avec NetworkX et Matplotlib
    def visualiser_graphe(self):
        G = nx.DiGraph()  # Creer un graphe oriente avec NetworkX

        # Ajouter les aretes au graphe NetworkX avec les capacites comme poids
        for u in self.graphe:
            for v in self.graphe[u]:
              if self.graphe[u][v] > 0:  # Ajouter uniquement les aretes avec une capacite positive
                G.add_edge(u, v, weight=self.graphe[u][v])  # Ajouter chaque arete u -> v avec sa capacite

        pos = nx.spring_layout(G)  # Calculer la disposition des sommets pour une meilleure presentation

        # Dessiner les sommets et les aretes du graphe
        plt.figure(figsize=(10, 7))  # Definir la taille de la figure
        nx.draw(G, pos, with_labels=True, node_size=1500, node_color="skyblue", font_size=15, font_weight="bold", arrows=True)

        # Ajouter les etiquettes des capacites sur les aretes
        labels = nx.get_edge_attributes(G, 'weight')  # Recuperer les capacites des aretes
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)  # Afficher les capacites sur le graphe

        # Afficher le graphe
        plt.title("Visualisation du graphe")
        plt.show()  # Afficher la figure


    def visualiser_capacites_residuelles(self):
      """affiche le graphe avec les capacites residuelles apres execution du ford-fulkerson"""
      G = nx.DiGraph()  # Creer un graphe oriente avec NetworkX

      # Ajouter les aretes et les capcites residuelles au graphe
      for u in self.graphe:
        for v, capacite in self.graphe[u].items():
          if capacite > 0:  # Ajouter uniquement les aretes avec une capacite residuelle positive
            G.add_edge(u, v, weight=capacite)  # Ajouter chaque arete u -> v avec sa capacite
      
      pos = nx.spring_layout(G)  # Calculer la disposition des sommets pour une meilleure presentation
      plt.figure(figsize=(10, 7))  # Definir la taille de la figure
      nx.draw(G, pos, with_labels=True, node_size=1500, node_color="skyblue", font_size=15, font_weight="bold", arrows=True)

      #Ajouter les capacites redsiduelles comme etiquettes sur les arettes
      labels = nx.get_edge_attributes(G, 'weight')  # Recuperer les capacites des aretes
      nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)  # Afficher les capacites sur le graphe

      plt.title("Visualisation du graphe avec les capacites residuelles")
      plt.show()  # Afficher la figure


# Fonction pour lire les aretes et capacites depuis un fichier texte
def lire_graphe_fichier(fichier_televerse):
  # Ouvrir et lire le fichier
  try:
      with open(fichier_televerse, 'r') as fichier:
          lignes = fichier.readlines()  # Lire toutes les lignes du fichier
  except FileNotFoundError:
      print(f"Le fichier '{fichier_televerse}' n'a pas ete trouve.")
      return [], 0

  aretes = []  # Liste pour stocker les aretes
  sommets = set()  # Ensemble pour stocker tous les sommets uniques

  # Parcourir chaque ligne du fichier pour extraire les sommets et les capacites
  for ligne in lignes:
      u, v, capacite = ligne.strip().split()  # Separer les informations par espaces
      capacite = int(capacite)  # Convertir la capacite en entier
      aretes.append((u, v, capacite))  # Ajouter l'arete a la liste des aretes
      sommets.add(u)  # Ajouter les sommets a l'ensemble pour les compter
      sommets.add(v)  # Ajouter v a l'ensemble pour s'assurer que tous les sommets sont inclus

  # Retourner la liste des aretes et le nombre de sommets uniques
  return aretes, len(sommets)

# Programme principal
if __name__ == "__main__":
     # Selection du fichier avec tkinter si possible, sinon demande par input
    nom_fichier = None
    if Tk and askopenfilename:
        Tk().withdraw()  # Masquer la fenetre principale de tkinter
        nom_fichier = askopenfilename(title="Selectionnez votre fichier texte de graphe",
                                      filetypes=[("Fichiers texte", "*.txt"), ("Tous les fichiers", "*.*")])

    if not nom_fichier:  # Si pas de fichier selectionne avec tkinter, demande manuelle
        nom_fichier = input("Entrez le chemin du fichier de graphe (ex: graphes.txt) : ")

    # Lire le graphe depuis le fichier texte
    aretes, nombre_sommets = lire_graphe_fichier(nom_fichier)

    if not aretes:
        print("Le fichier n'a pas pu etre lu ou est vide.")
    else:
      # Creer un objet Graphe
      g = Graphe(nombre_sommets)

      # Ajouter les aretes au graphe
      for u, v, capacite in aretes:
          g.ajouter_arete(u, v, capacite)

    # Visualiser le graphe avant de calculer le flot
    g.visualiser_graphe()

    # Calculer et afficher le flot maximal possible entre la source et le puits
    source = input("Entrez le sommet source : ")
    puits = input("Entrez le sommet puits : ")

    print(f"\n Le flot maximal possible est {g.ford_fulkerson(source, puits)}\n\n")
    
    g.visualiser_capacites_residuelles() #visualisation des capacites residueles aprs calcul
