from SoftwareView import SoftwareView
from SoftwareModel import SoftwareModel

from PyQt6.QtWidgets import *
from PyQt6.QtWidgets import QApplication
import sys, os
import matplotlib.pyplot as plt

# -----------------------------------------------------------------------------
# --- classe SoftwareController
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
        Cette méthode est utilisé lors de l'ouverture d'une image FITS.
        Quand un fichier FITS est ouvert celui-ci est affiché ainsi que l'ensemble de ses informations situées dans l'entête.
        Paramètres : self (SoftwareController) : L'instance de la classe.
                    fpath (str) : Chemin vers l'image FITS.
        Return : None
        """
        self.model.ImageHead = []
        self.model.ImageFilter = {}
        self.model.ImageBody = []
        self.view.tabWidget.clear()
        self.view.tabWidget2.clear()
        self.view.filter.clearFilter()

        self.model.setImagePath(fpath)
        datas = self.model.openImage()
        self.view.image.addImagesToTabWidget(datas, self.view.tabWidget2)
        self.view.updateInfoTable(self.model.ImageHead[0])

    def openFolder(self, fpath):
        self.model.ImageHead = []
        self.model.ImageFilter = {}
        self.model.ImageBody = []
        self.view.tabWidget.clear()
        self.view.tabWidget2.clear()

        self.view.filter.clearFilter()


        self.model.setImagePath(fpath)
        datas = self.model.openImage()
        self.view.image.addImagesToTabWidget(datas, self.view.tabWidget2)

        self.view.filter.updateFilter(self.model.ImageFilter)

        for imgHead in self.model.ImageHead : self.view.updateInfoTable(imgHead)

    def saveImage(self):
        self.model.exportAsPNG()

    # --- Méthodes pour View.filter --- #

    def createFilteredImage(self, dict):
        img = self.model.filteredImage(dict)
        self.view.image.setColorPixmap(img)

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