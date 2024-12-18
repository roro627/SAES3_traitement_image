import sys,os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from PyQt6.QtCore import pyqtSignal

from ImageView import ImageView
from FilterDialog import FilterDialog

# -----------------------------------------------------------------------------
# --- classe SoftwareView
# -----------------------------------------------------------------------------

class SoftwareView(QMainWindow):

    # Constructeur
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Logiciel de traitement d'images astronomiques")

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
        menu_file.addAction('Ouvrir un fichier', self.openImage)
        menu_file.addAction('Ouvrir un dossier', self.openFolder)
        menu_filter = menu_bar.addMenu('&Filtres')
        menu_filter.addAction('Appliquer un filtre',self.openFilterDialog)

        # Layouts
        layout_tools = QHBoxLayout()
        tab1_layout = QVBoxLayout()

        # Widgets
        self.image = ImageView()
        self.tabWidget = QTabWidget()
        self.filter = FilterDialog()

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(2)
        self.table_widget.setHorizontalHeaderLabels(["Clé", "Valeur"])
        self.table_widget.verticalHeader().setVisible(False)
        header = self.table_widget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        header.setStretchLastSection(True)

        self.tab1 = QWidget()
        self.tab1.setLayout(tab1_layout)
        tab1_layout.addWidget(self.table_widget)
        self.tabWidget.addTab(self.tab1,'Fits Header')

        # Ajout de widgets dans le layout layout_tools
        layout_tools.addWidget(self.image)
        layout_tools.addWidget(self.tabWidget, alignment=Qt.AlignmentFlag.AlignRight)

        mainlayout.addLayout(layout_tools)

    # Signals
    imageButtonClicked = pyqtSignal(str)
    folderButtonClicked = pyqtSignal(str)

    filterButtonClicked = pyqtSignal()

    # Methodes
    def openImage(self) -> None:
        """
        Cette méthode permet d'ouvrir une boîte de dialogue de sélection de fichier pour choisir une image.
        Paramètres :self (SoftwareView) : L'instance de la classe.
        Return : None
        """
        fpath = QFileDialog.getOpenFileName(self, 'Open file',self.parent_directory,"*.fit *.fits *.fts")[0]
        if fpath != "": # Si l'utilisateur ne sélectionne aucun fichier.
            self.imageButtonClicked.emit(fpath)

    def openFolder(self) -> None :
        fpath = QFileDialog.getExistingDirectory(self, 'Open folder', self.parent_directory)
        if fpath != "": # Si l'utilisateur ne sélectionne aucun répertoire.
            imageList = os.listdir(fpath)
            for image in imageList:
                pass


    def openFilterDialog(self) -> None :
        self.filter.exec()
        self.filterButtonClicked.emit()
    
    def updateInfoTable(self, infoHeader) -> None :
        """
        Cette méthode permet de mettre à jour le tableau contenant les informations de l'entête d'une image FITS.
        Paramètres :self (SoftwareView) : L'instance de la classe.
                    infoHeader (fits.header.Header) : Entête d'une image FITS.
        Return : None
        """
        self.table_widget.setRowCount(len(infoHeader))

        index : int = 0
        for (key, value) in infoHeader.items():

            itemkey = QTableWidgetItem(f"{key}")
            self.table_widget.setItem(index, 0, itemkey)

            itemvalue = QTableWidgetItem(f"{value}")
            self.table_widget.setItem(index, 1, itemvalue)
            index += 1

if __name__ == "__main__":  
    print(' ----- Execution du logiciel ----- ')
    app = QApplication(sys.argv)
    fenetre = SoftwareView()
    fenetre.showMaximized()
    sys.exit(app.exec())