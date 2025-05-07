import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QPushButton, QMenu, QSizePolicy
)
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtGui import QPixmap, QIcon, QPalette, QColor
import vlc

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
        media = self.instance.media_new("bateau.mp4")
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
        label = QLabel("Home")
        label.setStyleSheet("font-weight:bold; font-size: 18px; color:blue;")
        label.setAlignment(Qt.AlignHCenter)



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
        main_layout.addWidget(label)             # Home

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
