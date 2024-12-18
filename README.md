# Logiciel de traitement d'images astronomiques

## Auteurs

- Romain LAMBERT
- Alexis COCQUEREL

## Description

Ce projet est un logiciel de traitement d'images astronomiques développé en Python. Il permet de télécharger, afficher et traiter des images astronomiques au format FITS en utilisant des bibliothèques tels que Astropy, PyQt6 et Astroquery.

## Fonctionnalités

- Téléchargement d'images astronomiques avec le module astroquery.
- Interface graphique utilisateur développée avec le module PyQt6.
- Affichage et manipulation d'images FITS.
- Application de filtres de couleur aux images.
- Visualisation des métadonnées des fichiers FITS.
- Architecture Modèle-Vue-Contrôleur (MVC) pour une meilleure organisation du code.

## Installation

Assurez-vous d'avoir Python 3 installé sur votre machine. Installez les dépendances nécessaires avec :

```bash
pip install PyQt6, astropy, astroquery, scikit-image
```

## Utilisation

Pour lancer l'application principale :

```bash
python Application_1/SoftwareController.py
```

Pour ouvrir l'interface de téléchargement (prochainement intégrer à l'application principale) :

```bash
python qt_dl.py
```

## Remarques

- Le projet a été testé uniquement sur Windows. 
- Le projet nécéssite une connexion internet pour le téléchargement des images.