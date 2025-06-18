from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QGridLayout, QLineEdit, QPushButton, QMessageBox, QLabel, QCheckBox, QFrame, QHBoxLayout)
from PySide6.QtCore import Qt
from main_window import MainWindow
from database import Database

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Inventory Management System - Login")
        self.setFixedSize(420, 340)
        self.setStyleSheet("""
            QMainWindow {
                background: #f4f6fb;
            }
        """)

        # Central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setAlignment(Qt.AlignCenter)

        # Card frame
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 14px;
                border: 1.5px solid #e0e3ea;
                /* box-shadow: 0 4px 24px rgba(0,0,0,0.07); */
            }
        """)
        card.setFixedWidth(340)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(32, 32, 32, 32)
        card_layout.setSpacing(18)

        # Logo/title
        logo = QLabel("<b style='font-size:28px; color:#1976D2;'>IMS</b>")
        logo.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(logo)

        title = QLabel("Sign in to your account")
        title.setStyleSheet("color: #1976D2; font-size: 18px; font-weight: bold; margin-bottom: 8px;")
        title.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(title)

        # Grid layout for form
        form_grid = QGridLayout()
        form_grid.setVerticalSpacing(14)
        form_grid.setHorizontalSpacing(10)

        # Username
        user_label = QLabel("Username:")
        user_label.setStyleSheet("font-size: 14px;")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter username")
        self.username_input.setClearButtonEnabled(True)
        self.username_input.setMinimumHeight(36)
        self.username_input.setStyleSheet("padding: 8px; font-size: 15px; border-radius: 6px; border: 1.5px solid #BDBDBD;")
        form_grid.addWidget(user_label, 0, 0)
        form_grid.addWidget(self.username_input, 0, 1)

        # Password
        pw_label = QLabel("Password:")
        pw_label.setStyleSheet("font-size: 14px;")
        pw_row = QWidget()
        pw_row_layout = QHBoxLayout(pw_row)
        pw_row_layout.setContentsMargins(0, 0, 0, 0)
        pw_row_layout.setSpacing(0)
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setClearButtonEnabled(True)
        self.password_input.setMinimumHeight(36)
        self.password_input.setStyleSheet("padding: 8px; font-size: 15px; border-radius: 6px; border: 1.5px solid #BDBDBD;")
        self.show_pw_checkbox = QCheckBox("Show")
        self.show_pw_checkbox.setStyleSheet("margin-left: 8px; font-size: 13px;")
        self.show_pw_checkbox.toggled.connect(self.toggle_password)
        pw_row_layout.addWidget(self.password_input, 1)
        pw_row_layout.addWidget(self.show_pw_checkbox, 0, Qt.AlignVCenter)
        form_grid.addWidget(pw_label, 1, 0)
        form_grid.addWidget(pw_row, 1, 1)

        card_layout.addLayout(form_grid)

        # Login button
        self.login_button = QPushButton("Login")
        self.login_button.setMinimumHeight(38)
        self.login_button.setStyleSheet("""
            QPushButton {
                background: #1976D2;
                color: white;
                font-size: 16px;
                font-weight: bold;
                border-radius: 6px;
                border: none;
            }
            QPushButton:hover {
                background: #1565C0;
            }
            QPushButton:pressed {
                background: #0D47A1;
            }
        """)
        self.login_button.clicked.connect(self.handle_login)
        card_layout.addWidget(self.login_button)

        # Help text
        help_label = QLabel("<span style='color:#888;'>Default logins: <b>admin/admin</b> or <b>operator1/operator1</b></span>")
        help_label.setAlignment(Qt.AlignCenter)
        help_label.setStyleSheet("font-size:12px; margin-top:8px;")
        card_layout.addWidget(help_label)

        main_layout.addWidget(card, alignment=Qt.AlignCenter)

        # Set focus to username
        self.username_input.setFocus()
        self.username_input.returnPressed.connect(self.handle_login)
        self.password_input.returnPressed.connect(self.handle_login)

    def toggle_password(self, checked):
        self.password_input.setEchoMode(QLineEdit.Normal if checked else QLineEdit.Password)

    def handle_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        error_style = "border: 1.5px solid #D32F2F;"
        normal_style = "border: 1.5px solid #BDBDBD;"
        self.username_input.setStyleSheet(f"padding: 8px; font-size: 15px; border-radius: 6px; {normal_style}")
        self.password_input.setStyleSheet(f"padding: 8px; font-size: 15px; border-radius: 6px; {normal_style}")

        if not username or not password:
            if not username:
                self.username_input.setStyleSheet(f"padding: 8px; font-size: 15px; border-radius: 6px; {error_style}")
            if not password:
                self.password_input.setStyleSheet(f"padding: 8px; font-size: 15px; border-radius: 6px; {error_style}")
            QMessageBox.warning(self, "Validation Error", "Please enter both username and password")
            return

        self.login_button.setEnabled(False)
        try:
            user_id = self.db.validate_user(username, password)
            if user_id:
                self.main_window = MainWindow(user_id)
                self.main_window.show()
                self.close()
            else:
                self.username_input.setStyleSheet(f"padding: 8px; font-size: 15px; border-radius: 6px; {error_style}")
                self.password_input.setStyleSheet(f"padding: 8px; font-size: 15px; border-radius: 6px; {error_style}")
                QMessageBox.warning(self, "Login Failed", "Invalid username or password")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Login failed: {str(e)}")
        finally:
            self.login_button.setEnabled(True) 