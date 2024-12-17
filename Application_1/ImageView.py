import sys,json,os
import numpy as np
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
        self.grayData = ImageView.emptyImageGrayData()
        self.scene.addText("Aucune image n'est actuellement ouverte.")
        self.setScene(self.scene)
        self.setWindowTitle("QGraphicsView")

    def setPixmap(self, grayData :  np.ndarray):
        """
        Définit l'image pour la vue.
        
        Paramètres : fname (str) : Le nom du fichier de l'image à définir comme image de la vue.
        Return : None
        """
        height, width = grayData.shape
        bytesPerLine = width

        # Normalisation
        grayData[grayData > 1.0] = 1.0
        grayData[grayData < 0.0] = 0.0

        # Convertir en QImage
        qImg : QImage = QImage((grayData * 255).astype(np.uint8).data, width, height, bytesPerLine, QImage.Format.Format_Grayscale8)
        self.pixmap : QPixmap = QPixmap.fromImage(qImg)
        self.pixmap = self.pixmap.scaled(int(self.width()), int(self.height()), Qt.AspectRatioMode.KeepAspectRatio)
        image_item = QGraphicsPixmapItem(self.pixmap)

        self.scene.addItem(image_item)

    @staticmethod
    def emptyImageGrayData()-> np.ndarray: return np.ones((90,160))*(220/255) 