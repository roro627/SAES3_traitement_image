import os,sys
from PyQt6 import QtCore
from PyQt6.QtWidgets import *
from PyQt6.QtCore import pyqtSignal
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
        self.setWindowTitle("Application de filtres")

        # Layouts
        mainLayout = QVBoxLayout()
        filterLayout = QVBoxLayout()
        
        # Widgets
        self.filter = QComboBox()
        self.filter.addItems(["Filtre 1","Filtre 2","Filtre 3"])

        self.labelR = QLabel("Rouge (R)")
        self.labelV = QLabel("Vert (V)")
        self.labelB = QLabel("Bleu (B)")

        filterLayout.addWidget(self.filter)

        # Créer une figure matplotlib
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        # Ajouter un layout pour le widget
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)

        mainLayout.addLayout(filterLayout)
        mainLayout.addLayout(layout)

        self.setLayout(mainLayout)

