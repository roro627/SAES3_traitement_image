# Logiciel de traitement d'images astronomiques

## Auteurs

- Romain LAMBERT
- Alexis COCQUEREL

## Description

Ce projet est un logiciel de traitement d'images astronomiques développé en Python. Il permet de télécharger, afficher et traiter des images astronomiques au format FITS en utilisant des bibliothèques tels que Astropy, PyQt6 et Astroquery.

## Fonctionnalités

- Téléchargement d'images astronomiques avec astroquery.
- Interface graphique utilisateur développée avec le module PyQt6.
- Affichage et manipulation d'images FITS.
- Visualisation des métadonnées des fichiers FITS.
- Architecture Modèle-Vue-Contrôleur (MVC) pour une meilleure organisation du code.

## Installation

Assurez-vous d'avoir Python 3 installé sur votre machine. Installez les dépendances nécessaires avec :

```bash
pip install PyQt6, astropy, astroquery, scikit-image, pillow
```

## Utilisation

Pour lancer l'application :

```bash
python SoftwareController.py
```

Pour obtenir une image en couleur à partir d'images en niveaux de gris, il faut :
- Importer un dossier contenant des images FITS à l'aide du menu 'Ouvrir un dossier'.
- Associer les filtres au code RVB dans le menu 'Conversion polychromatique (RVB)'.
- Exporter l'image en couleur avec le menu 'Exporter', l'image se situe alors dans le dossier 'exports'.

## Remarques

- Le projet a été testé sur Windows et MacOs
- Le projet nécéssite une connexion internet pour le téléchargement des images.