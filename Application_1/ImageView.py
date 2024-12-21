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

    def setPixmap(self, pixmap):
        scene = QGraphicsScene()
        scene.addPixmap(pixmap)
        self.setScene(scene)

    def addImagesToTabs(self, datas, tabname: QTabWidget):
        for data in datas:
            height, width = data.shape
            bytes_per_line = data.strides[0]
            image = QImage(data.data, width, height, bytes_per_line, QImage.Format.Format_Grayscale8)

            # Convertir QImage en QPixmap
            pixmap = QPixmap.fromImage(image)
            pixmap = pixmap.scaled(int(width), int(height), Qt.AspectRatioMode.KeepAspectRatio)

            # Créer un widget pour l'onglet
            tabWidget = QWidget()
            tabLayout = QVBoxLayout()
            tabWidget.setLayout(tabLayout)

            # Créer une nouvelle instance de QGraphicsView
            graphicsView = ImageView()
            graphicsView.setPixmap(pixmap)

            # Ajouter la vue au layout de l'onglet
            tabLayout.addWidget(graphicsView)

            # Ajouter l'onglet avec le widget
            tabname.addTab(tabWidget, 'FITS Header')


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