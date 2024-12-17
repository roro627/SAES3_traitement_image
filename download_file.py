from astroquery.mast import Observations
from astroquery.mast import Mast
from astropy.coordinates import SkyCoord
import astropy.units as units
import os

def rechercher_observations(objet, rayon, mission=None, obs_type=None, program=None, celestial_object=None):
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
        return None

    # Appliquer les filtres supplémentaires sur les observations
    if mission:
        print(f"Applique le filtre de mission : {mission}")
        observations = observations[observations['obs_collection'] == mission]
    if obs_type:
        print(f"Applique le filtre de type d'observation : {obs_type}")
        observations = observations[observations['dataproduct_type'] == obs_type]
    if program:
        print(f"Applique le filtre de programme d'observation : {program}")
        observations = observations[observations['proposal_id'] == program]
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
    

def telecharger_observations(filtered_products, dossier_sortie):
    """
    Télécharge les fichiers FITS filtrés.

    Paramètres :
    - filtered_products : La table des produits FITS filtrés.
    - dossier_sortie (str) : Le dossier où sauvegarder les fichiers.
    """
    if not os.path.exists(dossier_sortie):
        os.makedirs(dossier_sortie)
        print(f"Dossier de sortie créé : {dossier_sortie}")
    else:
        print(f"Dossier de sortie existant : {dossier_sortie}")

    # Télécharger les fichiers FITS filtrés
    manifest = Observations.download_products(
        filtered_products,
        download_dir=dossier_sortie,
        mrp_only=False
    )
    print("Téléchargement terminé.")

    return manifest

def main():
    # Paramètres d'entrée
    objet = 'M31'
    rayon = 0.1
    dossier_sortie = 'test'
    mission = 'HST'
    obs_type = 'image'
    program = '10006'
    celestial_object = 'M31-BH3'

    # Rechercher les produits FITS filtrés
    filtered_products = rechercher_observations(objet, rayon, mission, obs_type, program, celestial_object)

    if filtered_products is None:
        print("Aucun produit à télécharger. Fin du programme.")
        return

    # Télécharger les produits FITS filtrés
    telecharger_observations(filtered_products, dossier_sortie)

if __name__ == "__main__":
    main()
