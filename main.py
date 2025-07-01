from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton,
                             QVBoxLayout, QHBoxLayout, QSizePolicy, QSpacerItem,
                             QGraphicsBlurEffect, QScrollArea, QStackedLayout, QStackedWidget, QFrame, QMessageBox)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import sys

import sqlite3
from backend.data_manager import check_login, add_user, init_db
from standard import Header


class LoginPage(QWidget):
    def __init__(self, switch_to_signup, switch_to_home):
        super().__init__()
        self.switch_to_home = switch_to_home

        main_layout = QHBoxLayout()

        image_container = QFrame()
        stack_layout = QStackedLayout(image_container)

        image_label = QLabel()
        pixmap = QPixmap("assets/Valetta.jpg")
        image_label.setPixmap(pixmap)
        image_label.setScaledContents(True)
        image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        blur_effect = QGraphicsBlurEffect()
        blur_effect.setBlurRadius(2)
        image_label.setGraphicsEffect(blur_effect)

        stack_layout.addWidget(image_label)
        main_layout.addWidget(image_container, 3)

        content_layout = QVBoxLayout()
        content_layout.setSpacing(20)
        content_layout.setContentsMargins(40, 40, 40, 40)
        content_layout.addSpacerItem(QSpacerItem(20, 40))

        title = QLabel("Welcome to your next Travel")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                background-color: #007ACC;
                border-radius: 10px;
                padding: 15px;
                color: white;
                font-weight: bold;
                font-size: 24px;
            }
        """)
        content_layout.addWidget(title)

        def create_input(placeholder):
            line = QLineEdit()
            line.setPlaceholderText(placeholder)
            line.setMinimumHeight(40)
            line.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            line.setStyleSheet("""
                QLineEdit {
                    border: 2px solid #007ACC;
                    border-radius: 10px;
                    padding: 10px;
                    background-color: #f9f9f9;
                    font-size: 14px;
                }
                QLineEdit:focus {
                    border-color: #005999;
                    background-color: #ffffff;
                }
            """)
            return line

        self.name = create_input("Enter your name")
        self.email = create_input("Enter your email")
        self.password = create_input("Enter your password")
        self.password.setEchoMode(QLineEdit.Password)

        content_layout.addWidget(self.name)
        content_layout.addWidget(self.email)
        content_layout.addWidget(self.password)

        self.login_button = QPushButton("Login")
        self.login_button.setMinimumHeight(40)
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                font-weight: bold;
                font-size: 16px;
                border: none;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        content_layout.addWidget(self.login_button)

        signup_link = QPushButton("Create an account")
        signup_link.setStyleSheet("QPushButton { color: #007ACC; background: transparent; border: none; }")
        signup_link.clicked.connect(switch_to_signup)
        content_layout.addWidget(signup_link, alignment=Qt.AlignRight)

        form = QWidget()
        form.setLayout(content_layout)
        form.setStyleSheet("background-color: white;")
        form.setMaximumWidth(1000)

        main_layout.addWidget(form)
        self.setLayout(main_layout)

        self.login_button.clicked.connect(self.handle_login)

    def handle_login(self):
        username = self.name.text()
        email = self.email.text()
        password = self.password.text()

        if check_login(username, email, password):
            QMessageBox.information(self, "Succès", "Connexion réussie !")
            self.switch_to_home()
        else:
            QMessageBox.warning(self, "Erreur", "Identifiants incorrects.")


class SignInPage(QWidget):
    def __init__(self, switch_to_login):
        super().__init__()

        main_layout = QHBoxLayout()

        image_container = QFrame()
        stack_layout = QStackedLayout(image_container)

        image_label = QLabel()
        pixmap = QPixmap("assets/Valencia.jpg")
        image_label.setPixmap(pixmap)
        image_label.setScaledContents(True)
        image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        blur_effect = QGraphicsBlurEffect()
        blur_effect.setBlurRadius(2)
        image_label.setGraphicsEffect(blur_effect)

        stack_layout.addWidget(image_label)
        main_layout.addWidget(image_container, 3)

        form_layout = QVBoxLayout()
        form_layout.setSpacing(20)
        form_layout.setContentsMargins(40, 40, 40, 40)
        form_layout.addSpacerItem(QSpacerItem(20, 40))

        title = QLabel("Create your Seavia account")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                background-color: #007ACC;
                border-radius: 10px;
                padding: 15px;
                color: white;
                font-weight: bold;
                font-size: 24px;
            }
        """)
        form_layout.addWidget(title)

        def create_input(placeholder, password=False):
            line = QLineEdit()
            line.setPlaceholderText(placeholder)
            if password:
                line.setEchoMode(QLineEdit.Password)
            line.setMinimumHeight(40)
            line.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            line.setStyleSheet("""
                QLineEdit {
                    border: 2px solid #007ACC;
                    border-radius: 10px;
                    padding: 10px;
                    background-color: #f9f9f9;
                    font-size: 14px;
                }
                QLineEdit:focus {
                    border-color: #005999;
                    background-color: #ffffff;
                }
            """)
            return line

        self.username = create_input("Choose a username")
        self.email = create_input("enter your email")
        self.password = create_input("Choose a password", password=True)
        self.confirm = create_input("Confirm password", password=True)

        form_layout.addWidget(self.username)
        form_layout.addWidget(self.email)
        form_layout.addWidget(self.password)
        form_layout.addWidget(self.confirm)

        create_button = QPushButton("Create Account")
        create_button.setMinimumHeight(40)
        create_button.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                font-weight: bold;
                font-size: 16px;
                border: none;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        create_button.clicked.connect(self.register_user)
        form_layout.addWidget(create_button)

        back_btn = QPushButton("Back to Login")
        back_btn.setStyleSheet("QPushButton { color: #007ACC; background: transparent; border: none; }")
        back_btn.clicked.connect(switch_to_login)
        form_layout.addWidget(back_btn, alignment=Qt.AlignRight)

        form_widget = QWidget()
        form_widget.setLayout(form_layout)
        form_widget.setStyleSheet("background-color: white;")
        form_widget.setMaximumWidth(1000)

        main_layout.addWidget(form_widget)
        self.setLayout(main_layout)

    def register_user(self):
        name = self.username.text()
        email = self.email.text()
        pwd = self.password.text()
        confirm = self.confirm.text()

        if pwd != confirm:
            QMessageBox.warning(self, "Erreur", "Les mots de passe ne correspondent pas.")
            return

        if add_user(name, email, pwd):
            QMessageBox.information(self, "Succès", "Compte créé avec succès.")
        else:
            QMessageBox.warning(self, "Erreur", "Nom ou email déjà utilisé.")


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Seavia Holiday")
        self.setMinimumSize(800, 600)

        self.stack = QStackedWidget()
        self.login_page = LoginPage(self.show_signup, self.show_home)
        self.signup_page = SignInPage(self.show_login)
        self.home_page = Header()

        self.stack.addWidget(self.login_page)
        self.stack.addWidget(self.signup_page)
        self.stack.addWidget(self.home_page)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.stack)
        self.setLayout(main_layout)

    def show_signup(self):
        self.stack.setCurrentWidget(self.signup_page)

    def show_login(self):
        self.stack.setCurrentWidget(self.login_page)

    def show_home(self):
        self.stack.setCurrentWidget(self.home_page)


if __name__ == "__main__":
    init_db()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
