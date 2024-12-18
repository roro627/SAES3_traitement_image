import os,sys
from PyQt6 import QtCore
from PyQt6.QtWidgets import *
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon
import matplotlib.pyplot as plt

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

# -----------------------------------------------------------------------------
# --- classe FilterDialog
# -----------------------------------------------------------------------------

class FilterDialog(QDialog):
    
    # Constructeur

    def __init__(self) :
        super().__init__()
        self.setWindowTitle("Conversion polychromatique (RVB)")
        self.setMinimumSize(QSize(500, 50))

        # Layouts
        mainLayout = QVBoxLayout()
        filterLayout = QVBoxLayout()
        composantRLayout = QHBoxLayout()
        composantVLayout = QHBoxLayout()
        composantBLayout = QHBoxLayout()
        
        # Widgets
        self.filterR = QComboBox()
        self.filterV = QComboBox()
        self.filterB = QComboBox()

        self.labelR = QLabel("(R) Rouge")
        self.labelV = QLabel("(V) Vert")
        self.labelB = QLabel("(B) Bleu")

        self.applyBtn = QPushButton("Appliquer")

        composantRLayout.addWidget(self.labelR)
        composantRLayout.addWidget(self.filterR)

        composantVLayout.addWidget(self.labelV)
        composantVLayout.addWidget(self.filterV)

        composantBLayout.addWidget(self.labelB)
        composantBLayout.addWidget(self.filterB)

        filterLayout.addLayout(composantRLayout)
        filterLayout.addLayout(composantVLayout)
        filterLayout.addLayout(composantBLayout)
        filterLayout.addWidget(self.applyBtn)

        # Ajouter un layout pour le widget
        layout = QVBoxLayout()

        mainLayout.addLayout(filterLayout)
        mainLayout.addLayout(layout)

        self.setLayout(mainLayout)
    
    def updateFilter(self, filterList):
        self.filterR.clear(), self.filterV.clear(), self.filterB.clear()
        self.filterR.addItems(filterList)
        self.filterV.addItems(filterList)
        self.filterB.addItems(filterList)

