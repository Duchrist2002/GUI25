import sys
import os
from PyQt5.QtGui import QPixmap, QFont, QIcon
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QComboBox,
    QSpinBox, QPushButton, QGroupBox, QTableWidget, QTableWidgetItem,
    QAbstractItemView, QScrollArea, QGridLayout, QFrame, QMessageBox, QStackedWidget, QLineEdit
)
from PyQt5.QtCore import Qt, QSize

from backend.filters import get_filtered_cruises

ASSETS_PATH = "assets/stadtbilder"

# ========================================
# Classe pour la galerie des villes
# ========================================
class CityGallery(QWidget):
    def __init__(self, city_list, callback):
        super().__init__()
        self.selected = set()
        self.callback = callback
        grid_widget = QWidget()
        grid = QGridLayout(grid_widget)
        grid.setSpacing(12)
        row, col = 0, 0

        for city in city_list:
            img_path = os.path.join(ASSETS_PATH, f"{city}.jpg")
            if not os.path.exists(img_path):
                img_path = "assets/placeholder.jpg"
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

# ========================================
# Classe pour la galerie des navires
# ========================================
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
        for schiff in shiptypes:
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

# ========================================
# Page des filtres et du tableau
# ========================================
class FilterPage(QWidget):
    def __init__(self, switch_to_summary):
        super().__init__()
        self.switch_to_summary = switch_to_summary
        self.selected_cruise = None
        self.user_label = QLabel("👤 Benutzer: Max Mustermann | Dummy_Kapital: 1850 €")
        self.user_label.setStyleSheet("font-size:16px; font-weight:bold; padding:8px;")

        # Filtres haut
        filter_box = QGroupBox("🔎 Filter")
        filter_layout = QHBoxLayout()
        self.meerart_cb = QComboBox()
        self.meerart_cb.addItems(["(Alle)", "Ostsee", "Nordsee", "Mittelmeer", "Nordpolarmeer", "Nordpolarmeer (Spezial)"])
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

        # Galeries
        city_list = ["Aberdeen", "Alexandria", "Algier", "Amsterdam", "Antwerpen", "Athen", "Barcelona", "Bari",
                     "Belfast", "Bergen", "Cagliari", "Catania", "Danzig", "Den Haag", "Dublin", "Edinburgh",
                     "Galway", "Genua", "Gibraltar", "Göteborg", "Hamburg", "Hammerfest", "Haugesund", "Helsinki",
                     "Heraklion", "Izmir", "Kaliningrad", "Kleipada", "Kopenhagen", "Kristiansand", "London",
                     "Longyearbyen", "Malaga", "Marseille", "Neapel", "Nizza", "Nuuk", "Oulu", "Palermo",
                     "Palma de Mallorca", "Reykjavik", "Rhodos", "Riga", "Rostock", "Sankt_Petersburg", "Split",
                     "Stavanger", "Stockholm", "Stralsund", "Swinemünde", "Tallin", "Tanger", "Thule", "Torshavn",
                     "Tromsö", "Trondheim", "Tunis", "Valencia", "Valetta", "Venedig", "Visby", "Ystad"]
        self.city_gallery = CityGallery(city_list, self.update_table)
        shiptypes = ["Schiffstyp A", "Schiffstyp B", "Schiffstyp C", "Schiffstyp D", "Schiffstyp E", "Schiffstyp F",
                     "Schiffstyp G", "Schiffstyp H", "Schiffstyp I", "Schiffstyp X"]
        self.ship_gallery = ShipGallery(shiptypes, self.update_table)

        # Tableau
        self.results_table = QTableWidget(0, 5)
        self.results_table.setHorizontalHeaderLabels(["Nr.", "Meerart", "Nächte", "Städte", "Schiffstyp"])
        self.results_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.results_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.results_table.setMinimumHeight(300)
        self.results_table.itemSelectionChanged.connect(self.store_selected_cruise)

        # Navigation
        self.next_btn = QPushButton("Weiter ➔")
        self.next_btn.clicked.connect(self.go_to_summary)
        self.prev_btn = QPushButton("← Précédent")
        nav_layout = QHBoxLayout()
        nav_layout.addWidget(self.prev_btn)
        nav_layout.addWidget(self.next_btn)

        # Layout général
        layout = QVBoxLayout()
        layout.addWidget(self.user_label)
        layout.addWidget(filter_box)
        layout.addWidget(QLabel("Wähle besuchte Städte:"))
        layout.addWidget(self.city_gallery)
        layout.addWidget(QLabel("Wähle Schiffstyp:"))
        layout.addWidget(self.ship_gallery)
        layout.addWidget(QLabel("🚢 Verfügbare Reisen:"))
        layout.addWidget(self.results_table)
        layout.addLayout(nav_layout)
        self.setLayout(layout)
        self.update_table()

    def store_selected_cruise(self):
        selected_row = self.results_table.currentRow()
        if selected_row >= 0:
            self.selected_cruise = {
                "Reisenummer": self.results_table.item(selected_row, 0).text(),
                "Meerart": self.results_table.item(selected_row, 1).text(),
                "Übernachtungen": self.results_table.item(selected_row, 2).text(),
                "besuchte Städte": self.results_table.item(selected_row, 3).text(),
                "Schiffstyp": self.results_table.item(selected_row, 4).text()
            }

    def go_to_summary(self):
        if not self.selected_cruise:
            QMessageBox.warning(self, "Fehler", "Bitte wähle d'abord une Reise!")
            return
        self.switch_to_summary(self.selected_cruise)

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

