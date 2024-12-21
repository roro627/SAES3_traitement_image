import sys,os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QIcon

from ImageView import ImageView
from FilterDialog import FilterDialog
from qt_dl import MainWindow as DlWindow

# -----------------------------------------------------------------------------
# --- classe SoftwareView
# --- Fait par : COCQUEREL Alexis et LAMBERT Romain
# -----------------------------------------------------------------------------

class SoftwareView(QMainWindow):

    # Constructeur
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Logiciel de traitement d'images astronomiques")
        self.setWindowIcon(QIcon("icons//telescope_icon.ico"))
        self.current_directory = sys.path[0]
        self.parent_directory = os.path.dirname(self.current_directory)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout vertical --> principal layout
        mainlayout = QVBoxLayout()
        central_widget.setLayout(mainlayout)

        # Menu bar
        menu_bar = self.menuBar()
        menu_file = menu_bar.addMenu('&Fichier')
        menu_file.addAction('Ouvrir un fichier', self.openFile)
        menu_file.addAction('Ouvrir un dossier', self.openFolder)
        menu_file.addSeparator()
        menu_file.addAction('Exporter', self.exportFile)
        menu_filter = menu_bar.addMenu('&Filtre')
        menu_filter.addAction(QIcon(self.current_directory+"//icons//color_icon.ico"),'Conversion polychromatique (RVB)', self.openFilterDialog)
        menu_download = menu_bar.addMenu('&Téléchargement')
        menu_download.addAction(QIcon(self.current_directory+"//icons//icon_downloader_app.ico"), 'Télécharger des FITS', self.dlFits)

        # Layouts
        tab_layout = QVBoxLayout()

        # Widgets
        self.image = ImageView()
        self.dl = DlWindow()
        self.tabWidget = QTabWidget()
        self.filter = FilterDialog()

        self.tab = QWidget()
        self.tab.setLayout(tab_layout)
        tab_layout.addWidget(self.image)
        self.tabWidget.addTab(self.tab,'Pas de fichier(s)')

        # Ajout de widgets dans le layout layout_tools
        mainlayout.addWidget(self.tabWidget)
        
    # Signaux
    fileButtonClicked = pyqtSignal(list)
    folderButtonClicked = pyqtSignal(list)
    exportButtonClicked = pyqtSignal()

    # Methodes
    def openFile(self) -> None:
        """
        Cette méthode permet d'ouvrir une boîte de dialogue de sélection de fichier pour choisir une image.
        Paramètres :self (SoftwareView) : L'instance de la classe.
        Return : None
        """
        fpath = QFileDialog.getOpenFileName(self, 'Open file',self.parent_directory,"*.fit *.fits *.fts")[0]
        if fpath != "": # Si l'utilisateur ne sélectionne aucun fichier.
            self.fileButtonClicked.emit([fpath])

    def openFolder(self) -> None :
        """
        Cette méthode permet d'ouvrir une boîte de dialogue de sélection de répertoire pour choisir des images.
        Paramètres :self (SoftwareView) : L'instance de la classe.
        Return : None
        """
        fpath = QFileDialog.getExistingDirectory(self, 'Open folder', self.parent_directory)
        if fpath != "": # Si l'utilisateur ne sélectionne aucun répertoire.
            imageListName = os.listdir(fpath)
            imageListPath = []

            for image in imageListName : 
                imagePath = fpath + '/' + image
                imageListPath.append(imagePath)
            
            self.folderButtonClicked.emit(imageListPath)
    
    def exportFile(self) -> None :
        """
        Cette méthode permet d'exporter l'image filtrée.
        Paramètres :self (SoftwareView) : L'instance de la classe.
        Return : None
        """
        self.exportButtonClicked.emit()
        
    def dlFits(self) -> None :
        """
        Cette méthode permet d'ouvrir une fenêtre de téléchargement de fichiers FITS.
        Paramètres :self (SoftwareView) : L'instance de la classe.
        Return : None
        """
        self.dl.show()

    def openFilterDialog(self) -> None :
        """
        Cette méthode permet d'ouvrir une boîte de dialogue pour choisir les filtres à appliquer.
        Paramètres :self (SoftwareView) : L'instance de la classe.
        Return : None
        """
        self.filter.exec()