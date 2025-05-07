# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout
# Créer l'application
app = QApplication(sys.argv)

# Créer une fenêtre
fenetre = QWidget()
fenetre.setWindowTitle("Ma première fenêtre PyQt5")

# Créer un layout vertical
layout_v = QVBoxLayout()

# Ajouter un bouton au layout
layout_v.addWidget(QPushButton("B1"))
layout_v.addWidget(QPushButton("B2"))
layout_v.addWidget(QPushButton("B3"))

layout_h = QHBoxLayout()

layout_h.addWidget(QPushButton("B1"))
layout_h.addWidget(QPushButton("B2"))

# Créer un layout principal pour combiner les deux
layout_principal = QVBoxLayout()

# Ajouter le layout horizontal dans le layout principal
layout_principal.addLayout(layout_h)

# Ajouter le layout vertical dans le layout principal
layout_principal.addLayout(layout_v)

# Appliquer le layout à la fenêtre
fenetre.setLayout(layout_principal)

# Afficher la fenêtre
fenetre.show()

# Lancer la boucle de l'application
sys.exit(app.exec_())
