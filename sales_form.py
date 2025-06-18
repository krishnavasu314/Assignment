from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
                             QLineEdit, QComboBox, QDoubleSpinBox, QTextEdit,
                             QPushButton, QMessageBox, QGroupBox, QTableWidget,
                             QTableWidgetItem, QHeaderView)
from PySide6.QtCore import Qt
from database import Database

class SalesForm(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.db = Database()
        self.user_id = user_id
        self.setup_ui()
        self.load_categories_subcategories()
        self.load_customers()

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

        # Customer Details Group
        customer_group = QGroupBox("Customer Details")
        customer_layout = QFormLayout()
        customer_layout.setSpacing(15)

        self.customer_combo = QComboBox()
        self.customer_combo.currentIndexChanged.connect(self.load_customer_details)
        customer_layout.addRow("Customer:", self.customer_combo)

        self.customer_name = QLineEdit()
        self.customer_name.setReadOnly(True)
        customer_layout.addRow("Name:", self.customer_name)

        self.customer_phone = QLineEdit()
        self.customer_phone.setReadOnly(True)
        customer_layout.addRow("Phone:", self.customer_phone)

        self.customer_email = QLineEdit()
        self.customer_email.setReadOnly(True)
        customer_layout.addRow("Email:", self.customer_email)

        customer_group.setLayout(customer_layout)
        layout.addWidget(customer_group)

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
        self.sell_button = QPushButton("Sell Product")
        self.sell_button.clicked.connect(self.sell_product)
        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self.clear_form)
        button_layout.addWidget(self.sell_button)
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

    def load_customers(self):
        try:
            customers = self.db.get_all_customers()
            self.customer_combo.clear()
            self.customer_combo.addItem("Select Customer", None)
            for customer in customers:
                self.customer_combo.addItem(customer[1], customer[0])
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load customers: {str(e)}")

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

    def load_customer_details(self):
        try:
            customer_id = self.customer_combo.currentData()
            if customer_id:
                customer = self.db.get_customer_by_id(customer_id)
                if customer:
                    self.customer_name.setText(customer[1])
                    self.customer_phone.setText(customer[2])
                    self.customer_email.setText(customer[3])
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load customer details: {str(e)}")

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
            
        if self.customer_combo.currentData() is None:
            QMessageBox.warning(self, "Validation Error", "Please select a customer")
            return False
            
        if self.quantity_input.value() <= 0:
            QMessageBox.warning(self, "Validation Error", "Please enter a valid quantity")
            return False
            
        if self.rate_input.value() <= 0:
            QMessageBox.warning(self, "Validation Error", "Please enter a valid rate")
            return False
            
        return True

    def sell_product(self):
        if not self.validate_form():
            return
            
        try:
            sale_data = {
                'product_id': self.product_combo.currentData(),
                'customer_id': self.customer_combo.currentData(),
                'user_id': self.user_id,
                'quantity': self.quantity_input.value(),
                'rate': self.rate_input.value(),
                'tax_rate': float(self.tax_rate.text().strip('%')),
                'tax_amount': float(self.tax_amount.text().strip('₹')),
                'total_amount': float(self.total_amount.text().strip('₹'))
            }
            
            self.db.add_sale(sale_data)
            QMessageBox.information(self, "Success", "Product sold successfully!")
            self.clear_form()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to sell product: {str(e)}")

    def clear_form(self):
        self.category_combo.setCurrentIndex(0)
        self.customer_combo.setCurrentIndex(0)
        self.quantity_input.setValue(1)
        self.rate_input.setValue(0)
        self.tax_rate.clear()
        self.tax_amount.clear()
        self.total_amount.clear()
        self.customer_name.clear()
        self.customer_phone.clear()
        self.customer_email.clear()
        self.unit_input.clear() 