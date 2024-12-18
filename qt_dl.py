import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QLineEdit
from PyQt6.QtCore import QSize, QThread, pyqtSignal, QTimer
from download_file import *

"""
TODO
- Lancer dans un thread le download et annimer
- Ajouter un logo
"""

class SearchThread(QThread):
    observations_ready = pyqtSignal(object)

    def __init__(self, objet, rayon):
        super().__init__()
        self.objet = objet
        self.rayon = rayon

    def run(self):
        observations = obtenir_observations(self.objet, self.rayon)
        self.observations_ready.emit(observations)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Downloader App")
        self.setMinimumSize(QSize(500, 50))
        
        self.value_to_add = 70
        self.current_height = self.value_to_add
        self.maxsize = 500

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Champs de saisie pour l'objet et le rayon
        self.layout.addWidget(QLabel("Entrez le nom de l'objet (ex: M31):"))
        self.objet_input = QLineEdit()
        self.layout.addWidget(self.objet_input)

        self.layout.addWidget(QLabel("Entrez le rayon de recherche en degrés (ex: 0.1):"))
        self.rayon_input = QLineEdit()
        self.layout.addWidget(self.rayon_input)

        # Bouton pour lancer la recherche
        self.search_button = QPushButton("Rechercher")
        self.search_button.clicked.connect(self.start_search)
        self.layout.addWidget(self.search_button)
        
        # Labels si les QLineEdit sont vides
        self.missing_input_label = QLabel("Veuillez remplir les champs ci-dessus.")
        self.layout.addWidget(self.missing_input_label)
        self.missing_input_label.hide()

        # Créer tous les widgets au début, mais les masquer
        self.mission_label = QLabel("Sélectionner une mission:")
        self.layout.addWidget(self.mission_label)
        self.mission_label.hide()

        self.mission_combo = QComboBox()
        self.mission_combo.currentTextChanged.connect(self.select_mission)
        self.layout.addWidget(self.mission_combo)
        self.mission_combo.hide()

        self.program_label = QLabel("Sélectionner un programme:")
        self.layout.addWidget(self.program_label)
        self.program_label.hide()

        self.program_combo = QComboBox()
        self.program_combo.currentTextChanged.connect(self.select_program)
        self.layout.addWidget(self.program_combo)
        self.program_combo.hide()

        self.celestial_label = QLabel("Sélectionner un objet céleste:")
        self.layout.addWidget(self.celestial_label)
        self.celestial_label.hide()

        self.celestial_combo = QComboBox()
        self.celestial_combo.currentTextChanged.connect(self.select_celestial_object)
        self.layout.addWidget(self.celestial_combo)
        self.celestial_combo.hide()
        
        self.result_label = QLabel("")
        self.layout.addWidget(self.result_label)
        self.result_label.hide()

        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.update_search_button_text)
        self.animation_texts = ["Recherche en cours", "Recherche en cours .", "Recherche en cours ..", "Recherche en cours ..."]
        self.animation_index = 0

        self.adjust_window_size()

    def start_search(self):
        objet = self.objet_input.text()
        rayon = self.rayon_input.text()
        
        # verification des champs
        if not objet or not rayon:
            self.missing_input_label.show()
            return
        self.missing_input_label.hide()
        
        rayon = float(rayon)

        # Start the animation
        self.animation_index = 0
        self.animation_timer.start(500)
        # Start the thread
        self.search_thread = SearchThread(objet, rayon)
        self.search_thread.observations_ready.connect(self.on_observations_ready)
        self.search_thread.start()

    def update_search_button_text(self):
        self.search_button.setText(self.animation_texts[self.animation_index])
        self.animation_index = (self.animation_index + 1) % len(self.animation_texts)

    def on_observations_ready(self, observations):
        # Stop the animation
        self.animation_timer.stop()
        self.search_button.setText("Rechercher")
        self.observations = observations
        if self.observations is None:
            
            return

        self.missions = obtenir_missions(self.observations)
        if self.missions:
            self.mission_combo.clear()
            self.mission_combo.addItems(self.missions)
            self.mission_label.show()
            self.mission_combo.show()
            self.adjust_window_size()

    def select_mission(self, mission):
        self.observations_mission = filtrer_par_mission(self.observations, mission)
        if self.observations_mission is None:
            return

        self.programmes = obtenir_programmes(self.observations_mission)
        if self.programmes:
            self.program_combo.clear()
            programme_items = ["Sélectionner un programme"] + [str(programme) for programme in self.programmes]
            self.program_combo.addItems(programme_items)
            self.program_label.show()
            self.program_combo.show()
            self.adjust_window_size()

    def select_program(self, programme):
        if programme == "Sélectionner un programme":
            return

        self.observations_programme = filtrer_par_programme(self.observations_mission, programme)
        if self.observations_programme is None:
            return

        self.objets_celestes = obtenir_objets_celestes(self.observations_programme)
        if self.objets_celestes:
            self.celestial_combo.clear()
            self.celestial_combo.addItems(self.objets_celestes)
            self.celestial_label.show()
            self.celestial_combo.show()
            self.adjust_window_size()

    def select_celestial_object(self, objet_celeste):
        self.observations_objet = filtrer_par_objet_celeste(self.observations_programme, objet_celeste)
        if self.observations_objet is None:
            return

        self.produit_final = obtenir_produit_final(self.observations_objet)
        if self.produit_final is not None:
            self.result_label.setText("Fichier FITS trouvé, téléchargement en cours...")
            self.adjust_window_size()
            # Télécharger le produit
            output_dir = "downloads"
            telecharger_observations(self.produit_final, output_dir)
            self.result_label.setText("Fichier téléchargé avec succès.")
            self.adjust_window_size()
        else:
            self.result_label.setText("Aucune observation trouvée.")
        self.result_label.show()

    def adjust_window_size(self):
        new_value = self.current_height + self.value_to_add
        if new_value > self.maxsize:
            new_value = self.maxsize
        else :
            self.current_height += new_value
        self.setMinimumSize(QSize(500, self.current_height))

if __name__ == "__main__":
    # Lancement de l'application Qt
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())