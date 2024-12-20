from astroquery.mast import Observations
from astropy.coordinates import SkyCoord
import astropy.units as units
import os

def filter_by_filter(observations, filter_value):
    """
    Filtre les observations en fonction du filtre sélectionné.
    """
    for obs in observations:
        if obs['filters'] == filter_value:
            yield obs


def filter_by_program(observations, program):
    """
    Filtre les observations en fonction du programme sélectionné.
    """
    for obs in observations:
        if obs['proposal_id'] == program:
            yield obs


def filter_by_celestial_object(observations, celestial_object):
    """
    Filtre les observations en fonction de l'objet céleste sélectionné.
    """
    for obs in observations:
        if obs['target_name'] == celestial_object:
            yield obs

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

def get_celestial_objects(observations):
    """
    Récupère les objets célestes uniques à partir des observations filtrées.
    """
    unique_celestial_objects = []
    seen = set() # pour éviter les doublons et optimiser les performances
    for obs in observations:
        try:
            celestial_object = str(obs['target_name'])
            if celestial_object not in seen:
                unique_celestial_objects.append(celestial_object)
                seen.add(celestial_object)
        except TypeError:
            # éviter TypeError: unhashable type: 'MaskedConstant'
            pass
        
    # Vérifie si la liste unique_celestial_objects n'est pas vide
    return unique_celestial_objects if unique_celestial_objects else None

def get_filters(observations):
    """
    Récupère les filtres uniques à partir des observations.
    """
    unique_filters = []
    for obs in observations:
        try:
            filter_value = str(obs['filters'])
            if filter_value not in unique_filters and filter_value != '--':
                unique_filters.append(filter_value)
                
        except TypeError:
            # éviter TypeError: unhashable type: 'MaskedConstant'
            pass
        
    # Vérifie si la liste unique_filters n'est pas vide
    return unique_filters if unique_filters else None

def get_programs(observations):
    """
    Récupère les programmes uniques à partir des observations filtrées.
    """
    unique_programs = []
    for obs in observations:
        try:
            program = str(obs['proposal_id'])
            if program not in unique_programs:
                unique_programs.append(program)
        except TypeError:
            # éviter TypeError: unhashable type: 'MaskedConstant'
            pass
        
    # Vérifie si la liste unique_programs n'est pas vide
    return unique_programs if unique_programs else None

def get_final_product(observations, ideal_Mo_size=50):
    """
    Sélectionne le produit final en fonction de la taille la plus proche de ideal_Mo_size.
    """
    
    # Extraire les obsid des observations
    obs_ids = [obs['obsid'] for obs in observations]

    # Obtenir les produits associés aux obsid filtrés
    products = Observations.get_product_list(obs_ids)
    
    # Filtrer pour ne garder que les fichiers FITS
    products = [product for product in products if ".fits" in product['dataURI']]
    
    if not products:
        return None

    # Garder le fichier avec la taille la plus proche de ideal_Mo_size Mo
    target_size = ideal_Mo_size * 1000000  
    sizes = [product['size'] for product in products]
    
    def absolute_difference(x):
        return abs(x - target_size)
    
    sorted_size = sorted(sizes, key=absolute_difference)
        
    # Initialisé au 2/3 de la taille idéale pour éviter de choisir un fichier trop petit
    closest_size = target_size * 2 / 3
    
    # trouver la taille la plus proche avec comme minimum closest_size
    for size in sorted_size:
        if size >= closest_size:
            closest_size = size
            break    
    
    
    # Appliquer le filtre de taille
    products_filtered_size = [product for product in products if product['size'] == closest_size]
    
    if not products_filtered_size:
        return None
    
    # Retourner un seul produit
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
        flat=True
    )
    return manifest