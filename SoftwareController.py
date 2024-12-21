from SoftwareView import SoftwareView
from SoftwareModel import SoftwareModel

from PyQt6.QtWidgets import *
from PyQt6.QtWidgets import QApplication
import sys

# -----------------------------------------------------------------------------
# --- classe SoftwareController
# --- Fait par : COCQUEREL Alexis et LAMBERT Romain
# -----------------------------------------------------------------------------

class SoftwareController():
    def __init__(self):
        
        # Initialisation de la vue et du modèle
        self.view = SoftwareView()
        self.model = SoftwareModel()

        # Connecter les signaux de la vue aux slots du contrôleur

        # -------------- Signaux de View -------------- #
        self.view.fileButtonClicked.connect(self.openFile)
        self.view.folderButtonClicked.connect(self.openFolder)
        self.view.exportButtonClicked.connect(self.saveImage)

        # -------------- Signaux de View.filter -------------- #
        self.view.filter.applyButtonClicked.connect(self.createFilteredImage)

    # --- Méthodes pour View --- #

    def openFile(self, fpath):
        """
        Cette méthode est utilisée lors de l'ouverture d'une image FITS.
        Quand un fichier FITS est ouvert celui-ci est affiché ainsi que l'ensemble de ses informations situées dans l'entête.
        Paramètres : self (SoftwareController) : L'instance de la classe.
                    fpath (str) : Chemin vers l'image FITS.
        Return : None
        """
        # Réinitialisation des attributs de l'instance de SoftwareModel
        self.model.ImageHead = []
        self.model.ImageFilter = {}
        self.model.ImageBody = []
        self.view.tabWidget.clear()
        self.view.filter.clearFilter()

        self.model.setImagePath(fpath)
        datas = self.model.openImage()
        self.view.image.addInfoToTabWidget(datas, self.model.ImageHead, self.view.tabWidget)

    def openFolder(self, fpath):
        """
        Cette méthode est utilisée lors de l'ouverture d'un repertoire contenant des images FITS.
        Quand un fichier FITS est ouvert celui-ci est affiché ainsi que l'ensemble de ses informations situées dans l'entête.
        Paramètres : self (SoftwareController) : L'instance de la classe.
                    fpath (str) : Chemin vers l'image FITS.
        Return : None
        """
        self.openFile(fpath)
        self.view.filter.updateFilter(self.model.ImageFilter) # La mise à jour des filtres ne se fait que si plusieurs images sont ouvertes.

    def saveImage(self):
        """
        Cette méthode permet de sauvegarder l'image filtrée.
        Paramètres : self (SoftwareController) : L'instance de la classe.
        Return : None
        """
        self.model.exportAsPNG()

    # --- Méthodes pour View.filter --- #

    def createFilteredImage(self, dict):
        """
        Cette méthode permet de créer une image filtrée.
        Paramètres : self (SoftwareController) : L'instance de la classe.
                    dict (dict) : Dictionnaire contenant les informations des filtres.
        Return : None
        """
        self.model.filteredImage(dict)

    # --- Autre --- #

    def show(self):
        """
        Cette méthode permet d'afficher la vue.
        Paramètres : self (SoftwareController) : L'instance de la classe.
        Return : None
        """
        self.view.showMaximized()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = SoftwareController()
    controller.show()
    sys.exit(app.exec())