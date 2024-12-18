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
        self.ImageHead : (None|fits.header.Header)  = None
        self.ImageBody : (None|np.ndarray) = None

    def openImage(self) -> np.ndarray :
        with fits.open(self.ImagePath) as hdul:
            dataHeader = hdul[0].header
            data = hdul[0].data

            self.setImageHead(dataHeader)
            self.setImageBody(data)

            # Normalisation
            print(data)
            data = np.nan_to_num(data)
            print(data)
            data = (data - data.min()) / (data.max() - data.min())
            print(data)


            return data

    def setImagePath(self,fpath) -> None :
        '''
        Cette méthode permet de mettre à jour le chemin vers le fichier FITS.
        
        Paramètres :self (SoftwareModel) : L'instance de la classe.
                    fpath (str) : Le chemin vers le fichier FITS.
        Return :None
        '''
        self.ImagePath = fpath

    def setImageHead(self, imgHead) -> None :
        '''
        Cette méthode permet de mettre à jour l'entête d'un fichier FITS.
        
        Paramètres :self (SoftwareModel) : L'instance de la classe.
                    imgHead (fits.header.Header) : Entête d'une image FITS.
        Return :None
        '''
        self.ImageHead = imgHead

    def setImageBody(self, imgBody) -> None :
        '''
        Cette méthode permet de mettre à jour la matrice d'un fichier FITS.
        
        Paramètres :self (SoftwareModel) : L'instance de la classe.
                    imgBody (np.ndarray) : Matrice d'un fichier FITS.
        Return :None
        '''
        self.ImageBody = imgBody
