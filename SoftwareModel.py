from astropy.io import fits
from skimage import exposure
from PIL import Image
import numpy as np
from datetime import datetime
import sys

# -----------------------------------------------------------------------------
# --- classe SoftwareModel
# --- Fait par : COCQUEREL Alexis et LAMBERT Romain
# -----------------------------------------------------------------------------

class SoftwareModel:

    # Constructeur
    def __init__(self) -> None:

        # Attributs
        self.ImagePath : list[str] = []
        self.ImageHead : list[fits.header.Header]  = []
        self.ImageFilter : dict[str, np.ndarray] = {}
        self.ImageBody : list[np.ndarray] = []
        self.ImageExport : np.ndarray = None

    def openImage(self) -> list[np.ndarray] :
        """
        Cette méthode permet d'ouvrir l'ensemble des images FITS importées sous la forme d'une matrice.
        Paramètres :self (SoftwareModel) : L'instance de la classe.
        Return : list[np.ndarray] : Liste qui contient toutes les matrices des images FITS.
        """
        datas = []
        for imagePath in self.ImagePath :
            hdul = fits.open(imagePath)

            dataHeader = hdul[0].header
            dataFilter = dataHeader['FILTER']
            data = hdul[0].data

            self.setImageHead(dataHeader)
            prepareData = self.prepareImage(data)
            self.setImageFilter(dataFilter,prepareData)
            self.setImageBody(data)

            # Éliminer les valeurs aberrantes
            data = np.clip(data, np.percentile(data, 1), np.percentile(data, 99))

            # Normaliser les données
            norm_data = 255 * (data - np.min(data)) / (np.max(data) - np.min(data))
            norm_data = np.clip(norm_data, 0, 255).astype(np.uint8)

            # S'assurer que les données sont contiguës
            norm_data = np.ascontiguousarray(norm_data)

            datas.append(norm_data)
        
        return datas
        
    def setImagePath(self,fpath : list[str]) -> None :
        """
        Cette méthode permet de mettre à jour les chemins des fichier FITS dans l'attribut ImagePath.
        Paramètres :self (SoftwareModel) : L'instance de la classe.
                    fpath (list[str]) : Le chemin vers le fichier FITS.
        Return : None
        """
        self.ImagePath = [] # On nettoie les données
        for imagePath in fpath : self.ImagePath.append(imagePath)

    def setImageHead(self, imgHead : fits.header.Header) -> None :
        """
        Cette méthode permet de mettre à jour les entêtes des fichiers FITS dans l'attribut ImageHead.
        Paramètres :self (SoftwareModel) : L'instance de la classe.
                    imgHead (fits.header.Header) : Entête d'une image FITS.
        Return : None
        """
        self.ImageHead.append(imgHead)

    def setImageFilter(self, imgFilter : str, prepareData : np.ndarray) -> None :
        """
        Cette méthode permet de mettre à jour les filtres des fichiers FITS dans l'attribut ImageFilter.
        Chaque nom de filtre est associé à une matrice. Cette matrice est utilisée lors de la superposition de plusieurs filtres.
        Paramètres :self (SoftwareModel) : L'instance de la classe.
                    imgHead (fits.header.Header) : Entête d'une image FITS.
        Return : None
        """
        self.ImageFilter[imgFilter] = prepareData

    def setImageBody(self, imgBody : np.ndarray) -> None :
        """
        Cette méthode permet de mettre à jour les matrices des fichier FITS dans l'attribut ImageBody.
        Paramètres :self (SoftwareModel) : L'instance de la classe.
                    imgBody (np.ndarray) : Matrice d'un fichier FITS.
        Return :None
        """
        self.ImageBody.append(imgBody)

    def log_scale(self, data : np.ndarray) -> np.ndarray:
        """
        Cette méthode permet de faire une transformation logarithmique des données.
        Paramètres :self (SoftwareModel) : L'instance de la classe.
                    data (np.ndarray) : Matrice d'un fichier FITS.
        Return : np.ndarray : Matrice des données transformées.
        """
        return np.log10(data + 1)

    def normalize_data(self, data : np.ndarray) -> np.ndarray:
        """
        Cette méthode permet de normaliser les données.
        Paramètres :self (SoftwareModel) : L'instance de la classe.
                    data (np.ndarray) : Matrice d'un fichier FITS.
        Return : np.ndarray : Matrice des données normalisées.
        """
        return (data - np.min(data)) / (np.max(data) - np.min(data))
    
    def prepareImage(self, data: np.ndarray) -> np.ndarray:
        """
        Cette méthode permet de préparer une image pour la superposition de plusieurs filtres.
        Paramètres :self (SoftwareModel) : L'instance de la classe.
                    data (np.ndarray) : Matrice d'un fichier FITS.
        Return : np.ndarray : Matrice des données préparées.
        """
        if not isinstance(data, np.ndarray): return # Si data n'est pas une matrice
        data = np.nan_to_num(data)
        data = self.log_scale(data)
        data = self.normalize_data(data)
        data = exposure.equalize_hist(data) # Égalisation de l'histogramme
        return data
    
    def filteredImage(self, dict : dict) -> np.ndarray:
        """
        Cette méthode permet de superposer plusieurs filtres sur une image.
        Le dictionnaire contient les filtres choisis pour chaque couleur. A l'aide de ces filtypes, on peut récupérer les matrices dans le dictionnaire ImageFilter.
        Paramètres :self (SoftwareModel) : L'instance de la classe.
                    dict (dict) : Dictionnaire qui contient les filtres choisis.
        Return : np.ndarray : Matrice de l'image superposée.
        """
        # Couleur -> Filtre -> Matrice
        combined_image = np.stack([self.ImageFilter[dict["Red"]], self.ImageFilter[dict["Green"]], self.ImageFilter[dict["Blue"]]], axis=-1)
        self.ImageExport = combined_image
        return combined_image
    
    def exportAsPNG(self):
        """
        Cette méthode permet d'exporter une image superposée en format PNG.
        Paramètres :self (SoftwareModel) : L'instance de la classe.
        Return : None
        """
        if self.ImageExport is None : return # Si aucune image n'est présente dans ImageExport
        combined_image = (self.ImageExport * 255).astype(np.uint8)
        image = Image.fromarray(combined_image)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S") # Générer un timestamp pour avoir un nom de fichier unique
        output_filename = f"/exports/image_{timestamp}.png" 

        current_directory = sys.path[0]
        output_path = current_directory + output_filename
        image.save(output_path)