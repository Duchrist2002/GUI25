# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QPushButton, QMenu, QGridLayout ,QSizePolicy, QScrollArea
)
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtGui import QPixmap, QIcon, QPalette, QColor
import vlc
from PyQt5.QtGui import QPixmap, QCursor
from PyQt5.QtCore import Qt, pyqtSignal

class Header(QWidget):
    def __init__(self):
        super().__init__()

        # === VLC Video Widget ===
        self.videoframe = QWidget()
        palette = self.videoframe.palette()
        palette.setColor(QPalette.Window, QColor(0, 0, 0))
        self.videoframe.setPalette(palette)
        self.videoframe.setAutoFillBackground(True)

        # Hauteur fixe (250px), largeur adaptable
        self.videoframe.setFixedHeight(250)

        # === VLC Player ===
        self.instance = vlc.Instance("--no-video-title-show", "--video-on-top", "--no-xlib", "--no-osd")
        self.player = self.instance.media_player_new()
        media = self.instance.media_new("small.mp4")
        self.player.set_media(media)

        # Lier la vidéo au widget selon le système
        if sys.platform.startswith("linux"):
            self.player.set_xwindow(self.videoframe.winId())
        elif sys.platform == "win32":
            self.player.set_hwnd(self.videoframe.winId())
        elif sys.platform == "darwin":
            self.player.set_nsobject(int(self.videoframe.winId()))

        # Laisse VLC gérer seul son scaling
        self.player.video_set_scale(0)
        self.player.set_fullscreen(False)
        # on supprime le forcing de ratio :
        # self.player.video_set_aspect_ratio("16:9")

        # === Logo ===
        logo_label = QLabel()
        pixmap = QPixmap("logo.png").scaled(100, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignLeft)

        # === Bouton Menu ===
        self.menu_button = QPushButton()
        self.menu_button.setIcon(QIcon("menu2.png"))
        self.menu_button.setIconSize(QSize(30, 30))
        self.menu_button.setStyleSheet("font-size: 14px; color: white; background-color: #87CEEB;")
        self.menu_button.clicked.connect(self.show_menu)
        
        # Header
        name = QLabel("Seavia Holiday")
        name.setStyleSheet("font-weight:bold; font-size: 40px; color:ADD8E6 ;")
        name.setAlignment(Qt.AlignCenter)
        name.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)



        # === Label Home (après vidéo) ===
        #label = QLabel("Home")
        #label.setStyleSheet("font-weight:bold; font-size: 18px; color:blue;")
        #label.setAlignment(Qt.AlignHCenter)




        # === Layout du haut ===
        top_layout = QHBoxLayout()
        top_layout.addWidget(logo_label, alignment=Qt.AlignLeft)
        top_layout.addWidget(name)
        top_layout.addWidget(self.menu_button, alignment=Qt.AlignRight)
        
        Header_W=QWidget()
        Header_W.setLayout(top_layout)
        Header_W.setStyleSheet("background-color: #CBDCE6;")
        Header_W.setFixedHeight(80)  # Ajuste la hauteur comme tu veux

        # === Layout principal ===
        main_layout = QVBoxLayout()
        main_layout.addWidget(Header_W)        
        main_layout.addWidget(self.videoframe)   # Vidéo (250px de haut)
        #main_layout.addWidget(label)             # Home

        main_layout.addWidget(Home())


        footer = Footer()
        main_layout.addWidget(footer)

        self.setLayout(main_layout)

        # Lancer la vidéo après un petit délai (surtout sous macOS/Windows)
        QTimer.singleShot(300, self.start_video)

    def start_video(self):
        self.player.play()
        self.player.event_manager().event_attach(
            vlc.EventType.MediaPlayerEndReached, self.loop_video
        )

    def show_menu(self):
        menu = QMenu(self)
        action1 = menu.addAction("Option 1")
        action2 = menu.addAction("Option 2")
        action1.triggered.connect(self.option1_action)
        action2.triggered.connect(self.option2_action)
        menu.exec_(self.menu_button.mapToGlobal(self.menu_button.rect().bottomLeft()))

    def option1_action(self):
        print("Option 1 sélectionnée")

    def option2_action(self):
        print("Option 2 sélectionnée")

    def loop_video(self, event):
        self.player.set_position(0)
        self.player.play()

