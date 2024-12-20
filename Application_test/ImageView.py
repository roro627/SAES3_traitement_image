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

    def setPixmap(self, datas):
        """
        Définit l'image pour la vue.
        
        Paramètres : fname (str) : Le nom du fichier de l'image à définir comme image de la vue.
        Return : None
        """
        data = datas[0]
        height, width = data.shape
        bytes_per_line = data.strides[0]
        self.image = QImage(data.data, width, height, bytes_per_line, QImage.Format.Format_Grayscale8)

        # Convertir QImage en QPixmap
        pixmap = QPixmap.fromImage(self.image)

        # Configurer la scène et ajouter le pixmap
        self.scene = QGraphicsScene()
        self.scene.addPixmap(pixmap)
        self.setScene(self.scene)

        # Configurer le zoom avec la molette de la souris
        self.setMouseTracking(True)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)

    def wheelEvent(self, event):
        zoom_in = 1.15
        zoom_out = 0.85

        if event.angleDelta().y() > 0:
            self.scale(zoom_in, zoom_in)
        else:
            self.scale(zoom_out, zoom_out)

        

    @staticmethod
    def emptyImageGrayData()-> np.ndarray: return np.ones((90,160))*(220/255) 