class SummaryPage(QWidget):
    def __init__(self, cruise, switch_to_filter, switch_to_payment):
        super().__init__()
        self.cruise = cruise
        self.switch_to_filter = switch_to_filter
        self.switch_to_payment = switch_to_payment

        # Titre en haut
        title = QLabel(f"Résumé du voyage n°{cruise['Reisenummer']}")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size:22px; font-weight:bold; padding:10px;")

        # Galerie scrollable
        scroll_widget = QWidget()
        grid = QGridLayout(scroll_widget)
        grid.setSpacing(12)

        # Photos des villes
        villes = [v.strip() for v in cruise["besuchte Städte"].split(",")]
        for idx, ville in enumerate(villes):
            img_path = os.path.join("assets/stadtbilder", f"{ville}.jpg")
            if not os.path.exists(img_path):
                img_path = "assets/placeholder.jpg"
            lbl_img = QLabel()
            pixmap = QPixmap(img_path).scaled(160, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            lbl_img.setPixmap(pixmap)
            lbl_img.setAlignment(Qt.AlignCenter)
            lbl_caption = QLabel(ville)
            lbl_caption.setAlignment(Qt.AlignCenter)
            vbox = QVBoxLayout()
            vbox.addWidget(lbl_img)
            vbox.addWidget(lbl_caption)
            frame = QFrame()
            frame.setLayout(vbox)
            grid.addWidget(frame, idx//4, idx%4)

        # Photo du navire
        ship_img_path = os.path.join("assets/schiffbilder", f"{cruise['Schiffstyp']}.jpg")
        if not os.path.exists(ship_img_path):
            ship_img_path = "assets/placeholder.jpg"
        ship_img_label = QLabel()
        ship_pixmap = QPixmap(ship_img_path).scaled(300, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        ship_img_label.setPixmap(ship_pixmap)
        ship_img_label.setAlignment(Qt.AlignCenter)
        grid.addWidget(ship_img_label, (len(villes)+4)//4, 0, 1, 4)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(scroll_widget)
        scroll_area.setFixedHeight(300)

        # Infos générales
        info_group = QGroupBox("Détails du voyage")
        info_layout = QVBoxLayout()
        info_layout.addWidget(QLabel(f"🌊 <b>Mer :</b> {cruise['Meerart']}"))
        info_layout.addWidget(QLabel(f"🛏️ <b>Nombre de nuits :</b> {cruise['Übernachtungen']}"))
        info_layout.addWidget(QLabel(f"🏙️ <b>Villes visitées :</b> {cruise['besuchte Städte']}"))
        info_layout.addWidget(QLabel(f"🚢 <b>Type de navire :</b> {cruise['Schiffstyp']}"))
        info_group.setLayout(info_layout)

        # Navigation bas
        nav_layout = QHBoxLayout()
        back_btn = QPushButton("← Retour aux filtres")
        back_btn.clicked.connect(self.switch_to_filter)
        next_btn = QPushButton("Continuer vers paiement →")
        next_btn.clicked.connect(self.switch_to_payment)
        nav_layout.addWidget(back_btn)
        nav_layout.addWidget(next_btn)

        # Layout global
        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addWidget(scroll_area)
        layout.addWidget(info_group)
        layout.addLayout(nav_layout)
        self.setLayout(layout)


class PaymentPage(QWidget):
    def __init__(self, switch_to_summary):
        super().__init__()
        self.switch_to_summary = switch_to_summary

        # Titre
        title = QLabel("💳 Paiement du voyage")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size:22px; font-weight:bold; padding:10px;")

        # Formulaire
        form_group = QGroupBox("Informations bancaires")
        form_layout = QVBoxLayout()
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nom du titulaire")
        self.card_input = QLineEdit()
        self.card_input.setPlaceholderText("Numéro de carte (XXXX XXXX XXXX XXXX)")
        self.exp_input = QLineEdit()
        self.exp_input.setPlaceholderText("Date d'expiration (MM/AA)")
        self.cvv_input = QLineEdit()
        self.cvv_input.setPlaceholderText("CVV")
        self.cvv_input.setEchoMode(QLineEdit.Password)
        for widget in [self.name_input, self.card_input, self.exp_input, self.cvv_input]:
            widget.setMinimumHeight(30)
            form_layout.addWidget(widget)
        form_group.setLayout(form_layout)

        # Navigation bas
        nav_layout = QHBoxLayout()
        back_btn = QPushButton("← Retour au résumé")
        back_btn.clicked.connect(self.switch_to_summary)
        pay_btn = QPushButton("Payer maintenant ✅")
        pay_btn.clicked.connect(self.validate_payment)
        nav_layout.addWidget(back_btn)
        nav_layout.addWidget(pay_btn)

        # Layout global
        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addWidget(form_group)
        layout.addLayout(nav_layout)
        self.setLayout(layout)

    def validate_payment(self):
        if not all([self.name_input.text(), self.card_input.text(), self.exp_input.text(), self.cvv_input.text()]):
            QMessageBox.warning(self, "Erreur", "Merci de remplir tous les champs.")
            return
        QMessageBox.information(self, "Paiement", "✅ Votre paiement a été effectué ! Merci pour votre confiance.")


class MainStackedApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Seavia Holiday – Application complète")
        self.setMinimumSize(950, 650)

        # Gestion des pages
        self.stack = QStackedWidget()
        self.filter_page = FilterPage(self.show_summary)
        self.stack.addWidget(self.filter_page)

        layout = QVBoxLayout()
        layout.addWidget(self.stack)
        self.setLayout(layout)

    def show_summary(self, cruise):
        # Crée et affiche la page résumé
        self.summary_page = SummaryPage(cruise, self.show_filter, self.show_payment)
        self.stack.addWidget(self.summary_page)
        self.stack.setCurrentWidget(self.summary_page)

    def show_filter(self):
        self.stack.setCurrentWidget(self.filter_page)

    def show_payment(self):
        # Crée et affiche la page paiement
        self.payment_page = PaymentPage(self.show_summary_back)
        self.stack.addWidget(self.payment_page)
        self.stack.setCurrentWidget(self.payment_page)

    def show_summary_back(self):
        self.stack.setCurrentWidget(self.summary_page)

    def select_meerart_and_open(self, meerart):
        """Sélectionne la mer et ouvre la page filtre."""
        self.filter_page.meerart_cb.setCurrentText(meerart)
        self.stack.setCurrentWidget(self.filter_page)


# ========================================
# Lancement de l'application
# ========================================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainStackedApp()
    window.show()
    sys.exit(app.exec_())
