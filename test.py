import sys
import numpy as np
from astropy.io import fits
from PyQt6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import Qt

class FITSViewer(QGraphicsView):
    def __init__(self, fits_path):
        super().__init__()

        # Charger les données FITS avec vérification
        try:
            data = fits.getdata(fits_path)
        except Exception as e:
            print(f"Erreur de chargement du fichier FITS : {e}")
            sys.exit(1)

        # Éliminer les valeurs aberrantes
        data = np.clip(data, np.percentile(data, 1), np.percentile(data, 99))

        # Normaliser les données
        norm_data = 255 * (data - np.min(data)) / (np.max(data) - np.min(data))
        norm_data = np.clip(norm_data, 0, 255).astype(np.uint8)

        # Assurez-vous que les données sont contiguës
        norm_data = np.ascontiguousarray(norm_data)

        # Créer un QImage à partir des données normalisées
        height, width = norm_data.shape
        bytes_per_line = norm_data.strides[0]
        self.image = QImage(norm_data.data, width, height, bytes_per_line, QImage.Format.Format_Grayscale8)

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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = FITSViewer(r'downloads\j8vp03olq_raw.fits')
    viewer.setWindowTitle("FITS Viewer avec Zoom")
    viewer.show()
    sys.exit(app.exec())
