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
        for imagePath in self.ImagePath :
            with fits.open(imagePath) as hdul:
                dataHeader = hdul[0].header
                dataFilter = dataHeader['FILTER']
                data = hdul[0].data

                self.setImageHead(dataHeader)
                self.setImageFilter(dataFilter)
                self.setImageBody(data)

                # Normalisation
                data = np.nan_to_num(data)
                data = (data - data.min()) / (data.max() - data.min())
        
        return data

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
