import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from login_window import LoginWindow

def main():
    app = QApplication(sys.argv)
    
    # Set application-wide modern stylesheet
    app.setStyleSheet("""
        QWidget {
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 13px;
            background: #f7f9fb;
            color: #222;
        }
        QMainWindow {
            background: #f7f9fb;
        }
        QGroupBox {
            font-weight: 600;
            border: 1.5px solid #e0e3ea;
            border-radius: 10px;
            margin-top: 1em;
            padding-top: 10px;
            background: #fff;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top left;
            padding: 0 8px;
            color: #1976D2;
            font-size: 15px;
        }
        QLineEdit, QTextEdit, QComboBox, QSpinBox, QDoubleSpinBox {
            padding: 8px;
            border: 1.5px solid #BDBDBD;
            border-radius: 6px;
            background: #fff;
            color: #222;
            font-size: 15px;
        }
        QLineEdit:focus, QTextEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus {
            border: 1.5px solid #1976D2;
            background: #f0f7ff;
        }
        QLabel {
            color: #222;
        }
        QPushButton {
            background: #1976D2;
            color: white;
            font-weight: 600;
            font-size: 15px;
            padding: 10px 0;
            border: none;
            border-radius: 6px;
            min-width: 100px;
        }
        QPushButton:hover {
            background: #1565C0;
        }
        QPushButton:pressed {
            background: #0D47A1;
        }
        QTableWidget {
            border: 1.5px solid #e0e3ea;
            border-radius: 8px;
            background: #fff;
            gridline-color: #e0e3ea;
        }
        QTableWidget::item {
            padding: 6px;
            color: #222;
        }
        QTableWidget::item:selected {
            background: #1976D2;
            color: white;
        }
        QHeaderView::section {
            background: #e3eafc;
            color: #1976D2;
            padding: 8px;
            border: none;
            font-weight: 600;
            font-size: 14px;
        }
        QMessageBox {
            background: #fff;
        }
        QMessageBox QPushButton {
            min-width: 80px;
        }
        QCheckBox {
            font-size: 13px;
        }
    """)
    
    # Create and show login window
    login_window = LoginWindow()
    login_window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 