# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QPushButton, QMenu, QScrollArea, QSizePolicy
)
from PyQt5.QtCore import Qt, QSize, QTimer, pyqtSignal
from PyQt5.QtGui import QPixmap, QIcon, QPalette, QColor
import vlc

from filterseite import MainStackedApp as FilterWindow


class Header(QWidget):
    def __init__(self):
        super().__init__()

        self.selected_meerart = None

        # === VIDEO FRAME ===
        self.videoframe = QWidget()
        palette = self.videoframe.palette()
        palette.setColor(QPalette.Window, QColor(0, 0, 0))
        self.videoframe.setPalette(palette)
        self.videoframe.setAutoFillBackground(True)
        self.videoframe.setFixedHeight(250)
        self.videoframe.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.instance = vlc.Instance("--no-video-title-show", "--video-on-top", "--no-xlib", "--no-osd")
        self.player = self.instance.media_player_new()
        media = self.instance.media_new("assets/small.mp4")
        self.player.set_media(media)
        QTimer.singleShot(300, self.setup_vlc_output)

        # === HEADER (logo + titre + user + menu) ===
        logo_label = QLabel()
        pixmap = QPixmap("assets/logo.png").scaled(100, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignLeft)

        self.menu_button = QPushButton("≡")
        self.menu_button.setFixedSize(40, 40)
        self.menu_button.setStyleSheet("""
            QPushButton {
                background-color: #007ACC; 
                color: white;
                border: none;
                border-radius: 20px;
                font-size: 20px;
            }
            QPushButton:hover {
                background-color: #005999;
            }
        """)
        self.menu_button.clicked.connect(self.show_menu)

        name = QLabel("Seavia Holiday")
        name.setStyleSheet("""
            QLabel {
                background-color: #007ACC;
                color: white;
                font-size: 28px;
                font-weight: bold;
                padding: 8px 16px;
                border-radius: 12px;
            }
        """)
        name.setAlignment(Qt.AlignCenter)

        # user info
        from backend.user_capital_manager import get_current_user, get_user_capital
        username = get_current_user()
        if username:
            capital = get_user_capital(username)
            self.user_info = QLabel(f"👤 {username} | Kapital: {capital} €")
        else:
            self.user_info = QLabel("👤 kein nutzer verbunden | Kapital: 0 €")
        self.user_info.setStyleSheet("""
            QLabel {
                background-color: #ffffff;
                color: #333;
                font-size: 16px;
                padding: 6px 12px;
                border-radius: 8px;
                border: 2px solid #007ACC;
            }
        """)
        self.user_info.setAlignment(Qt.AlignRight)

        # header layout
        top_layout = QHBoxLayout()
        top_layout.addWidget(logo_label)
        top_layout.addWidget(name, stretch=1)
        top_layout.addWidget(self.user_info)
        top_layout.addWidget(self.menu_button)

        header_widget = QWidget()
        header_widget.setLayout(top_layout)
        header_widget.setStyleSheet("background-color: #F0F8FF; border-bottom: 2px solid #007ACC; padding: 6px;")

        # === MAIN LAYOUT ===
        main_layout = QVBoxLayout()
        main_layout.addWidget(header_widget)
        main_layout.addWidget(self.videoframe)

        self.home = Home(self)
        self.home.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
                border-radius: 12px;
                padding: 12px;
                margin: 10px;
            }
        """)
        main_layout.addWidget(self.home)

        footer = Footer()
        footer.setStyleSheet("""
            QWidget {
                background-color: #CBDCE6;
                border-top: 2px solid #007ACC;
                border-radius: 0 0 12px 12px;
                padding: 8px;
            }
        """)
        main_layout.addWidget(footer)

        self.setLayout(main_layout)

    def setup_vlc_output(self):
        if sys.platform.startswith("linux"):
            self.player.set_xwindow(self.videoframe.winId())
        elif sys.platform == "win32":
            self.player.set_hwnd(self.videoframe.winId())
        elif sys.platform == "darwin":
            self.player.set_nsobject(int(self.videoframe.winId()))
        self.start_video()

    def start_video(self):
        self.player.play()
        self.adjust_video_aspect()
        self.player.event_manager().event_attach(
            vlc.EventType.MediaPlayerEndReached, self.loop_video
        )

    def adjust_video_aspect(self):
        w, h = self.videoframe.width(), self.videoframe.height()
        if w > 0 and h > 0:
            aspect_ratio = f"{w}:{h}"
            self.player.video_set_aspect_ratio(aspect_ratio)

    def loop_video(self, event):
        self.player.set_position(0)
        self.player.play()

    def show_menu(self):
        menu = QMenu(self)
        action1 = menu.addAction("🔍 Option 1")
        action2 = menu.addAction("⚙ Option 2")
        action1.triggered.connect(self.option1_action)
        action2.triggered.connect(self.option2_action)
        menu.exec_(self.menu_button.mapToGlobal(self.menu_button.rect().bottomLeft()))

    def option1_action(self):
        print("Option 1 sélectionnée")

    def option2_action(self):
        print("Option 2 sélectionnée")

    def open_filterseite(self, meerart):
        self.filterseite = FilterWindow()
        self.filterseite.select_meerart_and_open(meerart)
        self.filterseite.show()
        self.close()


class Home(QWidget):
    def __init__(self, parent_header):
        super().__init__()
        self.parent_header = parent_header

        image_container = QWidget()
        image_layout = QHBoxLayout()
        image_container.setLayout(image_layout)

        destinations = [
            ("assets/see/Nordsee.jpg", "Nordsee"),
            ("assets/see/Nordpolarmeer.jpg", "Nordpolarmeer"),
            ("assets/see/Mittelmeer.jpg", "Mittelmeer"),
            ("assets/see/Ostsee.jpg", "Ostsee"),
        ]

        for image, name in destinations:
            widget = ClickableImageWidget(image, name)
            widget.clicked.connect(lambda n=name: self.parent_header.open_filterseite(n))
            image_layout.addWidget(widget)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(image_container)
        scroll_area.setMinimumHeight(200)

        intro_label = QLabel(
            "Begib dich auf ein Abenteuer über die Meere der Welt.\n"
            "Vom ruhigen Nordmeer bis zum Eis des Polarmeers – jedes Ziel birgt eine Überraschung."
        )
        intro_label.setAlignment(Qt.AlignCenter)
        intro_label.setWordWrap(True)

        main_layout = QVBoxLayout()
        main_layout.addWidget(intro_label)
        main_layout.addWidget(scroll_area)

        back_to_login_btn = QPushButton("← Retour au Login")
        back_to_login_btn.clicked.connect(self.return_to_login)
        main_layout.addWidget(back_to_login_btn)

        self.setLayout(main_layout)

    def return_to_login(self):
        from main import MainWindow
        self.login_window = MainWindow()
        self.login_window.show()
        self.parent_header.close()


class ClickableImageWidget(QWidget):
    clicked = pyqtSignal(str)

    def __init__(self, image_path, label_text):
        super().__init__()
        self.label_text = label_text

        self.image_label = QLabel()
        self.pixmap = QPixmap(image_path)
        self.image_label.setPixmap(
            self.pixmap.scaled(180, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        )
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setCursor(Qt.PointingHandCursor)

        text_label = QLabel(f"<a href='#'>{label_text}</a>")
        text_label.setAlignment(Qt.AlignCenter)
        text_label.setTextFormat(Qt.RichText)
        text_label.setTextInteractionFlags(Qt.TextBrowserInteraction)
        text_label.setOpenExternalLinks(False)
        text_label.linkActivated.connect(lambda _: self.clicked.emit(self.label_text))
        text_label.setStyleSheet("""
            QLabel {
                color: #007ACC;
                font-size: 14px;
            }
            QLabel:hover {
                text-decoration: underline;
            }
        """)

        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(text_label)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)
        self.setStyleSheet("""
            QWidget {
                background: #ffffff;
                border: 2px solid #007ACC;
                border-radius: 12px;
            }
            QWidget:hover {
                background: #f0f8ff;
            }
        """)


class Footer(QWidget):
    def __init__(self):
        super().__init__()
        Kontakt = QLabel(
            '📧 <b>Kontakt</b><br>'
            '<a href="mailto:contact@seavia.com">contact@seavia.com</a><br>'
            '<a href="tel:+33612345678">+33 6 12 34 56 78</a><br>'
            '📍 Marseille'
        )
        Kontakt.setTextFormat(Qt.RichText)
        Kontakt.setOpenExternalLinks(True)

        SMedia = QLabel(
            '<a href="#">🌐 Réseaux sociaux</a><br>'
            '<a href="#">🐦 Twitter : @SeaviaHoliday</a><br>'
            '<a href="#">📘 Facebook : /SeaviaHoliday</a><br>'
            '<a href="#">📸 Instagram : @SeaviaHoliday</a><br>'
        )
        SMedia.setTextFormat(Qt.RichText)
        SMedia.setOpenExternalLinks(True)

        Links = QLabel(
            '🔗 <b>Links</b><br>'
            '<a href="#">🏠 Home</a><br>'
            '<a href="#">📝 Registration/Login</a><br>'
            '<a href="#">📋 Angebote</a><br>'
            '<a href="#">🌍 Entdecken</a><br>'
        )
        Links.setTextFormat(Qt.RichText)
        Links.setOpenExternalLinks(True)

        footer_layout = QHBoxLayout()
        footer_layout.addWidget(Kontakt)
        footer_layout.addWidget(SMedia)
        footer_layout.addWidget(Links)
        self.setLayout(footer_layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Header()
    window.setWindowTitle("Seavia_Holiday")
    window.resize(1000, 650)
    window.show()
    sys.exit(app.exec_())
