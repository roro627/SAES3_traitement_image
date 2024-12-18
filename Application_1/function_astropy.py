from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
from skimage import io, img_as_float, img_as_ubyte, exposure
import os,sys

def apply_color_filter(image, r_scale=30, g_scale=30, b_scale=30):
    red = image * r_scale
    green = image * g_scale
    blue = image * b_scale

    rgb_image = np.stack([red, green, blue], axis=-1)
    
    rgb_image = np.clip(rgb_image, 0, 1)

    return rgb_image


def test():
    current_directory = sys.path[0]
    parent_directory = os.path.dirname(current_directory)
    # Chargement de l'image FITS
    with fits.open(parent_directory + '\\downloads\\j8vp03olq_raw.fits') as hdul:
        header = hdul[0].header
        image_data = hdul[0].data

        # Normalisation des données de l'image

        # Affichage de l'image en niveaux de gris
        plt.figure(figsize=(10, 5))
        plt.subplot(1, 2, 1)
        plt.imshow(image_data, cmap='gray', vmin=0, vmax=1)
        plt.colorbar()
        plt.title('Image en Niveaux de Gris (Normalisée)')


def main():
    # Charger les trois fichiers FITS
    hdul_halpha = fits.open('./downloads/j8vp03olq_raw.fits.fits')
    hdul_oiii = fits.open('Tarantula/Tarantula_Nebula-oiii.fit')
    hdul_sii = fits.open('Tarantula/Tarantula_Nebula-sii.fit')
    # Extraire les données d'image
    data_halpha = hdul_halpha[0].data
    data_oiii = hdul_oiii[0].data
    data_sii = hdul_sii[0].data

    # Vérifier les plages de données
    print("H-alpha min:", np.min(data_halpha), "max:", np.max(data_halpha))
    print("OIII min:", np.min(data_oiii), "max:", np.max(data_oiii))
    print("SII min:", np.min(data_sii), "max:", np.max(data_sii))

    # Fonction pour appliquer une échelle logarithmique
    def log_scale(data):
        return np.log10(data + 1)  # log10 +1 pour éviter log(0)

    # Appliquer la mise à l'échelle logarithmique à chaque canal
    data_halpha_log = log_scale(data_halpha)
    data_oiii_log = log_scale(data_oiii)
    data_sii_log = log_scale(data_sii)

    # Normalisation entre 0 et 1
    def normalize_data(data):
        return (data - np.min(data)) / (np.max(data) - np.min(data))

    data_halpha_log = normalize_data(data_halpha_log)
    data_oiii_log = normalize_data(data_oiii_log)
    data_sii_log = normalize_data(data_sii_log)


    # Appliquer l'égalisation d'histogramme sur chaque canal
    data_halpha_eq = exposure.equalize_hist(data_halpha_log)
    data_oiii_eq = exposure.equalize_hist(data_oiii_log)
    data_sii_eq = exposure.equalize_hist(data_sii_log)

    # Créer une image combinée en RGB (H-alpha = rouge, OIII = vert, SII = bleu)
    combined_image = np.stack([data_halpha_eq, data_halpha_eq, data_halpha_eq], axis=-1)

    # Afficher l'image combinée
    plt.imshow(combined_image)
    plt.axis('off')  # Masquer les axes
    plt.show()


if __name__ == "__main__":
    test()







    