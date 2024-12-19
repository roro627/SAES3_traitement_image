from astroquery.mast import Observations
from astropy.coordinates import SkyCoord
import astropy.units as units
import os

def get_observations(object_name, radius):
    """
    Recherche des observations pour un objet donné dans un rayon spécifié.
    """
    # Convertir le nom de l'objet en coordonnées
    coord = SkyCoord.from_name(object_name)
        
    observations = Observations.query_criteria(coordinates=coord, radius=radius * units.deg, dataproduct_type="image")
    
    # Filtrer pour ne garder que les fichiers FITS dans les observations
    observations = observations[[ ".fits" in url for url in observations['dataURL'] ]]
    
    if len(observations) == 0:
        return None

    return observations

def get_missions(observations):
    """
    Récupère les missions uniques à partir des observations.
    """
    unique_missions = []
    for collection in observations['obs_collection']:
        if collection not in unique_missions:
            unique_missions.append(collection)
    return unique_missions

def filter_by_mission(observations, mission):
    """
    Filtre les observations en fonction de la mission sélectionnée.
    """
    observations = observations[observations['obs_collection'] == mission]
    if len(observations) == 0:
        return None
    return observations

def get_programs(observations):
    """
    Récupère les programmes uniques à partir des observations filtrées.
    """
    unique_programs = []
    for program in observations['proposal_id']:
        if program not in unique_programs:
            unique_programs.append(program)
    return unique_programs

def filter_by_program(observations, program):
    """
    Filtre les observations en fonction du programme sélectionné.
    """
    observations = observations[observations['proposal_id'] == program]
    if len(observations) == 0:
        return None
    return observations

def get_celestial_objects(observations):
    """
    Récupère les objets célestes uniques à partir des observations filtrées.
    """
    unique_celestial_objects = []
    for celestial_object in observations['target_name']:
        if celestial_object not in unique_celestial_objects:
            unique_celestial_objects.append(celestial_object)
    return unique_celestial_objects

def filter_by_celestial_object(observations, celestial_object):
    """
    Filtre les observations en fonction de l'objet céleste sélectionné.
    """
    observations = observations[observations['target_name'] == celestial_object]
    if len(observations) == 0:
        return None
    return observations

def get_final_product(observations, ideal_Mo_size=50):
    """
    Sélectionne le produit final en fonction de la taille la plus proche de ideal_Mo_size.
    """
    if len(observations) == 0:
        return None
    
    # Obtenir les produits associés aux observations filtrées
    products = Observations.get_product_list(observations)
    
    # Filtrer pour ne garder que les fichiers FITS
    products = products[[ ".fits" in url for url in products['dataURI'] ]]
    
    # Garder le fichier avec la taille la plus proche de 50Mo
    target_size = ideal_Mo_size * 1000000
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

def download_observations(filtered_product, output_folder):
    """
    Télécharge le fichier FITS filtré.

    Paramètres :
    - filtered_product : Le produit FITS filtré.
    - output_folder (str) : Le dossier où sauvegarder le fichier.

    Retourne :
    - Le manifeste du produit téléchargé.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Télécharger le fichier FITS filtré dans le dossier de sortie
    manifest = Observations.download_products(
        filtered_product,
        download_dir=output_folder,
        flat=True,
        verbose=False
    )

    return manifest
