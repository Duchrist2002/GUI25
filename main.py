from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton,
                             QVBoxLayout, QHBoxLayout, QSizePolicy, QSpacerItem,
                             QGraphicsBlurEffect, QStackedLayout, QStackedWidget, QFrame)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import sys

class LoginPage(QWidget):
    def __init__(self, switch_to_signup):
        super().__init__()

        main_layout = QHBoxLayout()

        # === Image + texte superposé ===
        image_container = QFrame()
        stack_layout = QStackedLayout(image_container)

        image_label = QLabel()
        pixmap = QPixmap("Valetta.jpg")
        image_label.setPixmap(pixmap)
        image_label.setScaledContents(True)
        image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        blur_effect = QGraphicsBlurEffect()
        blur_effect.setBlurRadius(2)
        image_label.setGraphicsEffect(blur_effect)

        welcome_label = QLabel("Welcome back, traveler 🌍")
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 32px;
                font-weight: bold;
                background-color: rgba(0, 0, 0, 0.4); 
                padding: 20px;
                border-radius: 10px;
            }
        """)

        stack_layout.addWidget(image_label)
        stack_layout.addWidget(welcome_label)
        main_layout.addWidget(image_container, 3)

        # === Formulaire Login ===
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

        name = create_input("Enter your name")
        password = create_input("Enter your password")
        password.setEchoMode(QLineEdit.Password)

        content_layout.addWidget(name)
        content_layout.addWidget(password)

        login_button = QPushButton("Login")
        login_button.setMinimumHeight(40)
        login_button.setStyleSheet("""
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
        content_layout.addWidget(login_button)

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

<<<<<<< Updated upstream
=======
         # Connexion du bouton login à la méthode handle_login
        self.login_button.clicked.connect(self.handle_login)

    def handle_login(self):  # <-- Valuers_User + comparaison + conclusion
        username = self.name.text()
        password = self.password.text()

        conn = sqlite3.connect("user.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username=Trésor AND password=Qlolo", (username, password))
        result = cursor.fetchone()

        if result:
            QMessageBox.information(self, "Succès", "Connexion réussie !")
            # TODO : switch vers la page d’accueil
        else:
            QMessageBox.warning(self, "Erreur", "Nom d'utilisateur ou mot de passe incorrect.")

        conn.close()

        """if username == "admin" and password == "1234":
            QMessageBox.information(self, "Succès", "Connexion réussie !")  # <-- MODIF: utilisation QMessageBox
            # TODO: switch vers la page d'accueil ou autre
        else:
            QMessageBox.warning(self, "Erreur", "Nom d'utilisateur ou mot de passe incorrect.")  # <-- MODIF: QMessageBox erreur

        # Code pour tester la fenêtre"""
        if __name__ == "__main__":
            app = QApplication(sys.argv)
            
            def dummy_switch_to_signup():
                print("Switch to signup called")

            login = LoginPage(dummy_switch_to_signup)
            login.show()
            sys.exit(app.exec_())



>>>>>>> Stashed changes
class SignInPage(QWidget):
    def __init__(self, switch_to_login):
        super().__init__()
        layout = QVBoxLayout()
        layout.setContentsMargins(100, 100, 100, 100)

        title = QLabel("Sign up for Seavia")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 26px; font-weight: bold; color: #007ACC;")
        layout.addWidget(title)

        username = QLineEdit()
        username.setPlaceholderText("Choose a username")
        password = QLineEdit()
        password.setPlaceholderText("Choose a password")
        password.setEchoMode(QLineEdit.Password)
        confirm = QLineEdit()
        confirm.setPlaceholderText("Confirm password")
        confirm.setEchoMode(QLineEdit.Password)

        for widget in (username, password, confirm):
            widget.setMinimumHeight(40)
            widget.setStyleSheet("padding: 10px; font-size: 14px; border: 2px solid #007ACC; border-radius: 8px;")

        layout.addWidget(username)
        layout.addWidget(password)
        layout.addWidget(confirm)

        create_button = QPushButton("Create Account")
        create_button.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                font-size: 16px;
                font-weight: bold;
                border: none;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        layout.addWidget(create_button)

        back_btn = QPushButton("Back to Login")
        back_btn.setStyleSheet("QPushButton { color: #007ACC; background: transparent; border: none; }")
        back_btn.clicked.connect(switch_to_login)
        layout.addWidget(back_btn, alignment=Qt.AlignRight)

        self.setLayout(layout)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Seavia Holiday")
        self.setMinimumSize(800, 600)

        self.stack = QStackedWidget()

        self.login_page = LoginPage(self.show_signup)
        self.signup_page = SignInPage(self.show_login)

        self.stack.addWidget(self.login_page)
        self.stack.addWidget(self.signup_page)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.stack)
        self.setLayout(main_layout)

    def show_signup(self):
        self.stack.setCurrentWidget(self.signup_page)

    def show_login(self):
        self.stack.setCurrentWidget(self.login_page)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
