import os
from astropy.io import fits

# Répertoire contenant les fichiers FITS
directory = './downloads'

# Itérer sur tous les fichiers dans le répertoire
for filename in os.listdir(directory):
    if filename.endswith('.fits'):
        filepath = os.path.join(directory, filename)
        with fits.open(filepath) as hdul:
            # Afficher le nom des filtres
            for hdu in hdul:
                if 'FILTER' in hdu.header:
                    print(f"Fichier: {filename}, Filtre: {hdu.header['FILTER']}")