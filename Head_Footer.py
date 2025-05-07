import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QMenu, QLineEdit
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QIcon

class Header(QWidget):
    def __init__(self):
        super().__init__()

        #Logo
        logo_label=QLabel()
        pixmap = QPixmap("logo.png").scaled(100, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignLeft)

        # Bouton Menu
        self.menu_button = QPushButton()
        self.menu_button.setIcon(QIcon("menu2.png"))  # Remplacer par ton icône
        self.menu_button.setIconSize(QSize(30, 30))  # Ajuster la taille de l'icône
        self.menu_button.setStyleSheet("font-size: 14px; color: white; background-color: #48D1CC;")
        self.menu_button.clicked.connect(self.show_menu)

        #Zone de recherche
        self.search_input= QLineEdit()
        self.search_input.setPlaceholderText("search...")
        self.search_input.setStyleSheet("padding: 5px; font-size: 10px; border-radius:5px;")

        #Search
        self.search=QPushButton()
        self.search.setIcon(QIcon("search.png"))
        self.search.setIconSize(QSize(20,20))
        self.search.setStyleSheet("color:white; background-color: white")
        self.search.clicked.connect(self.launch_search)

        # Label Home
        label = QLabel("Home")
        label.setStyleSheet("font-weight:bold; font-size: 18px; color:blue;")

       # Layout horizontal pour logo + menu en haut
        top_layout = QHBoxLayout()
        top_layout.addWidget(logo_label, alignment=Qt.AlignLeft)
        top_layout.addWidget(self.search_input)
        top_layout.addWidget(self.search)
        top_layout.addWidget(self.menu_button, alignment=Qt.AlignRight)
        

        # Layout principal vertical
        boxheader = QVBoxLayout()
        boxheader.setAlignment(Qt.AlignTop)
        boxheader.addLayout(top_layout)
        boxheader.addWidget(label, alignment=Qt.AlignHCenter)

        self.setLayout(boxheader)

    def show_menu(self):
        menu = QMenu(self)
        action1 = menu.addAction("Option 1")
        action2 = menu.addAction("Option 2")
        action1.triggered.connect(self.option1_action)
        action2.triggered.connect(self.option2_action)

        # Affiche le menu sous le bouton
        menu.exec_(self.menu_button.mapToGlobal(self.menu_button.rect().bottomLeft()))

    def option1_action(self):
        print("Option 1 sélectionnée")

    def option2_action(self):
        print("Option 2 sélectionnée")

    def launch_search(self):
        query = self.search_input.text()
        print(f"Recherche : {query}")


# --- Fenêtre principale ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Header()
    window.setWindowTitle("Seavia_Holiday")
    window.resize(300, 200)  # Taille de la fenêtre
    window.show()
    sys.exit(app.exec_())
