from astropy.io import fits
import numpy as np

# -----------------------------------------------------------------------------
# --- classe SoftwareModel
# -----------------------------------------------------------------------------

class SoftwareModel:

    # Constructeur
    def __init__(self) -> None:

        # Attributs
        self.ImagePath : (None|str) = None
        self.ImageHead = None
        self.ImageBody = None

    def openImage(self) -> np.ndarray :
        with fits.open(self.ImagePath) as hdul:
            data = hdul[0].data
            dataHeader = hdul[0].header

            self.setImageHead(dataHeader)

            # Normalisation
            data = np.nan_to_num(data)
            data = (data - data.min()) / (data.max() - data.min())

            return data

    def setImagePath(self,fpath) -> None :
        '''
        Cette méthode permet de mettre à jour le chemin vers le fichier .fit .
        
        Paramètres :self (SoftwareModel) : L'instance de la classe.
                    fpath (String) : Le chemin vers le fichier .fit .
        Return :None
        '''
        self.ImagePath = fpath

    def setImageHead(self, imgHead) -> None :
        '''
        Cette méthode permet de mettre à jour le chemin vers le fichier .fit .
        
        Paramètres :self (SoftwareModel) : L'instance de la classe.
                    fpath (String) : Le chemin vers le fichier .fit .
        Return :None
        '''
        self.ImageHead = imgHead

    def setImageBody(self, imgBody) -> None :
        '''
        Cette méthode permet de mettre à jour le chemin vers le fichier .fit .
        
        Paramètres :self (SoftwareModel) : L'instance de la classe.
                    fpath (String) : Le chemin vers le fichier .fit .
        Return :None
        '''
        self.ImageBody = imgBody
