# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QPushButton, QMenu, QGridLayout ,QSizePolicy, QScrollArea, QStackedWidget
)
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import Qt, QSize, QTimer, pyqtSignal
from PyQt5.QtGui import QPixmap, QIcon, QPalette, QColor
import vlc

from filterseite import MainWindow as FilterWindow  # import interface des filtres

class Header(QWidget):
    def __init__(self):
        super().__init__()

        self.selected_meerart = None

        self.videoframe = QWidget()
        palette = self.videoframe.palette()
        palette.setColor(QPalette.Window, QColor(0, 0, 0))
        self.videoframe.setPalette(palette)
        self.videoframe.setAutoFillBackground(True)
        self.videoframe.setFixedHeight(250)

        self.instance = vlc.Instance("--no-video-title-show", "--video-on-top", "--no-xlib", "--no-osd")
        self.player = self.instance.media_player_new()
        media = self.instance.media_new("small.mp4")
        self.player.set_media(media)

        if sys.platform.startswith("linux"):
            self.player.set_xwindow(self.videoframe.winId())
        elif sys.platform == "win32":
            self.player.set_hwnd(self.videoframe.winId())
        elif sys.platform == "darwin":
            self.player.set_nsobject(int(self.videoframe.winId()))

        self.player.video_set_scale(0)
        self.player.set_fullscreen(False)

        logo_label = QLabel()
        pixmap = QPixmap("logo.png").scaled(100, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignLeft)

        self.menu_button = QPushButton()
        self.menu_button.setIcon(QIcon("menu2.png"))
        self.menu_button.setIconSize(QSize(30, 30))
        self.menu_button.setStyleSheet("font-size: 14px; color: white; background-color: #87CEEB;")
        self.menu_button.clicked.connect(self.show_menu)

        name = QLabel("Seavia Holiday")
        name.setStyleSheet("font-weight:bold; font-size: 40px; color:ADD8E6 ;")
        name.setAlignment(Qt.AlignCenter)
        name.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        top_layout = QHBoxLayout()
        top_layout.addWidget(logo_label, alignment=Qt.AlignLeft)
        top_layout.addWidget(name)
        top_layout.addWidget(self.menu_button, alignment=Qt.AlignRight)

        Header_W = QWidget()
        Header_W.setLayout(top_layout)
        Header_W.setStyleSheet("background-color: #CBDCE6;")
        Header_W.setFixedHeight(80)

        main_layout = QVBoxLayout()
        main_layout.addWidget(Header_W)
        main_layout.addWidget(self.videoframe)

        self.home = Home(self)
        main_layout.addWidget(self.home)

        footer = Footer()
        main_layout.addWidget(footer)

        self.setLayout(main_layout)
        QTimer.singleShot(300, self.start_video)

    def start_video(self):
        self.player.play()
        self.player.event_manager().event_attach(
            vlc.EventType.MediaPlayerEndReached, self.loop_video
        )

    def loop_video(self, event):
        self.player.set_position(0)
        self.player.play()

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

    def open_filterseite(self, meerart):
        self.filterseite = FilterWindow()
        self.filterseite.meerart_cb.setCurrentText(meerart)
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
            ("Nordsee.jpeg", "Nordsee"),
            ("Nordpolarmeer.jpeg", "Nordpolarmeer"),
            ("Mittelmeer.jpeg", "Mittelmeer"),
            ("Ostsee.jpeg", "Ostsee"),
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
        self.setLayout(main_layout)
        self.setStyleSheet("QWidget { border-radius: 2px; }")


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
        self.image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.image_label.setCursor(Qt.PointingHandCursor)
        self.image_label.mousePressEvent = self.handle_click

        text_label = QLabel(f"<a href='#'>{label_text}</a>")
        text_label.setAlignment(Qt.AlignCenter)
        text_label.setTextFormat(Qt.RichText)
        text_label.setTextInteractionFlags(Qt.TextBrowserInteraction)
        text_label.setOpenExternalLinks(False)
        text_label.setCursor(Qt.PointingHandCursor)
        text_label.linkActivated.connect(lambda _: self.clicked.emit(self.label_text))
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
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)
        layout.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.image_label)
        layout.addWidget(text_label)
        self.setLayout(layout)
        self.setFixedWidth(180)

    def handle_click(self, event):
        self.clicked.emit(self.label_text)

    def resizeEvent(self, event):
        if self.pixmap:
            scaled = self.pixmap.scaled(
                self.image_label.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.image_label.setPixmap(scaled)
        super().resizeEvent(event)


class Footer(QWidget):
    def __init__(self):
        super().__init__()
        Kontakt = QLabel(
            '📧<b>Kontakts</b><br>'
            '<a href="mailto:contact@seavia.com">📧 contact@seavia.com</a><br>'
            '<a href="tel:+33612345678">📞 +33 6 12 34 56 78</a><br>'
            '📍 123 Rue de la Plage, Marseille'
        )
        Kontakt.setTextFormat(Qt.RichText)
        Kontakt.setOpenExternalLinks(True)

        SMedia = QLabel(
            '<a href="Réseaux sociaux">🌐 Réseaux sociaux</a><br>'
            '<a href="Twitter">🐦 Twitter : @SeaviaHoliday</a><br>'
            '<a href="Facebook">📘 Facebook : /SeaviaHoliday</a><br>'
            '<a href="Instagram">📸 Instagram : @SeaviaHoliday</a><br>'
        )
        SMedia.setTextFormat(Qt.RichText)
        SMedia.setOpenExternalLinks(True)

        Links = QLabel(
            '🔗<b>Links</b><br>'
            '<a href="https://seavia.com/home">🏠 Home</a><br>'
            '<a href="https://seavia.com/registration">📝 Registration/Login</a><br>'
            '<a href="https://seavia.com/angebot">📋 Angebote</a><br>'
            '<a href="https://seavia.com/entdecken">🌍 Entdecken</a><br>'
        )
        Links.setTextFormat(Qt.RichText)
        Links.setOpenExternalLinks(True)

        Footer = QHBoxLayout()
        Footer.addWidget(Kontakt)
        Footer.addWidget(SMedia)
        Footer.addWidget(Links)

        main_Layout = QHBoxLayout()
        main_Layout.addLayout(Footer)

        self.setLayout(main_Layout)
        self.setStyleSheet("background-color: #F0FFFF; padding: 10px;")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Header()
    window.setWindowTitle("Seavia_Holiday")
    window.resize(900, 550)
    window.show()
    sys.exit(app.exec_())
