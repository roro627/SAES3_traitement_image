from astroquery.mast import Observations
from astropy.coordinates import SkyCoord
import astropy.units as units
import os

def obtenir_observations(objet, rayon):
    """
    Recherche des observations pour un objet donné dans un rayon spécifié.
    """
    # Convertir le nom de l'objet en coordonnées
    coord = SkyCoord.from_name(objet)
    
    # Rechercher des observations dans le rayon donné
    observations = Observations.query_region(coord, radius=rayon * units.deg)
    
    # Filtrer les observations pour ne garder que les images
    observations = observations[observations['dataproduct_type'] == "image"]
    
    if len(observations) == 0:
        return None

    return observations

def obtenir_missions(observations):
    """
    Récupère les missions uniques à partir des observations.
    """
    unique_missions = []
    for collection in observations['obs_collection']:
        if collection not in unique_missions:
            unique_missions.append(collection)
    return unique_missions

def filtrer_par_mission(observations, mission):
    """
    Filtre les observations en fonction de la mission sélectionnée.
    """
    observations = observations[observations['obs_collection'] == mission]
    if len(observations) == 0:
        return None
    return observations

def obtenir_programmes(observations):
    """
    Récupère les programmes uniques à partir des observations filtrées.
    """
    unique_programs = []
    for program in observations['proposal_id']:
        if program not in unique_programs:
            unique_programs.append(program)
    return unique_programs

def filtrer_par_programme(observations, programme):
    """
    Filtre les observations en fonction du programme sélectionné.
    """
    observations = observations[observations['proposal_id'] == programme]
    if len(observations) == 0:
        return None
    return observations

def obtenir_objets_celestes(observations):
    """
    Récupère les objets célestes uniques à partir des observations filtrées.
    """
    unique_celestial_objects = []
    for celestial_object in observations['target_name']:
        if celestial_object not in unique_celestial_objects:
            unique_celestial_objects.append(celestial_object)
    return unique_celestial_objects

def filtrer_par_objet_celeste(observations, objet_celeste):
    """
    Filtre les observations en fonction de l'objet céleste sélectionné.
    """
    observations = observations[observations['target_name'] == objet_celeste]
    if len(observations) == 0:
        return None
    return observations

def obtenir_produit_final(observations):
    """
    Sélectionne le produit final en fonction de la taille la plus proche de 50 Mo.
    """
    # Filtrer pour ne garder que les fichiers FITS
    observations = observations[[ ".fits" in url for url in observations['dataURL'] ]]
    
    if len(observations) == 0:
        return None
    
    # Obtenir les produits associés aux observations filtrées
    products = Observations.get_product_list(observations)
    
    # Filtrer pour ne garder que les fichiers FITS
    products = products[[ ".fits" in url for url in products['dataURI'] ]]
    
    # Garder le fichier avec la taille la plus proche de 50Mo
    target_size = 50000000
    sizes = [product['size'] for product in products]
    
    def absolute_difference(x):
        return abs(x - target_size)
    
    closest_size = min(sizes, key=absolute_difference)
    
    # Appliquer le filtre de taille
    products_filtered_size = products[
        (products['size'] == closest_size)
    ]
    
    if len(products_filtered_size) == 0:
        return None
    
    # Retourner le dernier produit
    return products_filtered_size[-1]

def telecharger_observations(filtered_product, dossier_sortie):
    """
    Télécharge le fichier FITS filtré.

    Paramètres :
    - filtered_product : Le produit FITS filtré.
    - dossier_sortie (str) : Le dossier où sauvegarder le fichier.

    Retourne :
    - Le chemin local du fichier téléchargé.
    """
    if not os.path.exists(dossier_sortie):
        os.makedirs(dossier_sortie)

    # Télécharger le fichier FITS filtré dans le dossier de sortie
    manifest = Observations.download_products(
        filtered_product,
        download_dir=dossier_sortie,
        flat=True,
        verbose=False
    )

    return manifest['Local Path']

if __name__ == "__main__":
    # Exemple d'utilisation
    objet = "M31"
    rayon = 0.1

    observations = obtenir_observations(objet, rayon)
    if observations is None:
        exit()

    missions = obtenir_missions(observations)
    print("Missions disponibles :", missions)
    mission_selected = "HST"
    observations = filtrer_par_mission(observations, mission_selected)
    if observations is None:
        exit()

    programmes = obtenir_programmes(observations)
    print("Programmes disponibles :", programmes)
    programme_selected = "10006"
    observations = filtrer_par_programme(observations, programme_selected)
    if observations is None:
        exit()

    objets_celestes = obtenir_objets_celestes(observations)
    print("Objets célestes disponibles :", objets_celestes)
    objet_celeste_selected = "M31-BH3"
    observations = filtrer_par_objet_celeste(observations, objet_celeste_selected)
    if observations is None:
        exit()

    produit_final = obtenir_produit_final(observations)
    print("Produit final :", produit_final)

    print("Fin du programme.")