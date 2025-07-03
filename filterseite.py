# -*- coding: utf-8 -*-
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
                QPushButton {
                    border: 2px solid #007ACC; 
                    border-radius: 12px;
                    background: white;
                }
                QPushButton:checked {
                    background: #e6f2ff;
                    border: 2px solid #e74c3c;
                }
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
        scroll.setStyleSheet("""
            QScrollArea {
                border: 2px solid #007ACC;
                border-radius: 12px;
                background: #ffffff;
            }
        """)

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
                QPushButton {
                    border: 2px solid #007ACC;
                    border-radius: 12px;
                    background: white;
                }
                QPushButton:checked {
                    background: #e6f2ff;
                    border: 2px solid #e74c3c;
                }
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
        scroll.setStyleSheet("""
            QScrollArea {
                border: 2px solid #007ACC;
                border-radius: 12px;
                background: #ffffff;
            }
        """)

        layout = QVBoxLayout(self)
        layout.addWidget(scroll)

    def on_ship_click(self, schiff, checked):
        if checked:
            self.selected.add(schiff)
        else:
            self.selected.discard(schiff)
        self.callback()


class FilterPage(QWidget):
    def __init__(self, switch_to_summary):
        super().__init__()
        self.switch_to_summary = switch_to_summary
        self.selected_cruise = None

        self.user_label = QLabel("👤 Benutzer: Max Mustermann | Kapital: 1850 €")
        self.user_label.setStyleSheet("""
            QLabel {
                font-size:16px; 
                font-weight:bold; 
                padding:8px;
                background: #007ACC; 
                color: white;
                border-radius: 8px;
            }
        """)

        # Filtres haut
        filter_box = QGroupBox(" 🔍 Filter")
        filter_box.setStyleSheet("""
            QGroupBox {
                border: 2px solid #007ACC;
                border-radius: 12px;
                padding: 8px;
                font-weight: bold;
                background: #ffffff;
            }
        """)
        filter_layout = QHBoxLayout()
        self.meerart_cb = QComboBox()
        self.meerart_cb.addItems(
            ["(Alle)", "Ostsee", "Nordsee", "Mittelmeer", "Nordpolarmeer", "Nordpolarmeer (Spezial)"])
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
        self.results_table.setStyleSheet("""
            QTableWidget {
                border: 2px solid #007ACC;
                border-radius: 12px;
                background: #ffffff;
            }
        """)
        self.results_table.itemSelectionChanged.connect(self.store_selected_cruise)

        # Navigation
        self.next_btn = QPushButton("Weiter ➔")
        self.next_btn.setStyleSheet("""
            QPushButton {
                background: #e74c3c;
                color: white;
                font-weight: bold;
                font-size: 16px;
                padding: 8px 16px;
                border: none;
                border-radius: 10px;
            }
            QPushButton:hover {
                background: #c0392b;
            }
        """)
        self.next_btn.clicked.connect(self.go_to_summary)

        self.prev_btn = QPushButton("← Précédent")
        self.prev_btn.setStyleSheet(self.next_btn.styleSheet())
        self.prev_btn.clicked.connect(self.back_to_home)

        nav_layout = QHBoxLayout()
        nav_layout.addWidget(self.prev_btn)
        nav_layout.addWidget(self.next_btn)

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
            QMessageBox.warning(self, "Fehler", "Bitte wähle zuerst eine Reise!")
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

    def back_to_home(self):
        self.close()
        from standard import Header
        self.new_home = Header()
        self.new_home.show()


