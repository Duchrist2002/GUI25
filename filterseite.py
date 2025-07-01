import sys
import os
from PyQt5.QtGui import QPixmap, QFont, QIcon
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QComboBox,
    QSpinBox, QPushButton, QGroupBox, QTableWidget, QTableWidgetItem,
    QAbstractItemView, QScrollArea, QGridLayout, QFrame
)
from PyQt5.QtCore import Qt, QSize

from backend.filters import get_filtered_cruises

ASSETS_PATH = "assets/stadtbilder"  #chemin d acces pour les photos

class CityGallery(QWidget):
    def __init__(self, city_list, callback):
        super().__init__()
        self.selected = set()
        self.callback = callback

        grid_widget = QWidget()
        grid = QGridLayout(grid_widget)
        grid.setSpacing(12)
        row, col = 0, 0

        for idx, city in enumerate(city_list):
            img_path = os.path.join(ASSETS_PATH, f"{city}.jpg")
            if not os.path.exists(img_path):
                img_path = "assets/placeholder.jpg"  # Une image de secours

            btn = QPushButton()
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
        self.callback()

class ShipGallery(QWidget):
    def __init__(self, shiptypes, callback):
        super().__init__()
        self.selected = set()
        self.callback = callback

        grid_widget = QWidget()
        grid = QGridLayout(grid_widget)
        grid.setSpacing(12)
        row, col = 0, 0

        ASSETS_SHIP = "assets/schiffbilder"
        for idx, schiff in enumerate(shiptypes):
            img_path = os.path.join(ASSETS_SHIP, f"{schiff}.jpg")
            if not os.path.exists(img_path):
                img_path = "assets/placeholder.jpg"

            btn = QPushButton()
            btn.setIcon(QIcon(QPixmap(img_path)))
            btn.setIconSize(QSize(110, 80))
            btn.setFixedSize(120, 100)
            btn.setCheckable(True)
            btn.setToolTip(schiff)
            btn.setStyleSheet("""
                QPushButton { border: 2px solid transparent; border-radius: 12px; }
                QPushButton:checked { border: 2px solid #0078D7; background: #e6f2ff; }
            """)
            btn.clicked.connect(lambda checked, s=schiff: self.on_ship_click(s, checked))

            lbl = QLabel(schiff)
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setFont(QFont("Arial", 9))
            ship_widget = QFrame()
            ship_layout = QVBoxLayout(ship_widget)
            ship_layout.addWidget(btn)
            ship_layout.addWidget(lbl)
            ship_layout.setContentsMargins(0, 0, 0, 0)
            ship_layout.setSpacing(2)

            grid.addWidget(ship_widget, row, col)
            col += 1
            if col >= 5:
                col = 0
                row += 1

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(grid_widget)
        scroll.setFixedHeight(160)

        layout = QVBoxLayout(self)
        layout.addWidget(scroll)

    def on_ship_click(self, schiff, checked):
        if checked:
            self.selected.add(schiff)
        else:
            self.selected.discard(schiff)
        self.callback()

