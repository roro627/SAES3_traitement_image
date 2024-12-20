import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QLineEdit, QSpinBox
from PyQt6.QtCore import QSize, QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QIcon
import itertools

from download_file import *

from astropy.io import fits

"""
TODO:
    - supprimer programme et mettre 3 comboboxes pour les filtres
    - lors du dl crée un dossier avec le nom de l'objet et datetime (pour le rendre unqiue) puis dl dedans les fichiers
"""

class SearchThread(QThread):
    """
    Thread pour la recherche d'observations.
    """
    observations_ready = pyqtSignal()
    celestial_objects_ready = pyqtSignal(list)

    def __init__(self, object_name, radius,main_window):
        super().__init__()
        self.object_name = object_name
        self.radius = radius
        self.main_window = main_window

    def run(self):
        observations = get_observations(self.object_name, self.radius)
        
        observations, obs2 = itertools.tee(observations, 2)
        self.main_window.observations = observations
        self.observations_ready.emit()
                
        self.celestial_objects_ready.emit(get_celestial_objects(obs2))

class DownloadThread(QThread):
    """
    Thread pour le téléchargement des fichiers.
    """
    download_complete = pyqtSignal(object)

    def __init__(self, final_product, output_directory, main_window):
        super().__init__()
        self.final_product = final_product
        self.output_directory = output_directory
        self.main_window = main_window  

    def run(self):
        # Désactiver les entrées avant le téléchargement
        self.main_window.disable_inputs()
        manifest = download_observations(self.final_product, self.output_directory)
        self.download_complete.emit(manifest)

