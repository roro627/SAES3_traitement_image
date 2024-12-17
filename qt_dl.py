import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import QSize
from astroquery.mast import Observations
from astroquery.mast import Mast
from astropy.coordinates import SkyCoord
import astropy.units as units
import os

def rechercher_observations(objet, rayon):
    """
    Recherche les observations disponibles dans le MAST pour un objet donné,
    filtre les produits pour ne garder que les fichiers FITS,
    et retourne les produits filtrés.

    Paramètres :
    - objet (str) : Le nom de l'objet (par exemple 'M31').
    - rayon (float) : Rayon de recherche autour de l'objet en degrés.
    - mission (str) : Filtrer par mission (par exemple, 'HST').
    - obs_type (str) : Filtrer par type d'observation (par exemple, 'image', 'spectrum').
    - program (str) : Filtrer par programme d'observation.
    - celestial_object (str) : Filtrer par objet céleste.

    Retourne :
    - Une table des produits filtrés (Astropy Table).
    """
    # Convertir le nom de l'objet en coordonnées
    coord = SkyCoord.from_name(objet)
    print(f"Coordonnées de {objet} : {coord}")

    # Rechercher des observations dans le rayon donné
    observations = Observations.query_region(coord, radius=rayon * units.deg)
    print(f"Nombre d'observations trouvées : {len(observations)}")

    if len(observations) == 0:
        print("Aucune observation trouvée.")
        yield None

    # renvoyer toutes les missions trouvées (1 seule fois par mission)
    unique_collections = []
    for collection in observations['obs_collection']:
        if collection not in unique_collections:
            unique_collections.append(collection)
    mission = yield unique_collections

    # Appliquer les filtres supplémentaires sur les observations
    print(f"Applique le filtre de mission : {mission}")
    observations = observations[observations['obs_collection'] == mission]
    if len(observations) == 0:
        print("Aucune observation correspondante aux filtres spécifiés.")
        yield None
    
    # renvoyer toutes les types d'observations trouvées (1 seule fois par type)
    unique_types = []
    for obs_type in observations['dataproduct_type']:
        if obs_type not in unique_types:
            unique_types.append(obs_type)
    obs_type = yield unique_types
    
    if obs_type:
        print(f"Applique le filtre de type d'observation : {obs_type}")
        observations = observations[observations['dataproduct_type'] == obs_type]
    if len(observations) == 0:
        print("Aucune observation correspondante aux filtres spécifiés.")
        yield None
        
    # renvoyer tous les programmes trouvés (1 seule fois par programme)
    unique_programs = []
    for program in observations['proposal_id']:
        if program not in unique_programs:
            unique_programs.append(program)
    program = yield unique_programs
    
    if program:
        print(f"Applique le filtre de programme d'observation : {program}")
        observations = observations[observations['proposal_id'] == program]
    
    if len(observations) == 0:
        print("Aucune observation correspondante aux filtres spécifiés.")
        yield None
        
    # renvoyer tous les objets célestes trouvés (1 seule fois par objet)
    unique_celestial_objects = []
    for celestial_object in observations['target_name']:
        if celestial_object not in unique_celestial_objects:
            unique_celestial_objects.append(celestial_object)
    celestial_object = yield unique_celestial_objects
        
    if celestial_object:
        print(f"Applique le filtre d'objet céleste : {celestial_object}")
        observations = observations[observations['target_name'] == celestial_object]

    

    # Filtrer pour ne garder que les fichiers FITS
    observations = observations[[ ".fits" in url for url in observations['dataURL'] ]]

    print(f"Nombre d'observations après filtrage : {len(observations)}")

    if len(observations) == 0:
        print("Aucune observation correspondante aux filtres spécifiés.")
        return None
    
    # Obtenir les produits associés aux observations filtrées
    products = Observations.get_product_list(observations)
    print(f"Nombre total de produits associés : {len(products)}")
    
    # Filtrer pour ne garder que les fichiers FITS
    products = products[[ ".fits" in url for url in products['dataURI'] ]]
    print(f"Nombre de produits FITS : {len(products)}")
    

    # Garder le fichier avec la taille la plus proche de 50Mo
    target_size = 50000000
    sizes = [product['size'] for product in products]
    
    def absolute_difference(x):
        return abs(x - target_size)
    
    closest_size = min(sizes, key=absolute_difference)
    print(f"Taille la plus proche de 50Mo : {closest_size}")
    
    # Appliquer le filtre de taille manuellement
    products_filtered_size = products[
        (products['size'] == closest_size)
    ]

    if len(products_filtered_size) == 0:
        print("Aucun fichier FITS trouvé après filtrage.")
        return None

    # renvoyé que le dernier produit
    return products_filtered_size[-1]


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Downloader App")
        self.setGeometry(100, 100, 800, 600)


if __name__ == "__main__":
    # ne pas oublier de gérer les none
    res_filters = rechercher_observations("M31", 0.1)
    print(next(res_filters))
    print(res_filters.send("HST"))
    
    # app = QApplication(sys.argv)
    # window = MainWindow()
    # window.show()
    # sys.exit(app.exec())