class SummaryPage(QWidget):
    def __init__(self, cruise, switch_to_filter, switch_to_payment):
        super().__init__()
        self.cruise = cruise
        self.switch_to_filter = switch_to_filter
        self.switch_to_payment = switch_to_payment

        title = QLabel(f"Zusammenfassung der Reise n°{cruise['Reisenummer']}")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #007ACC;
                background: #f0f8ff;
                border-radius: 12px;
                padding: 12px;
            }
        """)

        scroll_widget = QWidget()
        grid = QGridLayout(scroll_widget)
        grid.setSpacing(12)

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
            frame.setStyleSheet("""
                QFrame {
                    border: 2px solid #007ACC;
                    border-radius: 10px;
                    background: white;
                }
            """)
            grid.addWidget(frame, idx // 4, idx % 4)

        ship_img_path = os.path.join("assets/schiffbilder", f"{cruise['Schiffstyp']}.jpg")
        if not os.path.exists(ship_img_path):
            ship_img_path = "assets/placeholder.jpg"
        ship_img_label = QLabel()
        ship_pixmap = QPixmap(ship_img_path).scaled(300, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        ship_img_label.setPixmap(ship_pixmap)
        ship_img_label.setAlignment(Qt.AlignCenter)
        grid.addWidget(ship_img_label, (len(villes) + 4) // 4, 0, 1, 4)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(scroll_widget)
        scroll_area.setFixedHeight(300)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: 2px solid #007ACC;
                border-radius: 12px;
                background: #ffffff;
            }
        """)

        info_group = QGroupBox("Détails du voyage")
        info_group.setStyleSheet("""
            QGroupBox {
                border: 2px solid #007ACC;
                border-radius: 12px;
                background: #ffffff;
                padding: 10px;
            }
        """)
        info_layout = QVBoxLayout()
        info_layout.addWidget(QLabel(f"🌊 <b>Mer :</b> {cruise['Meerart']}"))
        info_layout.addWidget(QLabel(f"🛏️ <b>Anzahl Nächte :</b> {cruise['Übernachtungen']}"))
        info_layout.addWidget(QLabel(f"🏙️ <b>besuchte Städte :</b> {cruise['besuchte Städte']}"))
        info_layout.addWidget(QLabel(f"🚢 <b>Schifftyp :</b> {cruise['Schiffstyp']}"))
        info_group.setLayout(info_layout)

        back_btn = QPushButton("← zurück zum Filter")
        next_btn = QPushButton("weiter zur Zahlung →")
        for btn in [back_btn, next_btn]:
            btn.setStyleSheet("""
                QPushButton {
                    background: #e74c3c;
                    color: white;
                    font-weight: bold;
                    font-size: 16px;
                    padding: 8px 16px;
                    border: none;
                    border-radius: 10px;
                }
                QPushButton:hover {
                    background: #c0392b;
                }
            """)
        back_btn.clicked.connect(self.switch_to_filter)
        next_btn.clicked.connect(self.switch_to_payment)

        nav_layout = QHBoxLayout()
        nav_layout.addWidget(back_btn)
        nav_layout.addWidget(next_btn)

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

        title = QLabel("💳 Zahung der Reise")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #007ACC;
                background: #f0f8ff;
                border-radius: 12px;
                padding: 12px;
            }
        """)

        form_group = QGroupBox("Bankdaten")
        form_group.setStyleSheet("""
            QGroupBox {
                border: 2px solid #007ACC;
                border-radius: 12px;
                background: #ffffff;
                padding: 10px;
            }
        """)
        form_layout = QVBoxLayout()
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Name des Eigentumers")
        self.card_input = QLineEdit()
        self.card_input.setPlaceholderText("Kartennummer (XXXX XXXX XXXX XXXX)")
        self.exp_input = QLineEdit()
        self.exp_input.setPlaceholderText("Ablaufdatum (MM/AA)")
        self.cvv_input = QLineEdit()
        self.cvv_input.setPlaceholderText("CVV")
        self.cvv_input.setEchoMode(QLineEdit.Password)
        for widget in [self.name_input, self.card_input, self.exp_input, self.cvv_input]:
            widget.setMinimumHeight(30)
            widget.setStyleSheet("""
                QLineEdit {
                    border: 2px solid #007ACC;
                    border-radius: 8px;
                    padding: 6px;
                    background: #f9f9f9;
                }
                QLineEdit:focus {
                    border-color: #e74c3c;
                    background: #ffffff;
                }
            """)
            form_layout.addWidget(widget)
        form_group.setLayout(form_layout)

        back_btn = QPushButton("← Zurück zum Fazit")
        pay_btn = QPushButton("Jetzt Zahlen✅")
        for btn in [back_btn, pay_btn]:
            btn.setStyleSheet("""
                QPushButton {
                    background: #e74c3c;
                    color: white;
                    font-weight: bold;
                    font-size: 16px;
                    padding: 8px 16px;
                    border: none;
                    border-radius: 10px;
                }
                QPushButton:hover {
                    background: #c0392b;
                }
            """)
        back_btn.clicked.connect(self.switch_to_summary)
        pay_btn.clicked.connect(self.validate_payment)

        nav_layout = QHBoxLayout()
        nav_layout.addWidget(back_btn)
        nav_layout.addWidget(pay_btn)

        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addWidget(form_group)
        layout.addLayout(nav_layout)
        self.setLayout(layout)

    def validate_payment(self):
        if not all([self.name_input.text(), self.card_input.text(), self.exp_input.text(), self.cvv_input.text()]):
            QMessageBox.warning(self, "Error", "Füllen Sie alle Felder aus.")
            return
        QMessageBox.information(self, "Paiement", "✅ Ihre Zahlung ist erfolgreich ! Danke fürs Vertrauen.")

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
        self.filter_page.meerart_cb.setCurrentText(meerart)
        self.stack.setCurrentWidget(self.filter_page)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainStackedApp()
    window.show()
    sys.exit(app.exec_())