class MainWindow(QWidget):
    """
    Fenêtre principale de l'application.
    """
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Downloader App")
        self.setMinimumSize(QSize(500, 50))
        self.setWindowIcon(QIcon("icon_downloader_app.ico"))
        
        self.value_to_add = 35
        self.current_height = self.value_to_add
        self.maxsize = 500
        
        self.output_directory = "downloads"
        self.ideal_Mo_size = 70  # Valeur par défaut
        
        # Message par défaut pour les combobox
        self.message_program = "Sélectionner un programme"
        self.message_filter = "Sélectionner un filtre"
        self.message_celestial = "Sélectionner un objet céleste"

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Champs de saisie pour l'objet et le rayon
        self.layout.addWidget(QLabel("Entrez le nom de l'objet (ex:M31):"))
        self.object_input = QLineEdit()
        self.layout.addWidget(self.object_input)

        self.layout.addWidget(QLabel("Entrez le rayon de recherche en degrés (ex: 0.1):"))
        self.radius_input = QLineEdit()
        self.layout.addWidget(self.radius_input)

        # Ajouter le widget pour modifier ideal_Mo_size
        self.layout.addWidget(QLabel("Entrez la taille idéale du fichier à télécharger (en Mo) (ex: 70):"))
        self.size_input = QSpinBox()
        self.size_input.setRange(1, 1000)  # Valeurs possibles
        self.size_input.setValue(self.ideal_Mo_size)  # Valeur par défaut
        self.layout.addWidget(self.size_input)

        # Bouton pour démarrer la recherche
        self.search_button = QPushButton("Rechercher")
        self.search_button.clicked.connect(self.start_search)
        self.layout.addWidget(self.search_button)
        
        # Label pour les champs manquants
        self.missing_input_label = QLabel("Veuillez remplir les champs ci-dessus.")
        self.layout.addWidget(self.missing_input_label)
        self.missing_input_label.hide()

        # Création de tous les widgets au début en les cachant

        self.celestial_label = QLabel("Sélectionner un objet céleste:")
        self.layout.addWidget(self.celestial_label)
        self.celestial_label.hide()

        self.celestial_combo = QComboBox()
        self.celestial_combo.currentTextChanged.connect(self.populate_filter_combo)
        self.layout.addWidget(self.celestial_combo)
        self.celestial_combo.hide()

        self.filter_label = QLabel("Sélectionner un filtre:")
        self.layout.addWidget(self.filter_label)
        self.filter_label.hide()

        self.filter_combo = QComboBox()
        self.filter_combo.currentTextChanged.connect(self.populate_program_combo)
        self.layout.addWidget(self.filter_combo)
        self.filter_combo.hide()

        self.program_label = QLabel("Sélectionner un programme:")
        self.layout.addWidget(self.program_label)
        self.program_label.hide()

        self.program_combo = QComboBox()
        self.program_combo.currentTextChanged.connect(self.manage_final_product)
        self.layout.addWidget(self.program_combo)
        self.program_combo.hide()
        
        self.result_label = QLabel("")
        self.layout.addWidget(self.result_label)
        self.result_label.hide()

        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.update_search_button_text)
        self.animation_texts = ["Recherche en cours", "Recherche en cours .", "Recherche en cours ..", "Recherche en cours ..."]
        self.animation_index = 0

        self.result_label_timer = QTimer()
        self.result_label_timer.timeout.connect(self.update_result_label_text)
        self.result_label_texts = [
            "Fichier FITS trouvé, téléchargement en cours",
            "Fichier FITS trouvé, téléchargement en cours .",
            "Fichier FITS trouvé, téléchargement en cours ..",
            "Fichier FITS trouvé, téléchargement en cours ..."
        ]
        self.result_label_index = 0

        self.adjust_window_size()

    def disable_inputs(self):
        """
        Désactiver tous les champs d'entrée et listes déroulantes.
        """
        self.object_input.setEnabled(False)
        self.radius_input.setEnabled(False)
        self.filter_combo.setEnabled(False)
        self.program_combo.setEnabled(False)
        self.celestial_combo.setEnabled(False)
        self.search_button.setEnabled(False)
        self.size_input.setEnabled(False)

    def enable_inputs(self):
        """
        Activer tous les champs d'entrée et listes déroulantes.
        """
        self.object_input.setEnabled(True)
        self.radius_input.setEnabled(True)
        self.filter_combo.setEnabled(True)
        self.program_combo.setEnabled(True)
        self.celestial_combo.setEnabled(True)
        self.search_button.setEnabled(True)
        self.size_input.setEnabled(True)

    def start_search(self):
        """
        Démarrer la recherche.
        """
        object_name = self.object_input.text()
        radius = self.radius_input.text()
        
        # Vérifier les champs
        if not object_name or not radius:
            self.missing_input_label.show()
            return
        self.missing_input_label.hide()
        
        self.search_button.setEnabled(False)
        
        radius = float(radius)

        # Démarrer l'animation
        self.animation_index = 0
        self.animation_timer.start(500)
        # Démarrer le thread de recherche
        self.search_thread = SearchThread(object_name, radius, self)
        self.search_thread.observations_ready.connect(self.on_observations_ready)
        self.search_thread.celestial_objects_ready.connect(self.on_celestial_objects_ready)
        self.search_thread.start()

    def update_search_button_text(self):
        """
        Mettre à jour le texte du bouton de recherche. Pour l'animation.
        """
        self.search_button.setText(self.animation_texts[self.animation_index])
        self.animation_index = (self.animation_index + 1) % len(self.animation_texts)

    def on_observations_ready(self):
        """
        Remettre à jour le texte de base et arrêter l'animation.
        """
        # Arrêter l'animation
        self.animation_timer.stop()
        self.search_button.setText("Rechercher")
        self.search_button.setEnabled(True)

    def on_celestial_objects_ready(self, celestial_objects):
        """
        Quand les objets célestes sont prêts.
        """
        self.celestial_objects = celestial_objects
        
        if self.celestial_objects:
            self.celestial_combo.clear()
            self.celestial_combo.addItems([self.message_celestial] + self.celestial_objects)
            self.celestial_label.show()
            self.celestial_combo.show()
            self.adjust_window_size()
        else:
            self.result_label.setText("Aucun objet céleste trouvé.")
            self.result_label.show()
            self.adjust_window_size()

    def populate_filter_combo(self, celestial_object):
        """
        Remplir la combobox des filtres en fonction de l'objet céleste sélectionné.
        """
        # Mettre les valeurs de base pour les autres comboboxes
        self.filter_combo.clear()
        self.program_combo.clear()
        
        self.filter_combo.setCurrentText(self.message_filter)
        self.program_combo.setCurrentText(self.message_program)

        if celestial_object == self.message_celestial:
            return

        self.observations,obs_2 = itertools.tee(self.observations, 2)

        self.observations_celestial = filter_by_celestial_object(obs_2, celestial_object)
        
        self.observations_celestial, obs2 = itertools.tee(self.observations_celestial, 2)

        filters = get_filters(obs2)

        if not filters:
            self.result_label.setText("Aucun filtre pour cet objet céleste.")
            self.result_label.show()
            self.adjust_window_size()
            return
        else:
            self.result_label.hide()
            
        filters = [self.message_filter] + filters
        self.filter_combo.clear()
        self.filter_combo.addItems(filters)
        self.filter_label.show()
        self.filter_combo.show()
        self.adjust_window_size()

    def populate_program_combo(self, filter_value):
        """
        Remplir la combobox des programmes en fonction du filtre sélectionné.
        """
        # Mettre les valeurs de base pour la combobox des programmes
        self.program_combo.clear()
        self.program_combo.setCurrentText(self.message_program)

        if filter_value == self.message_filter:
            return

        self.observations_celestial, obs2 = itertools.tee(self.observations_celestial, 2)

        self.observations_filter = filter_by_filter(obs2, filter_value)

        self.observations_filter, obs2 = itertools.tee(self.observations_filter, 2)

        programs = get_programs(obs2)

        if not programs:
            self.result_label.setText("Aucun programme pour ce filtre.")
            self.result_label.show()
            self.adjust_window_size()
            return
        else:
            self.result_label.hide()
            
        programs = [self.message_program] + programs
        self.program_combo.clear()
        self.program_combo.addItems(programs)
        self.program_label.show()
        self.program_combo.show()
        self.adjust_window_size()

    def manage_final_product(self, program):
        """
        Trouver le produit final et le télécharger s'il existe.
        """
        if program == self.message_program or program =="":
            return

        self.observations_filter, obs2 = itertools.tee(self.observations_filter, 2)

        self.observations_program = list(filter_by_program(obs2, program))
        
        # Mettre à jour ideal_Mo_size avec la valeur du widget
        self.ideal_Mo_size = self.size_input.value()

        self.final_product = get_final_product(self.observations_program, self.ideal_Mo_size)
        
        if self.final_product is not None:
            
            self.result_label.setText("Fichier FITS trouvé, téléchargement en cours")
            self.result_label.show()
            self.adjust_window_size()

            # Démarrer l'animation
            self.result_label_index = 0
            self.result_label_timer.start(500)

            # Démarrer le thread de téléchargement
            self.download_thread = DownloadThread(self.final_product, self.output_directory, self)
            self.download_thread.download_complete.connect(self.on_download_complete)
            self.download_thread.start()
        else:
            self.result_label.setText("Aucun produit trouvé.")
            self.result_label.show()
            self.adjust_window_size()

    def update_result_label_text(self):
        """
        Mettre à jour le texte du label de résultat.
        """
        self.result_label.setText(self.result_label_texts[self.result_label_index])
        self.result_label_index = (self.result_label_index + 1) % len(self.result_label_texts)

    def on_download_complete(self, manifest):
        """
        Quand le téléchargement est terminé.
        """
        # Arrêter l'animation
        self.result_label_timer.stop()

        # Vérifie qu'il n'y a pas eu d'erreur
        if manifest["Status"][0] == "COMPLETE":
            self.result_label.setText("Fichier téléchargé avec succès.")
        else:
            self.result_label.setText("Erreur lors du téléchargement. Essayer un autre produit.")
        self.adjust_window_size()

        # Mettre à jour le header du fichier FITS avec le filtre
        current_filter = self.filter_combo.currentText()
        dl_path = manifest["Local Path"][0]
        with fits.open(dl_path, mode="update") as fits_file:
            fits_file[0].header["FILTER"] = current_filter
            fits_file.flush()


        # Réactiver les entrées après le téléchargement
        self.enable_inputs()

    def adjust_window_size(self):
        """
        Ajuster la taille de la fenêtre.
        """
        new_value = self.current_height + self.value_to_add
        if new_value > self.maxsize:
            new_value = self.maxsize
        else:
            self.current_height += new_value
        self.setMinimumSize(QSize(500, self.current_height))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())