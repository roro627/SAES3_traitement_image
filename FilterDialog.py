import os,sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import QSize, pyqtSignal
from PyQt6.QtGui import QIcon

# -----------------------------------------------------------------------------
# --- classe FilterDialog
# --- Fait par : COCQUEREL Alexis et LAMBERT Romain
# -----------------------------------------------------------------------------

class FilterDialog(QDialog):
    
    # Constructeur

    def __init__(self) :
        super().__init__()

        self.current_directory = sys.path[0]
        self.parent_directory = os.path.dirname(self.current_directory)
        
        self.setWindowIcon(QIcon(self.current_directory+"//icons//color_icon.ico"))
        self.setWindowTitle("Conversion polychromatique (RVB)")
        self.setMinimumSize(QSize(500, 50))

        # Layouts
        filterLayout = QVBoxLayout()
        composantRLayout = QHBoxLayout()
        composantVLayout = QHBoxLayout()
        composantBLayout = QHBoxLayout()
        
        # Widgets
        self.filterR = QComboBox()
        self.filterV = QComboBox()
        self.filterB = QComboBox()

        self.labelColorRed = QLabel()
        self.labelColorRed.setStyleSheet('background-color: red')
        self.labelColorRed.setMaximumSize(QSize(15,15))

        self.labelColorGreen = QLabel()
        self.labelColorGreen.setStyleSheet('background-color: green')
        self.labelColorGreen.setMaximumSize(QSize(15,15))

        self.labelColorBlue = QLabel()
        self.labelColorBlue.setStyleSheet('background-color: blue')
        self.labelColorBlue.setMaximumSize(QSize(15,15))

        self.labelR = QLabel("Rouge")
        self.labelV = QLabel("Vert")
        self.labelB = QLabel("Bleu")

        self.applyBtn = QPushButton("Appliquer")
        self.applyBtn.clicked.connect(self.getColorFilter)

        # Ajout des widgets dans les layouts
        composantRLayout.addWidget(self.labelColorRed)
        composantRLayout.addWidget(self.labelR)
        composantRLayout.addWidget(self.filterR)

        composantVLayout.addWidget(self.labelColorGreen)
        composantVLayout.addWidget(self.labelV)
        composantVLayout.addWidget(self.filterV)

        composantBLayout.addWidget(self.labelColorBlue)
        composantBLayout.addWidget(self.labelB)
        composantBLayout.addWidget(self.filterB)

        # Ajout des layouts dans le filterLayout
        filterLayout.addLayout(composantRLayout)
        filterLayout.addLayout(composantVLayout)
        filterLayout.addLayout(composantBLayout)
        filterLayout.addWidget(self.applyBtn)

        self.setLayout(filterLayout)

    # Signal
    applyButtonClicked = pyqtSignal(dict)

    def clearFilter(self) -> None :
        """
        Cette méthode permet de supprimer les items qui sont insérés dans les QComboBox.
        Paramètres :self (FilterDialog): L'instance de la classe.
        Return : None
        """
        self.filterR.clear(), self.filterV.clear(), self.filterB.clear()

    def updateFilter(self, filterList : dict) -> None:
        """
        Cette méthode permet de mettre à jour les filtres dans les QComboBox à partir des clés d'un dictionnaire.
        Paramètres :self (FilterDialog): L'instance de la classe.
                    filterList (dict): Dictionnaire qui contient les associations filtre => matrice
        Return : None
        """
        self.filterR.addItems(filterList.keys())
        self.filterV.addItems(filterList.keys())
        self.filterB.addItems(filterList.keys())
    
    def getColorFilter(self) -> dict :
        """
        Cette méthode permet d'avoir le nom des filtres associés au code RVB sous forme de dictionnaire.
        Paramètres :self (FilterDialog): L'instance de la classe.
        Return :dict: Un dictionnaire contenant les filtres choisis.
        """
        dictionary = {}
        if self.filterR.currentText() != "" and self.filterV.currentText() != "" and self.filterB.currentText() != "":
            dictionary["Red"] = self.filterR.currentText()
            dictionary["Green"] = self.filterV.currentText()
            dictionary["Blue"] = self.filterB.currentText()
            self.applyButtonClicked.emit(dictionary)
            self.close()
        return dictionary