class MainWindow(QWidget):
    def __init__(self, preset_meerart=None):
        super().__init__()
        self.setWindowTitle("Schiffsreisen Auswahl – Mockup")
        self.setMinimumSize(950, 650)
        self.init_ui(preset_meerart)

    def init_ui(self, preset_meerart):
        self.user_label = QLabel("👤 Benutzer: Max Mustermann | Dummy_Kapital: 1850 €")
        self.user_label.setStyleSheet("font-size:16px; font-weight:bold; padding:8px;")

        filter_box = QGroupBox("🔎 Filter")
        filter_layout = QHBoxLayout()

        self.meerart_cb = QComboBox()
        self.meerart_cb.addItems(["(Alle)", "Ostsee", "Nordsee", "Mittelmeer", "Nordpolarmeer", "Nordpolarmeer (Spezial)"])
        if preset_meerart:
            index = self.meerart_cb.findText(preset_meerart, Qt.MatchFixedString)
            if index >= 0:
                self.meerart_cb.setCurrentIndex(index)

        self.meerart_cb.currentTextChanged.connect(self.update_table)

        self.naechte_sb = QSpinBox()
        self.naechte_sb.setMinimum(1)
        self.naechte_sb.setMaximum(30)
        self.naechte_sb.setValue(7)
        self.naechte_sb.valueChanged.connect(self.update_table)

        filter_layout.addWidget(QLabel("Meerart:"))
        filter_layout.addWidget(self.meerart_cb)
        filter_layout.addWidget(QLabel("Nächte:"))
        filter_layout.addWidget(self.naechte_sb)
        filter_box.setLayout(filter_layout)

        city_list = ["Aberdeen", "Alexandria", "Algier", "Amsterdam", "Antwerpen", "Athen", "Barcelona", "Bari",
            "Belfast", "Bergen", "Cagliari", "Catania", "Danzig", "Den Haag", "Dublin", "Edinburgh",
            "Galway", "Genua", "Gibraltar", "Göteborg", "Hamburg", "Hammerfest", "Haugesund", "Helsinki",
            "Heraklion", "Izmir", "Kaliningrad", "Kleipada", "Kopenhagen", "Kristiansand", "London",
            "Longyearbyen", "Malaga", "Marseille", "Neapel", "Nizza", "Nuuk", "Oulu", "Palermo",
            "Palma de Mallorca", "Reykjavik", "Rhodos", "Riga", "Rostock", "Sankt_Petersburg", "Split",
            "Stavanger", "Stockholm", "Stralsund", "Swinemünde", "Tallin", "Tanger", "Thule", "Torshavn",
            "Tromsö", "Trondheim", "Tunis", "Valencia", "Valetta", "Venedig", "Visby", "Ystad"]

        self.city_gallery = CityGallery(city_list, self.update_table)

        shiptypes = ["Schiffstyp A", "Schiffstyp B", "Schiffstyp C", "Schiffstyp D", "Schiffstyp E", "Schiffstyp F", "Schiffstyp G", "Schiffstyp H", "Schiffstyp I", "Schiffstyp X"]
        self.ship_gallery = ShipGallery(shiptypes, self.update_table)

        self.results_table = QTableWidget(0, 5)
        self.results_table.setHorizontalHeaderLabels(["Nr.", "Meerart", "Nächte", "Städte", "Schiffstyp"])
        self.results_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.results_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.results_table.setMinimumHeight(300)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.user_label)
        main_layout.addWidget(filter_box)
        main_layout.addWidget(QLabel("Wähle besuchte Städte:"))
        main_layout.addWidget(self.city_gallery)
        main_layout.addWidget(QLabel("Wähle Schiffstyp:"))
        main_layout.addWidget(self.ship_gallery)
        main_layout.addWidget(QLabel("🚢 Verfügbare Reisen:"))
        main_layout.addWidget(self.results_table)
        self.setLayout(main_layout)

        self.update_table()

    def update_table(self):
        filters = {
            "meerart": self.meerart_cb.currentText() if self.meerart_cb.currentText() != "(Alle)" else None,
            "naechte": self.naechte_sb.value(),
            "staedte": list(self.city_gallery.selected),
            "schiffstyp": list(self.ship_gallery.selected)[0] if self.ship_gallery.selected else None
        }
        reisen = get_filtered_cruises(filters)
        self.results_table.setRowCount(len(reisen))
        for row, r in enumerate(reisen):
            self.results_table.setItem(row, 0, QTableWidgetItem(str(r["Reisenummer"])))
            self.results_table.setItem(row, 1, QTableWidgetItem(str(r["Meerart"])))
            self.results_table.setItem(row, 2, QTableWidgetItem(str(r["Übernachtungen"])))
            self.results_table.setItem(row, 3, QTableWidgetItem(", ".join(r["besuchte Städte"])))
            self.results_table.setItem(row, 4, QTableWidgetItem(str(r["Schiffstyp"])))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