class Home(QWidget):
    def __init__(self):
        super().__init__()

       # Grid_home = QGridLayout()

        image_container = QWidget()
        image_layout = QHBoxLayout()
        image_container.setLayout(image_layout)

        # === Données : image + nom associé ===
        destinations = [
            ("Nordsee.jpeg", "Nordsee", NordseePage()),
            ("Nordpolarmeer.jpeg", "Nordpolarmeer", QWidget()),
            ("Nordpolarmeer2.jpeg", "Polarmeer 2", QWidget()),
            ("mittelmeer.jpeg", "Mittelmeer", MittelmeerPage()),
            ("Nordpolarmeer.jpeg", "Retour Polarmeer", QWidget())
            ]

        for image, name, widget_page in destinations:
            widget = ClickableImageWidget(image, name, widget_page)
            widget.clicked.connect(self.open_page)
            image_layout.addWidget(widget)

        # Scroll horizontal
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(image_container)
        scroll_area.setMinimumHeight(200)

             # --- Nouveau : ajout du QLabel avec le texte ---
        intro_label = QLabel(
            "Begib dich auf ein Abenteuer über die Meere der Welt.\n"
            "Vom ruhigen Nordmeer bis zum Eis des Polarmeers – jedes Ziel birgt eine Überraschung."
        )
        intro_label.setAlignment(Qt.AlignCenter)  # Centrer le texte
        intro_label.setWordWrap(True)  # Autoriser le retour à la ligne

        main_layout = QVBoxLayout()
        main_layout.addWidget(intro_label)
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)

        self.setStyleSheet("""
            QWidget {
                border-radius: 2px;
            }
        """)


    def open_page(self, widget_page):
        print(f"Redirection vers {widget_page.__class__.__name__}")
        widget_page.show()

        
        '''
        for index, (image, name, widget_page) in enumerate(destinations):
            row = index // 3
            col = index % 3
            widget = ClickableImageWidget(image, name, widget_page)
            widget.clicked.connect(self.open_page)
            Grid_home.addWidget(widget, row, col)

        Grid_home.setAlignment(Qt.AlignCenter)
        Grid_home.setHorizontalSpacing(20)
        Grid_home.setVerticalSpacing(20)
        self.setStyleSheet("background-color: #0000;")  # fond sombre

        self.setLayout(Grid_home)

    def open_page(self, widget_page):
        print(f"Redirection vers {widget_page.__class__.__name__}")
        widget_page.show()  # À adapter selon ta logique d’affichage '''



class ClickableImageWidget(QWidget):
    clicked = pyqtSignal(QWidget)  # Nom de la destination

    def __init__(self, image_path, label_text,target_widget):
        super().__init__()

        self.target_widget = target_widget  # QWidget cible
        # Image
        self.image_label = QLabel()
        self.pixmap = QPixmap(image_path)
        self.image_label.setPixmap(
        self.pixmap.scaled(180, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        )
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.image_label.setStyleSheet("...")
        self.image_label.setCursor(Qt.PointingHandCursor)
        self.image_label.mousePressEvent = self.handle_click

        # Texte cliquable
        text_label = QLabel(f"<a href='#'>{label_text}</a>")
        text_label.setAlignment(Qt.AlignCenter)
        text_label.setTextFormat(Qt.RichText)
        text_label.setTextInteractionFlags(Qt.TextBrowserInteraction)
        text_label.setOpenExternalLinks(False)
        text_label.setCursor(Qt.PointingHandCursor)
        text_label.linkActivated.connect(lambda _: self.clicked.emit(self.target_widget))
        text_label.setStyleSheet("""
            QLabel {
                color: #2c2c2c;
                margin-top: 5px;
                font-size: 14px;
            }
            QLabel:hover {
                text-decoration: underline;
            }
        """)


        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)  # pas de marge autour
        layout.setSpacing(4)  # petit espace entre image et texte
        layout.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.image_label)
        layout.addWidget(text_label)

        self.setLayout(layout)
        self.setFixedWidth(180)  # uniformise la largeur de chaque bloc

    def handle_click(self, event):
        self.clicked.emit(self.target_widget)

    def resizeEvent(self, event):
        if self.pixmap:
            scaled = self.pixmap.scaled(
            self.image_label.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
            )
        self.image_label.setPixmap(scaled)
        super().resizeEvent(event)


class NordseePage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Bienvenue sur la page Nordsee"))
        self.setLayout(layout)


class MittelmeerPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Bienvenue sur la page Mittelmeer"))
        self.setLayout(layout)


    

class Footer(QWidget):
    def __init__(self):
        super ().__init__()

        Kontakt=QLabel(
            '📧<b>Kontakts</b><br>'
            '<a href="mailto:contact@seavia.com">📧 contact@seavia.com</a><br>'
            '<a href="tel:+33612345678">📞 +33 6 12 34 56 78</a><br>'
            '📍 123 Rue de la Plage, Marseille'
            
        )

        Kontakt.setTextFormat(Qt.RichText)
        Kontakt.setOpenExternalLinks(True)

        SMedia=QLabel(
            '<a href="Réseaux sociaux">🌐 Réseaux sociaux</a><br>'
            '<a href="Twitter">🐦 Twitter : @SeaviaHoliday</a><br>'
            '<a href="Facebook">📘 Facebook : /SeaviaHoliday</a><br>'
            '<a href="Instagram">📸 Instagram : @SeaviaHoliday</a><br>'
        )
        SMedia.setTextFormat(Qt.RichText)
        SMedia.setOpenExternalLinks(True)

        Links=QLabel(
           '🔗<b>Links</b><br>'
            '<a href="https://seavia.com/home">🏠 Home</a><br>'
            '<a href="https://seavia.com/registration">📝 Registration/Login</a><br>'
            '<a href="https://seavia.com/angebot">📋 Angebote</a><br>'
            '<a href="https://seavia.com/entdecken">🌍 Entdecken</a><br>'
        )
        Links.setTextFormat(Qt.RichText)
        Links.setOpenExternalLinks(True)

       


        Footer=QHBoxLayout()
        Footer.addWidget(Kontakt)
        Footer.addWidget(SMedia)
        Footer.addWidget(Links)

        main_Layout=QHBoxLayout()
        main_Layout.addLayout(Footer)

        self.setLayout(main_Layout)
        self.setStyleSheet("background-color: #F0FFFF; padding: 10px;")
        

# === Main ===
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Header()
    window.setWindowTitle("Seavia_Holiday")
    window.resize(900, 550)
    window.show()
    sys.exit(app.exec_())
