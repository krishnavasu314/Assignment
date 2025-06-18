from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QStackedWidget, QMessageBox)
from PySide6.QtCore import Qt
from product_master_form import ProductMasterForm
from goods_receiving_form import GoodsReceivingForm
from sales_form import SalesForm

class MainWindow(QMainWindow):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Inventory Management System")
        self.setMinimumSize(1200, 800)

        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # Create navigation buttons
        nav_widget = QWidget()
        nav_layout = QVBoxLayout(nav_widget)
        nav_layout.setSpacing(10)
        nav_layout.setContentsMargins(10, 10, 10, 10)

        self.product_master_btn = QPushButton("Product Master")
        self.product_master_btn.clicked.connect(lambda: self.show_form(0))
        nav_layout.addWidget(self.product_master_btn)

        self.goods_receiving_btn = QPushButton("Goods Receiving")
        self.goods_receiving_btn.clicked.connect(lambda: self.show_form(1))
        nav_layout.addWidget(self.goods_receiving_btn)

        self.sales_btn = QPushButton("Sales")
        self.sales_btn.clicked.connect(lambda: self.show_form(2))
        nav_layout.addWidget(self.sales_btn)

        nav_layout.addStretch()
        main_layout.addWidget(nav_widget)

        # Create stacked widget for forms
        self.stacked_widget = QStackedWidget()
        
        # Add forms to stacked widget
        self.product_master_form = ProductMasterForm()
        self.goods_receiving_form = GoodsReceivingForm(self.user_id)
        self.sales_form = SalesForm(self.user_id)
        
        self.stacked_widget.addWidget(self.product_master_form)
        self.stacked_widget.addWidget(self.goods_receiving_form)
        self.stacked_widget.addWidget(self.sales_form)
        
        main_layout.addWidget(self.stacked_widget)

        # Set initial form
        self.show_form(0)

    def show_form(self, index):
        self.stacked_widget.setCurrentIndex(index)
        
        # Update button styles
        buttons = [self.product_master_btn, self.goods_receiving_btn, self.sales_btn]
        for i, btn in enumerate(buttons):
            if i == index:
                btn.setStyleSheet("""
                    QPushButton {
                        background: #1976D2;
                        color: white;
                        font-weight: bold;
                        padding: 10px;
                        border: none;
                        border-radius: 4px;
                    }
                """)
            else:
                btn.setStyleSheet("""
                    QPushButton {
                        background: #2196F3;
                        color: white;
                        font-weight: bold;
                        padding: 10px;
                        border: none;
                        border-radius: 4px;
                    }
                    QPushButton:hover {
                        background: #1976D2;
                    }
                """) 