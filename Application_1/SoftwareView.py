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
        menu_file.addAction('Ouvrir', self.openImage)
        menu_filter = menu_bar.addMenu('&Filtres')
        menu_filter.addAction('Appliquer un filtre')

        # Layouts
        self.layout_test = QHBoxLayout()

        # Widgets
        self.image = ImageView()
        self.tabWidget = QTabWidget()

        tab1 = QWidget()
        tab1_layout = QVBoxLayout()
        tab1.setLayout(tab1_layout)

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(2)
        self.table_widget.setHorizontalHeaderLabels(["Clé", "Valeur"])
        self.table_widget.verticalHeader().setVisible(False)

        tab1_layout.addWidget(self.table_widget)
        self.tabWidget.addTab(tab1,'Fits Header')

        self.layout_test.addWidget(self.image)
        self.layout_test.addWidget(self.tabWidget, alignment=Qt.AlignmentFlag.AlignRight)

        mainlayout.addLayout(self.layout_test)

    # Signals
    imageButtonClicked = pyqtSignal(str)

    # Methodes
    def openImage(self) -> None:
        """
        Cette méthode permet d'ouvrir une boîte de dialogue de sélection de fichier pour choisir une image.
        Paramètres :self (newProjectDialog): L'instance de la classe.
        Return : None
        """
        fpath = QFileDialog.getOpenFileName(self, 'Open file',self.parent_directory,"*.fit *.fits *.fts")[0]
        if fpath != "": # Si l'utilisateur ne sélectionne aucun fichier.
            self.imageButtonClicked.emit(fpath)
    
    def updateInfoTable(self, infoHeader):

        self.table_widget.setRowCount(len(infoHeader))

        i = 0
        for (key, value) in infoHeader.items():
            itemkey = QTableWidgetItem(f"{key}")
            self.table_widget.setItem(i, 0, itemkey)
            itemvalue = QTableWidgetItem(f"{value}")
            self.table_widget.setItem(i, 1, itemvalue)
            i += 1

        self.table_widget.resizeColumnsToContents()

if __name__ == "__main__":  
    print(' ----- Execution du logiciel ----- ')
    app = QApplication(sys.argv)
    fenetre = SoftwareView()
    fenetre.showMaximized()
    sys.exit(app.exec())