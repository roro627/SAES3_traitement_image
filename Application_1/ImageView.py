import sys,json,os
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtCore import pyqtSignal

# -----------------------------------------------------------------------------
# --- classe ImageView
# -----------------------------------------------------------------------------

class ImageView(QGraphicsView):
    # Constructeur
    def __init__(self):
        super().__init__()

        self.scene = QGraphicsScene()
        self.scene.addText("Aucune image n'est actuellement ouverte.")
        self.setScene(self.scene)
        self.setWindowTitle("QGraphicsView")

    def setPixmap(self,fname):
        """
        Définit l'image pour la vue.
        
        Paramètres : fname (str) : Le nom du fichier de l'image à définir comme image de la vue.
        Return : None
        """
        self.pixmap = QPixmap(fname)
        self.pixmap = self.pixmap.scaled(int(self.width()), int(self.height()), Qt.AspectRatioMode.KeepAspectRatio)
        self.pixmap_height = self.pixmap.height()
        self.pixmap_width = self.pixmap.width()
        image_item = QGraphicsPixmapItem(self.pixmap)
        self.scene.addItem(image_item)