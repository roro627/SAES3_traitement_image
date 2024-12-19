from astroquery.mast import Observations
from astropy.coordinates import SkyCoord
import astropy.units as units
import os
import itertools

def get_observations(object_name, radius):
    """
    Recherche des observations pour un objet donné dans un rayon spécifié.
    """
    # Convertir le nom de l'objet en coordonnées
    coord = SkyCoord.from_name(object_name)
        
    observations = Observations.query_criteria(coordinates=coord, radius=radius * units.deg, dataproduct_type="image")
    
    # Filtrer pour ne garder que les fichiers FITS dans les observations et générer les observations
    for obs in observations:
        if ".fits" in obs['dataURL']:
            yield obs

def get_missions(observations):
    """
    Récupère les missions uniques à partir des observations.
    """
    unique_missions = set()
    for obs in observations:
        try :
            collection = obs['obs_collection']
            if collection not in unique_missions:
                unique_missions.add(collection)
                yield collection
        except TypeError:
            # éviter TypeError: unhashable type: 'MaskedConstant'
            pass

def filter_by_mission(observations, mission):
    """
    Filtre les observations en fonction de la mission sélectionnée.
    """
    for obs in observations:
        if obs['obs_collection'] == mission:
            yield obs

def get_programs(observations):
    """
    Récupère les programmes uniques à partir des observations filtrées.
    """
    unique_programs = set()
    for obs in observations:
        try:
            program = obs['proposal_id']
            if program not in unique_programs:
                unique_programs.add(program)
                yield program
        except TypeError:
            # éviter TypeError: unhashable type: 'MaskedConstant'
            pass

def filter_by_program(observations, program):
    """
    Filtre les observations en fonction du programme sélectionné.
    """
    for obs in observations:
        if obs['proposal_id'] == program:
            yield obs

def get_celestial_objects(observations):
    """
    Récupère les objets célestes uniques à partir des observations filtrées.
    """
    unique_celestial_objects = set()
    for obs in observations:
        try:
            celestial_object = obs['target_name']
            if celestial_object not in unique_celestial_objects:
                unique_celestial_objects.add(celestial_object)
                yield celestial_object
        except TypeError:
            # éviter TypeError: unhashable type: 'MaskedConstant'
            pass

def filter_by_celestial_object(observations, celestial_object):
    """
    Filtre les observations en fonction de l'objet céleste sélectionné.
    """
    for obs in observations:
        if obs['target_name'] == celestial_object:
            yield obs

def get_final_product(observations, ideal_Mo_size=50):
    """
    Sélectionne le produit final en fonction de la taille la plus proche de ideal_Mo_size.
    """
    observations_list = list(observations)
    if not observations_list:
        return None

    # Extraire les obsid des observations
    obs_ids = [obs['obsid'] for obs in observations_list]

    # Obtenir les produits associés aux obsid filtrés
    products = Observations.get_product_list(obs_ids)
    
    # Filtrer pour ne garder que les fichiers FITS
    products = [product for product in products if ".fits" in product['dataURI']]
    
    if not products:
        return None

    # Garder le fichier avec la taille la plus proche de 50Mo
    target_size = ideal_Mo_size * 1000000
    sizes = [product['size'] for product in products]
    
    def absolute_difference(x):
        return abs(x - target_size)
    
    closest_size = min(sizes, key=absolute_difference)
    
    # Appliquer le filtre de taille
    products_filtered_size = [product for product in products if product['size'] == closest_size]
    
    if not products_filtered_size:
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