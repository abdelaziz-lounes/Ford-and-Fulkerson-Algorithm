# Calcul de Flot Maximal avec l'Algorithme de Ford-Fulkerson
Ce projet implémente l'algorithme de Ford-Fulkerson pour le calcul du flot maximal dans un réseau de transport représenté par un graphe orienté. L'utilisateur peut téléverser un fichier contenant les données du graphe, spécifier un sommet source et un sommet puits, et obtenir le flot maximal entre ces deux sommets. Des visualisations sont également fournies pour illustrer les capacités initiales et résiduelles du graphe.

## Fonctionnalités

* **Lecture de fichier** : L'utilisateur peut téléverser un fichier contenant la définition des arêtes et des capacités du graphe.
* **Calcul du flot maximal** : Implémentation de l'algorithme Ford-Fulkerson, qui trouve le flot maximal entre une source et un puits.
* **Visualisation** :
  * Visualisation des capacités initiales du graphe.
  * Visualisation des capacités résiduelles après calcul du flot maximal.

## Structure du Code
### 1. Classe Graphe

La classe `Graphe` contient les méthodes principales pour gérer le graphe et calculer le flot maximal.
### Méthodes principales

* `ajouter_arete(u, v, capacite)` : Ajoute une arête entre deux sommets avec une capacité spécifique. Gère également l’ajout conditionnel d’une arête inverse avec une capacité de 0.
* `bfs(source, puits, parent)` : Utilise une recherche en largeur pour trouver un chemin augmentant entre la source et le puits, si un tel chemin existe.
* `ford_fulkerson(source, puits)` : Calcule le flot maximal entre la source et le puits en utilisant l'algorithme de Ford-Fulkerson.
* `visualiser_graphe()` : Affiche le graphe avec les capacités initiales.
* `visualiser_capacites_residuelles()` : Affiche les capacités résiduelles du graphe après calcul du flot maximal.

### 2. Fonction lire_graphe_fichier(fichier_televerse)
Cette fonction lit un fichier texte contenant les définitions des arêtes et leurs capacités et renvoie une liste d'arêtes et le nombre de sommets uniques dans le graphe.

### 3. Exemple de Fichier graphes.txt

Le fichier texte doit contenir une liste d’arêtes avec leurs capacités, chaque ligne respectant le format suivant :
```
S A 10
A B 5
B D 10
A D 7
```

Chaque ligne inclut :

* Source de l'arête (`S`).
* Destination de l'arête (`A`).
* Capacité de l'arête (`10`).

## 4. Visualisation des Graphes

* `visualiser_graphe() `: Affiche les capacités initiales des arêtes du graphe.
* `visualiser_capacites_residuelles() `: Affiche les capacités résiduelles après exécution de l'algorithme.

## Prérequis

* Python 3.x
* Bibliothèques networkx et matplotlib pour la visualisation. Installez-les via :

  `**pip install networkx matplotlib**`

## Utilisation

1. **Téléverser le fichier** : L’utilisateur est invité à téléverser un fichier texte contenant les arêtes et les capacités du graphe.
2. **Spécifier la source** et le puits : Une fois le fichier lu, l’utilisateur est invité à entrer les sommets source et puits.
3. **Exécution du code** : Le programme affiche le flot maximal calculé ainsi que les graphes avec les capacités initiales et résiduelles.

## Exemple d'Exécution

```
  # Téléversement du fichier dans Colab
  print("Veuillez téléverser votre fichier texte de graphe.")
  fichier_televerse = files.upload()
  
  # Lire le fichier, ajouter les arêtes et calculer le flot maximal
  aretes, nombre_sommets = lire_graphe_fichier(nom_fichier)
  g = Graphe(nombre_sommets)
  for u, v, capacite in aretes:
      g.ajouter_arete(u, v, capacite)
  
  g.visualiser_graphe()
  source = input("Entrez le sommet source : ")
  puits = input("Entrez le sommet puits : ")
  print(f"\nLe flot maximal possible est : {g.ford_fulkerson(source, puits)}\n")
  g.visualiser_capacites_residuelles()
```
## Sortie attendue

* Flot maximal calculé entre les sommets source et puits.
* Visualisation initiale des capacités du graphe.
* Visualisation des capacités résiduelles après calcul du flot maximal.

## Explication de l'Algorithme de Ford-Fulkerson

L’algorithme de Ford-Fulkerson cherche à maximiser le flot dans un réseau en trouvant des **chemins augmentants** entre une source et un puits :

  1. Utilise la recherche en largeur pour trouver des chemins où le flot peut être augmenté.
  2. Calcule la capacité minimale dans ce chemin.
  3. Réduit les capacités le long du chemin en fonction de ce flot, en ajoutant un flot inverse pour permettre des ajustements ultérieurs.
  4. Répète le processus jusqu’à ce qu’il n’existe plus de chemins augmentants possibles.

## Structure des Dossiers
```
  |-- README.md
  |-- main.py              # Script principal contenant le code du graphe et de Ford-Fulkerson
  |-- graphes.txt          # Fichier d'entrée avec les arêtes et capacités du graphe
```
  
