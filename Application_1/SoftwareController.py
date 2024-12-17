from SoftwareView import SoftwareView
from SoftwareModel import SoftwareModel

from PyQt6.QtWidgets import *
from PyQt6.QtWidgets import QApplication
import sys, os

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
        self.view.imageButtonClicked.connect(self.openImage)

    # --- Méthodes pour View --- #

    def openImage(self, fpath):
        self.model.setImagePath(fpath)
        data = self.model.openImage()
        self.view.image.setPixmap(data)
        self.view.updateInfoTable(self.model.ImageHead)

    def show(self):
        """
        Cette méthode permet d'afficher la vue.
        
        Paramètres : self : L'instance de la classe.
        Return : None
        """
        self.view.showMaximized()

if __name__ == "__main__":

    app = QApplication(sys.argv)

    controller = SoftwareController()
    controller.show()

    sys.exit(app.exec())