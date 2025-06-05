import sys
import os
from PyQt5.QtGui import QPixmap, QFont, QIcon
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QComboBox,
    QSpinBox, QPushButton, QGroupBox, QTableWidget, QTableWidgetItem,
    QAbstractItemView, QScrollArea, QGridLayout, QFrame
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QFont

ASSETS_PATH = "assets/stadtbilder"  # À adapter selon ton projet

class CityGallery(QWidget):
    def __init__(self, city_list):
        super().__init__()
        self.selected = set()
        grid_widget = QWidget()
        grid = QGridLayout(grid_widget)
        grid.setSpacing(12)
        row, col = 0, 0

        for idx, city in enumerate(city_list):
            img_path = os.path.join(ASSETS_PATH, f"{city}.jpg")
            if not os.path.exists(img_path):
                img_path = "assets/placeholder.jpg"  # Une image de secours

            btn = QPushButton()
            from PyQt5.QtGui import QIcon
            btn.setIcon(QIcon(QPixmap(img_path)))
            btn.setIconSize(QSize(110, 80))
            btn.setFixedSize(120, 100)
            btn.setCheckable(True)
            btn.setToolTip(city)
            btn.setStyleSheet("""
                QPushButton { border: 2px solid transparent; border-radius: 12px; }
                QPushButton:checked { border: 2px solid #0078D7; background: #e6f2ff; }
            """)
            btn.clicked.connect(lambda checked, c=city: self.on_city_click(c, checked))

            lbl = QLabel(city)
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setFont(QFont("Arial", 9))
            city_widget = QFrame()
            city_layout = QVBoxLayout(city_widget)
            city_layout.addWidget(btn)
            city_layout.addWidget(lbl)
            city_layout.setContentsMargins(0,0,0,0)
            city_layout.setSpacing(2)

            grid.addWidget(city_widget, row, col)
            col += 1
            if col >= 4:
                col = 0
                row += 1

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(grid_widget)
        scroll.setFixedHeight(230)

        layout = QVBoxLayout(self)
        layout.addWidget(scroll)

    def on_city_click(self, city, checked):
        if checked:
            self.selected.add(city)
        else:
            self.selected.discard(city)
        print("Villes sélectionnées:", self.selected)  # À connecter à ta logique de filtre

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Schiffsreisen Auswahl – Mockup")
        self.setMinimumSize(950, 650)
        self.init_ui()

    def init_ui(self):
        self.user_label = QLabel("👤 Benutzer: Max Mustermann | Kapital: 1850 €")
        self.user_label.setStyleSheet("font-size:16px; font-weight:bold; padding:8px;")

        # --- FILTERS ZONE ---
        filter_box = QGroupBox("🔎 Filter")
        filter_layout = QHBoxLayout()

        # Meerart
        self.meerart_cb = QComboBox()
        self.meerart_cb.addItems(["(Alle)", "Ostsee", "Nordsee", "Mittelmeer", "Nordpolarmeer", "Nordpolarmeer (Spezial)"])
        filter_layout.addWidget(QLabel("Meerart:"))
        filter_layout.addWidget(self.meerart_cb)

        # Anzahl Nächte
        self.naechte_sb = QSpinBox()
        self.naechte_sb.setMinimum(1)
        self.naechte_sb.setMaximum(30)
        self.naechte_sb.setValue(7)
        filter_layout.addWidget(QLabel("Nächte:"))
        filter_layout.addWidget(self.naechte_sb)

        # Schiffstyp
        self.schiff_cb = QComboBox()
        self.schiff_cb.addItems(["(Alle)", "A", "B", "C", "D", "E", "F", "G", "H", "I", "X"])
        filter_layout.addWidget(QLabel("Schiffstyp:"))
        filter_layout.addWidget(self.schiff_cb)

        filter_box.setLayout(filter_layout)

        # --- CITY GALLERY ZONE ---
        city_list = ["Stockholm", "Helsinki", "Kopenhagen", "Tallinn", "Riga", "Hamburg", "Oslo", "Amsterdam"]
        self.city_gallery = CityGallery(city_list)

        # --- RESULTS ZONE ---
        self.results_table = QTableWidget(6, 5)
        self.results_table.setHorizontalHeaderLabels(["Nr.", "Meerart", "Nächte", "Städte", "Schiffstyp"])
        self.results_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.results_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.results_table.setMinimumHeight(300)
        self.fill_results_mock()

        # --- LAYOUT ROOT ---
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.user_label)
        main_layout.addWidget(filter_box)
        main_layout.addWidget(QLabel("Wähle besuchte Städte:"))
        main_layout.addWidget(self.city_gallery)
        main_layout.addWidget(QLabel("🚢 Verfügbare Reisen:"))
        main_layout.addWidget(self.results_table)
        self.setLayout(main_layout)

    def fill_results_mock(self):
        reisen = [
            ["001", "Ostsee", "7", "Stockholm, Helsinki", "A"],
            ["002", "Mittelmeer", "10", "Rom, Barcelona", "C"],
            ["003", "Nordsee", "5", "Hamburg, Amsterdam", "E"],
            ["004", "Nordpolarmeer", "14", "Spitzbergen", "X"],
            ["005", "Ostsee", "12", "Tallinn, Riga", "B"],
            ["006", "Mittelmeer", "8", "Athen, Malta", "D"],
        ]
        for row, r in enumerate(reisen):
            for col, v in enumerate(r):
                item = QTableWidgetItem(v)
                self.results_table.setItem(row, col, item)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
