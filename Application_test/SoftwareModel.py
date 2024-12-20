from astropy.io import fits
import numpy as np

# -----------------------------------------------------------------------------
# --- classe SoftwareModel
# -----------------------------------------------------------------------------

class SoftwareModel:

    # Constructeur
    def __init__(self) -> None:

        # Attributs
        self.ImagePath : list[str] = []
        self.ImageHead : list[fits.header.Header]  = []
        self.ImageFilter : list[dict] = []
        self.ImageBody : list[np.ndarray] = []

    def openImage(self) -> np.ndarray :
        datas = []
        for imagePath in self.ImagePath :
            hdul = fits.open(imagePath)

            dataHeader = hdul[0].header
            dataFilter = dataHeader['FILTER']
            data = hdul[0].data

            self.setImageHead(dataHeader)
            self.setImageFilter(dataFilter)
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

    def setImageFilter(self, imgFilter) -> None :
        self.ImageFilter.append(imgFilter)

    def setImageBody(self, imgBody) -> None :
        """
        Cette méthode permet de mettre à jour la matrice d'un fichier FITS.
        
        Paramètres :self (SoftwareModel) : L'instance de la classe.
                    imgBody (np.ndarray) : Matrice d'un fichier FITS.
        Return :None
        """
        self.ImageBody.append(imgBody)
