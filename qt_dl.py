import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QLineEdit
from PyQt6.QtCore import QSize, QThread, pyqtSignal, QTimer
from download_file import *
from PyQt6.QtGui import QIcon
import itertools

class SearchThread(QThread):
    """
    Thread pour la recherche d'observations.
    """
    observations_ready = pyqtSignal(object)

    def __init__(self, object_name, radius):
        super().__init__()
        self.object_name = object_name
        self.radius = radius

    def run(self):
        observations_generator = get_observations(self.object_name, self.radius)
        self.observations_ready.emit(observations_generator)

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
        self.ideal_Mo_size = 50
        
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Champs de saisie pour l'objet et le rayon
        self.layout.addWidget(QLabel("Entrez le nom de l'objet (ex: M31):"))
        self.object_input = QLineEdit()
        self.layout.addWidget(self.object_input)

        self.layout.addWidget(QLabel("Entrez le rayon de recherche en degrés (ex: 0.1):"))
        self.radius_input = QLineEdit()
        self.layout.addWidget(self.radius_input)

        # Bouton pour démarrer la recherche
        self.search_button = QPushButton("Rechercher")
        self.search_button.clicked.connect(self.start_search)
        self.layout.addWidget(self.search_button)
        
        # Label pour les champs manquants
        self.missing_input_label = QLabel("Veuillez remplir les champs ci-dessus.")
        self.layout.addWidget(self.missing_input_label)
        self.missing_input_label.hide()

        # Création de tous les widgets au début, mais les cacher

        self.mission_label = QLabel("Sélectionner une mission:")
        self.layout.addWidget(self.mission_label)
        self.mission_label.hide()

        self.mission_combo = QComboBox()
        self.mission_combo.currentTextChanged.connect(self.populate_mission_combo)
        self.layout.addWidget(self.mission_combo)
        self.mission_combo.hide()

        self.celestial_label = QLabel("Sélectionner un objet céleste:")
        self.layout.addWidget(self.celestial_label)
        self.celestial_label.hide()

        self.celestial_combo = QComboBox()
        self.celestial_combo.currentTextChanged.connect(self.populate_program_combo)
        self.layout.addWidget(self.celestial_combo)
        self.celestial_combo.hide()

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
        self.mission_combo.setEnabled(False)
        self.program_combo.setEnabled(False)
        self.celestial_combo.setEnabled(False)
        self.search_button.setEnabled(False)

    def enable_inputs(self):
        """
        Activer tous les champs d'entrée et listes déroulantes.
        """
        self.object_input.setEnabled(True)
        self.radius_input.setEnabled(True)
        self.mission_combo.setEnabled(True)
        self.program_combo.setEnabled(True)
        self.celestial_combo.setEnabled(True)
        self.search_button.setEnabled(True)

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
        
        radius = float(radius)

        # Démarrer l'animation
        self.animation_index = 0
        self.animation_timer.start(500)
        # Démarrer le thread de recherche
        self.search_thread = SearchThread(object_name, radius)
        self.search_thread.observations_ready.connect(self.on_observations_ready)
        self.search_thread.start()

    def update_search_button_text(self):
        """
        Mettre à jour le texte du bouton de recherche.
        """
        self.search_button.setText(self.animation_texts[self.animation_index])
        self.animation_index = (self.animation_index + 1) % len(self.animation_texts)

    def on_observations_ready(self, observations_generator):
        """
        Quand les observations sont prêtes.
        """
        # Arrêter l'animation
        self.animation_timer.stop()
        self.search_button.setText("Rechercher")
        # Dupliquer le générateur pour une utilisation multiple
        self.observations_generator, self.observations_generator_copy = itertools.tee(observations_generator)
        self.missions = ["Sélectionner une mission"] + list(get_missions(self.observations_generator))
        if self.missions:
            self.mission_combo.clear()
            self.mission_combo.addItems(self.missions)
            self.mission_label.show()
            self.mission_combo.show()
            self.adjust_window_size()

    def populate_mission_combo(self, mission):
        """
        Remplir la combobox des objets célestes en fonction de la mission sélectionnée.
        """
        if mission == "Sélectionner une mission":
            return

        # Utiliser une copie du générateur pour filtrer par mission
        self.observations_generator_copy, observations_mission_gen = itertools.tee(self.observations_generator_copy)
        self.observations_mission_list = list(filter_by_mission(observations_mission_gen, mission))
        if not self.observations_mission_list:
            self.result_label.setText("Aucune observation pour cette mission.")
            self.result_label.show()
            self.adjust_window_size()
            return

        celestial_objects = ["Sélectionner un objet céleste"] + list(get_celestial_objects(self.observations_mission_list))
        if celestial_objects:
            self.celestial_combo.clear()
            self.celestial_combo.addItems(celestial_objects)
            self.celestial_label.show()
            self.celestial_combo.show()
            self.adjust_window_size()

    def populate_program_combo(self, celestial_object):
        """
        Remplir la combobox des programmes en fonction de l'objet céleste sélectionné.
        """
        if celestial_object == "Sélectionner un objet céleste":
            return
        
        observations_object_gen = filter_by_celestial_object(self.observations_mission_list, celestial_object)
        self.observations_object_list = list(observations_object_gen)
        if not self.observations_object_list:
            self.result_label.setText("Aucune observation trouvée.")
            self.result_label.show()
            self.adjust_window_size()
            return

        programs = ["Sélectionner un programme"] + list(get_programs(self.observations_object_list))
        if programs:
            self.program_combo.clear()
            self.program_combo.addItems(programs)
            self.program_label.show()
            self.program_combo.show()
            self.adjust_window_size()
            
    def manage_final_product(self, program):
        """
        Trouver le produit final et le télécharger s'il existe.
        """
        if program == "Sélectionner un programme":
            return

        observations_program_gen = filter_by_program(self.observations_object_list, program)
        self.observations_program_list = list(observations_program_gen)
        if not self.observations_program_list:
            return

        self.final_product = get_final_product(self.observations_program_list, self.ideal_Mo_size)
        if self.final_product is not None:
            self.result_label.setText("Fichier FITS trouvé, téléchargement en cours")
            self.result_label.show()
            self.adjust_window_size()

            # Démarrer l'animation
            self.result_label_index = 0
            self.result_label_timer.start(1000)

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