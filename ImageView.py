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

    def setPixmap(self, grayData: np.ndarray):
        """
        Définit l'image pour la vue.
        """
        height, width = grayData.shape
        bytesPerLine = grayData.strides[0]

        self.scene.clear()

        # Convertir en QImage
        qImg: QImage = QImage(grayData.data, width, height, bytesPerLine, QImage.Format.Format_Grayscale8)
        self.pixmap: QPixmap = QPixmap.fromImage(qImg)
        
        self.pixmap = self.pixmap.scaled(int(self.pixmap.width()), int(self.pixmap.height()), Qt.AspectRatioMode.KeepAspectRatio)
        #self.pixmap = self.pixmap.scaled(int(self.width()), int(self.height()), Qt.AspectRatioMode.KeepAspectRatio)
        image_item = QGraphicsPixmapItem(self.pixmap)

        self.scene.addItem(image_item)

    def addImagesToTabWidget(self, images: list[np.ndarray], tabWidget: QTabWidget):
        """
        Ajoute une liste d'images dans un QTabWidget, chaque image dans un nouvel onglet.

        Paramètres:
            images (list[np.ndarray]): Liste de tableaux numpy représentant les images en niveaux de gris.
            tabWidget (QTabWidget): Le QTabWidget où les images seront ajoutées.

        Retourne:
            None
        """
        for i, image in enumerate(images):
            # Créer un nouvel onglet contenant un ImageViewer
            image_viewer = ImageView()
            image_viewer.setPixmap(image)

            # Créer un widget conteneur pour l'onglet
            tabContainer = QWidget()
            layout = QVBoxLayout()
            layout.addWidget(image_viewer)
            tabContainer.setLayout(layout)

            # Ajouter l'onglet au QTabWidget
            tabWidget.addTab(tabContainer, f"Image {i + 1}")



    def setColorPixmap(self, data):
        height, width , channel  = data.shape   
        bytesPerLine = channel * width

        # clip
        data[data>1.0] = 1.0
        data[data<0.0] = 0.0

        qImg : QImage= QImage(bytes((data*255).astype(np.uint8)), width, height, bytesPerLine, QImage.Format.Format_RGB888) # QImage
        self.pixmap : QPixmap = QPixmap.fromImage(qImg)
        self.pixmap = self.pixmap.scaled(int(self.width()), int(self.height()), Qt.AspectRatioMode.KeepAspectRatio)
        image_item = QGraphicsPixmapItem(self.pixmap)

        self.scene.addItem(image_item)


    def wheelEvent(self, event):
        zoom_in = 1.15
        zoom_out = 0.85

        if event.angleDelta().y() > 0:
            self.scale(zoom_in, zoom_in)
        else:
            self.scale(zoom_out, zoom_out)

        

    @staticmethod
    def emptyImageGrayData()-> np.ndarray: return np.ones((90,160))*(220/255) 