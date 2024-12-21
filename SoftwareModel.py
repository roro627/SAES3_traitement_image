from astropy.io import fits
from skimage import exposure
from PIL import Image
import numpy as np
from datetime import datetime
import sys

# -----------------------------------------------------------------------------
# --- classe SoftwareModel
# -----------------------------------------------------------------------------

class SoftwareModel:

    # Constructeur
    def __init__(self) -> None:

        # Attributs
        self.ImagePath : list[str] = []
        self.ImageHead : list[fits.header.Header]  = []
        self.ImageFilter : dict = {}
        self.ImageBody : list[np.ndarray] = []
        self.ImageExport : np.ndarray = None

    def openImage(self) -> np.ndarray :
        datas = []
        for imagePath in self.ImagePath :
            hdul = fits.open(imagePath)

            dataHeader = hdul[0].header
            dataFilter = dataHeader['FILTER']
            data = hdul[0].data

            self.setImageHead(dataHeader)
            self.setImageFilter(dataFilter,data)
            self.setImageBody(data)

            data = fits.getdata(imagePath)

            # Éliminer les valeurs aberrantes
            data = np.clip(data, np.percentile(data, 1), np.percentile(data, 99))

            # Normaliser les données
            norm_data = 255 * (data - np.min(data)) / (np.max(data) - np.min(data))
            norm_data = np.clip(norm_data, 0, 255).astype(np.uint8)

            # Assurez-vous que les données sont contiguës
            norm_data = np.ascontiguousarray(norm_data)

            datas.append(norm_data)
        
        return datas
        

    def setImagePath(self,fpath) -> None :
        """
        Cette méthode permet de mettre à jour le chemin vers le fichier FITS.
        
        Paramètres :self (SoftwareModel) : L'instance de la classe.
                    fpath (str) : Le chemin vers le fichier FITS.
        Return :None
        """
        self.ImagePath = []
        for imagePath in fpath :
            self.ImagePath.append(imagePath)

    def setImageHead(self, imgHead) -> None :
        """
        Cette méthode permet de mettre à jour l'entête d'un fichier FITS.
        
        Paramètres :self (SoftwareModel) : L'instance de la classe.
                    imgHead (fits.header.Header) : Entête d'une image FITS.
        Return :None
        """
        self.ImageHead.append(imgHead)

    def setImageFilter(self, imgFilter, data) -> None :
        if not isinstance(data, np.ndarray):
            return
        data = np.nan_to_num(data)
        data = self.log_scale(data)
        data = self.normalize_data(data)
        data = exposure.equalize_hist(data)
        self.ImageFilter[imgFilter] = data

    def setImageBody(self, imgBody) -> None :
        """
        Cette méthode permet de mettre à jour la matrice d'un fichier FITS.
        
        Paramètres :self (SoftwareModel) : L'instance de la classe.
                    imgBody (np.ndarray) : Matrice d'un fichier FITS.
        Return :None
        """
        self.ImageBody.append(imgBody)

    def log_scale(self, data):
        return np.log10(data + 1)

    def normalize_data(self, data):
        return (data - np.min(data)) / (np.max(data) - np.min(data))
    
    def filteredImage(self, dict):
        # Couleur -> Filtre -> Matrice
        combined_image = np.stack([self.ImageFilter[dict["Red"]], self.ImageFilter[dict["Green"]], self.ImageFilter[dict["Blue"]]], axis=-1)
        self.ImageExport = combined_image
        return combined_image
    
        # combined_image = (combined_image * 255).astype(np.uint8)
        # image = Image.fromarray(combined_image)
        # image.save("output_image.png")
    
    def exportAsPNG(self):
        if self.ImageExport is None:
            return
        combined_image = (self.ImageExport * 255).astype(np.uint8)
        image = Image.fromarray(combined_image)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"/exports/image_{timestamp}.png"

        current_directory = sys.path[0]
        output_path = current_directory + output_filename
        print(output_path)
        image.save(output_path)