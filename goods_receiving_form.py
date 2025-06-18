from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
                             QLineEdit, QComboBox, QDoubleSpinBox, QTextEdit,
                             QPushButton, QMessageBox, QGroupBox, QTableWidget,
                             QTableWidgetItem, QHeaderView)
from PySide6.QtCore import Qt
from database import Database

class GoodsReceivingForm(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.db = Database()
        self.user_id = user_id
        self.setup_ui()
        self.load_categories_subcategories()
        self.load_suppliers()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        # Product Selection Group
        product_group = QGroupBox("Product Selection")
        product_layout = QFormLayout()
        product_layout.setSpacing(15)

        self.category_combo = QComboBox()
        self.category_combo.currentIndexChanged.connect(self.filter_subcategories)
        product_layout.addRow("Category:", self.category_combo)

        self.subcategory_combo = QComboBox()
        self.subcategory_combo.currentIndexChanged.connect(self.filter_products)
        product_layout.addRow("Subcategory:", self.subcategory_combo)

        self.product_combo = QComboBox()
        self.product_combo.currentIndexChanged.connect(self.load_product_details)
        product_layout.addRow("Product:", self.product_combo)

        product_group.setLayout(product_layout)
        layout.addWidget(product_group)

        # Supplier Details Group
        supplier_group = QGroupBox("Supplier Details")
        supplier_layout = QFormLayout()
        supplier_layout.setSpacing(15)

        self.supplier_combo = QComboBox()
        self.supplier_combo.currentIndexChanged.connect(self.load_supplier_details)
        supplier_layout.addRow("Supplier:", self.supplier_combo)

        self.supplier_name = QLineEdit()
        self.supplier_name.setReadOnly(True)
        supplier_layout.addRow("Name:", self.supplier_name)

        self.supplier_phone = QLineEdit()
        self.supplier_phone.setReadOnly(True)
        supplier_layout.addRow("Phone:", self.supplier_phone)

        self.supplier_email = QLineEdit()
        self.supplier_email.setReadOnly(True)
        supplier_layout.addRow("Email:", self.supplier_email)

        supplier_group.setLayout(supplier_layout)
        layout.addWidget(supplier_group)

        # Quantity and Rate Group
        quantity_group = QGroupBox("Quantity and Rate")
        quantity_layout = QFormLayout()
        quantity_layout.setSpacing(15)

        self.quantity_input = QDoubleSpinBox()
        self.quantity_input.setRange(1, 999999)
        self.quantity_input.setDecimals(0)
        self.quantity_input.valueChanged.connect(self.calculate_total)
        quantity_layout.addRow("Quantity:", self.quantity_input)

        self.rate_input = QDoubleSpinBox()
        self.rate_input.setRange(0, 999999.99)
        self.rate_input.setDecimals(2)
        self.rate_input.setPrefix("₹")
        self.rate_input.valueChanged.connect(self.calculate_total)
        quantity_layout.addRow("Rate:", self.rate_input)

        self.tax_rate = QLineEdit()
        self.tax_rate.setReadOnly(True)
        quantity_layout.addRow("Tax Rate:", self.tax_rate)

        self.tax_amount = QLineEdit()
        self.tax_amount.setReadOnly(True)
        quantity_layout.addRow("Tax Amount:", self.tax_amount)

        self.total_amount = QLineEdit()
        self.total_amount.setReadOnly(True)
        quantity_layout.addRow("Total Amount:", self.total_amount)

        self.unit_input = QLineEdit()
        self.unit_input.setReadOnly(True)
        quantity_layout.addRow("Unit of Measurement:", self.unit_input)

        quantity_group.setLayout(quantity_layout)
        layout.addWidget(quantity_group)

        # Buttons
        button_layout = QHBoxLayout()
        self.receive_button = QPushButton("Receive Goods")
        self.receive_button.clicked.connect(self.receive_goods)
        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self.clear_form)
        button_layout.addWidget(self.receive_button)
        button_layout.addWidget(self.clear_button)
        layout.addLayout(button_layout)

    def load_categories_subcategories(self):
        try:
            # Load categories
            categories = self.db.get_all_categories()
            self.category_combo.clear()
            self.category_combo.addItem("Select Category", None)
            for category in categories:
                self.category_combo.addItem(category[1], category[0])

            # Load subcategories
            self.filter_subcategories()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load categories: {str(e)}")

    def filter_subcategories(self):
        try:
            category_id = self.category_combo.currentData()
            self.subcategory_combo.clear()
            self.subcategory_combo.addItem("Select Subcategory", None)
            
            if category_id:
                subcategories = self.db.get_subcategories_by_category(category_id)
                for subcategory in subcategories:
                    self.subcategory_combo.addItem(subcategory[1], subcategory[0])
            
            self.filter_products()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load subcategories: {str(e)}")

    def filter_products(self):
        try:
            category_id = self.category_combo.currentData()
            subcategory_id = self.subcategory_combo.currentData()
            
            self.product_combo.clear()
            self.product_combo.addItem("Select Product", None)
            
            if category_id and subcategory_id:
                products = self.db.get_products_by_category_subcategory(category_id, subcategory_id)
                for product in products:
                    self.product_combo.addItem(product[1], product[0])
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load products: {str(e)}")

    def load_suppliers(self):
        try:
            suppliers = self.db.get_all_suppliers()
            self.supplier_combo.clear()
            self.supplier_combo.addItem("Select Supplier", None)
            for supplier in suppliers:
                self.supplier_combo.addItem(supplier[1], supplier[0])
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load suppliers: {str(e)}")

    def load_product_details(self):
        try:
            product_id = self.product_combo.currentData()
            if product_id:
                product = self.db.get_product_by_id(product_id)
                if product:
                    self.rate_input.setValue(product[7])  # Price
                    self.tax_rate.setText(f"{product[8]}%")  # Tax Rate
                    self.unit_input.setText(product[9] or "")  # Default Unit
                    self.calculate_total()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load product details: {str(e)}")

    def load_supplier_details(self):
        try:
            supplier_id = self.supplier_combo.currentData()
            if supplier_id:
                supplier = self.db.get_supplier_by_id(supplier_id)
                if supplier:
                    self.supplier_name.setText(supplier[1])
                    self.supplier_phone.setText(supplier[2])
                    self.supplier_email.setText(supplier[3])
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load supplier details: {str(e)}")

    def calculate_total(self):
        try:
            quantity = self.quantity_input.value()
            rate = self.rate_input.value()
            tax_rate = float(self.tax_rate.text().strip('%'))
            
            subtotal = quantity * rate
            tax_amount = (subtotal * tax_rate) / 100
            total = subtotal + tax_amount
            
            self.tax_amount.setText(f"₹{tax_amount:.2f}")
            self.total_amount.setText(f"₹{total:.2f}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to calculate total: {str(e)}")

    def validate_form(self):
        if self.product_combo.currentData() is None:
            QMessageBox.warning(self, "Validation Error", "Please select a product")
            return False
            
        if self.supplier_combo.currentData() is None:
            QMessageBox.warning(self, "Validation Error", "Please select a supplier")
            return False
            
        if self.quantity_input.value() <= 0:
            QMessageBox.warning(self, "Validation Error", "Please enter a valid quantity")
            return False
            
        if self.rate_input.value() <= 0:
            QMessageBox.warning(self, "Validation Error", "Please enter a valid rate")
            return False
            
        return True

    def receive_goods(self):
        if not self.validate_form():
            return
            
        try:
            goods_data = {
                'product_id': self.product_combo.currentData(),
                'supplier_id': self.supplier_combo.currentData(),
                'user_id': self.user_id,
                'quantity': self.quantity_input.value(),
                'rate': self.rate_input.value(),
                'tax_rate': float(self.tax_rate.text().strip('%')),
                'tax_amount': float(self.tax_amount.text().strip('₹')),
                'total_amount': float(self.total_amount.text().strip('₹'))
            }
            
            self.db.add_goods_receiving(goods_data)
            QMessageBox.information(self, "Success", "Goods received successfully!")
            self.clear_form()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to receive goods: {str(e)}")

    def clear_form(self):
        self.category_combo.setCurrentIndex(0)
        self.supplier_combo.setCurrentIndex(0)
        self.quantity_input.setValue(1)
        self.rate_input.setValue(0)
        self.tax_rate.clear()
        self.tax_amount.clear()
        self.total_amount.clear()
        self.supplier_name.clear()
        self.supplier_phone.clear()
        self.supplier_email.clear()
        self.unit_input.clear() 