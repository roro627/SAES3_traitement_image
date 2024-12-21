import numpy as np
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from astropy.io import fits

# -----------------------------------------------------------------------------
# --- classe ImageView
# --- Fait par : COCQUEREL Alexis et LAMBERT Romain
# -----------------------------------------------------------------------------

class ImageView(QGraphicsView):

    # Constructeur
    def __init__(self):
        super().__init__()

        self.scene = QGraphicsScene()
        self.scene.addText("Aucune image n'est actuellement ouverte.")
        self.setScene(self.scene)

    def setPixmap(self, grayData: np.ndarray) -> None:
        """
        Cette méthode est utilisée pour afficher en niveaux de gris dans la vue une image FITS.
        Paramètres : self (ImageView) : L'instance de la classe.
                    grayData (np.ndarray): Tableau numpy représentant l'image en niveaux de gris.
        Return 
        """
        height, width = grayData.shape
        bytesPerLine = grayData.strides[0]

        self.scene.clear()
        # Convertir en QImage
        qImg: QImage = QImage(grayData.data, width, height, bytesPerLine, QImage.Format.Format_Grayscale8)
        self.pixmap: QPixmap = QPixmap.fromImage(qImg)
        
        self.pixmap = self.pixmap.scaled(int(self.pixmap.width()), int(self.pixmap.height()), Qt.AspectRatioMode.KeepAspectRatio)
        image_item = QGraphicsPixmapItem(self.pixmap)

        self.scene.addItem(image_item)
        self.fitInView(image_item, Qt.AspectRatioMode.KeepAspectRatio) 
        self.scale(1.8, 1.8) # Zoom par défaut

    def addInfoToTabWidget(self, images: list[np.ndarray], infoHeader : fits.header.Header, tabWidget: QTabWidget):
        """
        Cette méthode est utilisée pour ajouter des images à un QTabWidget ainsi qu'un QTableWidget qui contient les métadonnées de ces images.
        Paramètres : self (ImageView) : L'instance de la classe.
                    images (list[np.ndarray]) : Liste des images à afficher.
                    infoHeader (fits.header.Header) : Informations de l'entête de l'image.
                    tabWidget (QTabWidget) : Le QTabWidget dans lequel les images seront ajoutées.
        Return : None
        """
        for i, image in enumerate(images):

            # Créer un nouvel onglet contenant un ImageViewer
            image_viewer = ImageView()
            image_viewer.setPixmap(image)

            # Créer un QTableWidget contenant les informations de l'entête
            table_widget = QTableWidget()
            table_widget.setColumnCount(2)
            table_widget.setHorizontalHeaderLabels(["Clé", "Valeur"])
            table_widget.verticalHeader().setVisible(False)
            table_widget.setMinimumWidth(250)
            header = table_widget.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
            header.setStretchLastSection(True)
            table_widget.setRowCount(len(infoHeader[i]))

            # Ajouter les informations de l'entête dans le QTableWidget
            index : int = 0
            for (key, value) in infoHeader[i].items():

                itemkey = QTableWidgetItem(f"{key}")
                table_widget.setItem(index, 0, itemkey)

                itemvalue = QTableWidgetItem(f"{value}")
                table_widget.setItem(index, 1, itemvalue)
                index += 1

            # Créer un widget conteneur pour l'onglet
            tabContainer = QWidget()
            layout = QHBoxLayout()
            layout.addWidget(image_viewer)
            layout.addWidget(table_widget, alignment=Qt.AlignmentFlag.AlignRight)
            tabContainer.setLayout(layout)

            # Ajouter l'onglet au QTabWidget
            tabWidget.addTab(tabContainer, f"Image {i + 1}")

    def wheelEvent(self, event : QWheelEvent) -> None:
        """
        Cette méthode est utilisée pour gérer le zoom de la vue.
        Paramètres : self (ImageView) : L'instance de la classe.
                    event (QWheelEvent) : L'événement de la molette de la souris.
        Return : None
        """
        zoom_in = 1.15
        zoom_out = 0.85

        if event.angleDelta().y() > 0:
            self.scale(zoom_in, zoom_in)
        else:
            self.scale(zoom_out, zoom_out)