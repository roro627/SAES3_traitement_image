import sys,os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from PyQt6.QtCore import pyqtSignal

from ImageView import ImageView

# -----------------------------------------------------------------------------
# --- classe SoftwareView
# -----------------------------------------------------------------------------

class SoftwareView(QMainWindow):

    # Constructeur
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Logiciel de traitement d'images astronomiques")

        current_directory = sys.path[0]
        self.parent_directory = os.path.dirname(current_directory)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout vertical --> principal layout
        mainlayout = QVBoxLayout()
        central_widget.setLayout(mainlayout)

        # Menu bar
        menu_bar = self.menuBar()
        menu_file = menu_bar.addMenu('&Fichier')
        menu_file.addAction('Ouvrir', self.openImage)

        # Layouts
        layout_test = QHBoxLayout()

        # Widgets
        self.image = ImageView()

        layout_test.addWidget(self.image)

        mainlayout.addLayout(layout_test)

    # Signals
    imageButtonClicked = pyqtSignal(str)

    # Methodes
    def openImage(self) -> None:
        """
        Cette méthode permet d'ouvrir une boîte de dialogue de sélection de fichier pour choisir une image.
        Paramètres :self (newProjectDialog): L'instance de la classe.
        Return : None
        """
        fpath = QFileDialog.getOpenFileName(self, 'Open file',self.parent_directory,"*.fit *.fits *.fts *.jpg")[0]
        if fpath != "": # Si l'utilisateur ne sélectionne aucun fichier.
            fname = os.path.basename(fpath)
            self.imageButtonClicked.emit(fname)


if __name__ == "__main__":  
    print(' ----- Execution du logiciel ----- ')
    app = QApplication(sys.argv)
    fenetre = SoftwareView()
    fenetre.showMaximized()
    sys.exit(app.exec())