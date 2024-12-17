from SoftwareView import SoftwareView
from PyQt6.QtWidgets import QApplication
import sys, os

# -----------------------------------------------------------------------------
# --- classe SoftwareController
# -----------------------------------------------------------------------------

class SoftwareController():
    def __init__(self):
        
        # Initialiser les vues et les modèles
        self.view = SoftwareView()

        # Connecter les signaux de la vue aux slots du contrôleur

        # -------------- Signaux de View -------------- #
        self.view.imageButtonClicked.connect(self.test)

    # --- Méthodes pour View --- #

    def test(self, fname):
        print('test')
        var = os.path.dirname(sys.path[0]) + '\\' + fname
        print(var)
        self.view.image.setPixmap(var)


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