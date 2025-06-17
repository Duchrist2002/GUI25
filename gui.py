import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QComboBox,
    QListWidget, QPushButton, QLineEdit
)

from backend.filters import get_filtered_cruises

class CruiseFilterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Filtrer les croisières")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.meerart_label = QLabel("Mer :")
        self.meerart_combo = QComboBox()
        self.meerart_combo.addItems(["", "Ostsee", "Nordsee"])

        self.naechte_label = QLabel("Nombre de nuits :")
        self.naechte_input = QLineEdit()

        self.staedte_label = QLabel("Villes (séparées par virgule) :")
        self.staedte_input = QLineEdit()

        self.schiffstyp_label = QLabel("Type de bateau :")
        self.schiffstyp_combo = QComboBox()
        self.schiffstyp_combo.addItems(["", "A", "B"])

        self.search_button = QPushButton("Filtrer")
        self.results_list = QListWidget()

        self.search_button.clicked.connect(self.apply_filters)

        # Ajout des widgets au layout
        layout.addWidget(self.meerart_label)
        layout.addWidget(self.meerart_combo)
        layout.addWidget(self.naechte_label)
        layout.addWidget(self.naechte_input)
        layout.addWidget(self.staedte_label)
        layout.addWidget(self.staedte_input)
        layout.addWidget(self.schiffstyp_label)
        layout.addWidget(self.schiffstyp_combo)
        layout.addWidget(self.search_button)
        layout.addWidget(self.results_list)

        self.setLayout(layout)

    def apply_filters(self):
        filters = {
            "meerart": self.meerart_combo.currentText(),
            "naechte": int(self.naechte_input.text()) if self.naechte_input.text().isdigit() else None,
            "staedte": [s.strip() for s in self.staedte_input.text().split(",") if s.strip()],
            "schiffstyp": self.schiffstyp_combo.currentText()
        }

        cruises = get_filtered_cruises(filters)
        self.results_list.clear()

        if cruises:
            for c in cruises:
                self.results_list.addItem(c["titel"])
        else:
            self.results_list.addItem("Aucun résultat trouvé.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CruiseFilterApp()
    window.show()
    sys.exit(app.exec_())
