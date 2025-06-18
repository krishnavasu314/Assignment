from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
                             QLineEdit, QComboBox, QDoubleSpinBox, QTextEdit,
                             QPushButton, QMessageBox, QGroupBox, QTableWidget,
                             QTableWidgetItem, QHeaderView, QInputDialog, QLabel)
from PySide6.QtCore import Qt
from database import Database

class ImageDropLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setText("Drag & Drop Image Here\nor Click to Browse")
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("border: 2px dashed #1976D2; border-radius: 8px; padding: 20px; color: #1976D2;")
        self.setAcceptDrops(True)
        self.setFixedHeight(120)
        self.image_path = None

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                self.setText(f"Image Selected:\n{file_path.split('/')[-1]}")
                self.image_path = file_path
            else:
                self.setText("Invalid file type!")
        event.acceptProposedAction()

    def mousePressEvent(self, event):
        from PySide6.QtWidgets import QFileDialog
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Product Image", "", "Images (*.png *.jpg *.jpeg *.bmp)")
        if file_path:
            self.setText(f"Image Selected:\n{file_path.split('/')[-1]}")
            self.image_path = file_path

class ProductMasterForm(QWidget):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.setup_ui()
        self.load_categories_subcategories()
        self.load_products()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        # Form Group
        form_group = QGroupBox("Add New Product")
        form_layout = QFormLayout()
        form_layout.setSpacing(15)

        self.barcode_input = QLineEdit()
        self.barcode_input.setPlaceholderText("Enter barcode")
        form_layout.addRow("Barcode:", self.barcode_input)

        self.sku_input = QLineEdit()
        self.sku_input.setPlaceholderText("Enter SKU ID")
        form_layout.addRow("SKU ID:", self.sku_input)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter product name")
        form_layout.addRow("Name:", self.name_input)

        # Category row with add button
        cat_row = QHBoxLayout()
        self.category_combo = QComboBox()
        self.category_combo.currentIndexChanged.connect(self.filter_subcategories)
        cat_row.addWidget(self.category_combo)
        self.add_category_btn = QPushButton("+")
        self.add_category_btn.setFixedWidth(28)
        self.add_category_btn.setToolTip("Add Category")
        self.add_category_btn.clicked.connect(self.add_category)
        cat_row.addWidget(self.add_category_btn)
        form_layout.addRow("Category:", cat_row)

        # Subcategory row with add button
        subcat_row = QHBoxLayout()
        self.subcategory_combo = QComboBox()
        subcat_row.addWidget(self.subcategory_combo)
        self.add_subcategory_btn = QPushButton("+")
        self.add_subcategory_btn.setFixedWidth(28)
        self.add_subcategory_btn.setToolTip("Add Subcategory")
        self.add_subcategory_btn.clicked.connect(self.add_subcategory)
        subcat_row.addWidget(self.add_subcategory_btn)
        form_layout.addRow("Subcategory:", subcat_row)

        self.default_unit_input = QLineEdit()
        self.default_unit_input.setPlaceholderText("e.g. pcs, kg, ltr")
        form_layout.addRow("Default Unit:", self.default_unit_input)

        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("Enter product description")
        self.description_input.setMaximumHeight(100)
        form_layout.addRow("Description:", self.description_input)

        self.price_input = QDoubleSpinBox()
        self.price_input.setRange(0, 999999.99)
        self.price_input.setDecimals(2)
        self.price_input.setPrefix("₹")
        form_layout.addRow("Price:", self.price_input)

        self.tax_input = QDoubleSpinBox()
        self.tax_input.setRange(0, 100)
        self.tax_input.setDecimals(2)
        self.tax_input.setSuffix("%")
        form_layout.addRow("Tax Rate:", self.tax_input)

        # Product Image (drag-and-drop)
        self.image_drop = ImageDropLabel()
        form_layout.addRow("Product Image:", self.image_drop)

        # Buttons
        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Add Product")
        self.add_button.clicked.connect(self.add_product)
        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self.clear_form)
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.clear_button)
        form_layout.addRow("", button_layout)

        form_group.setLayout(form_layout)
        layout.addWidget(form_group)

        # Products Table
        table_group = QGroupBox("Product List")
        table_layout = QVBoxLayout()
        
        self.products_table = QTableWidget()
        self.products_table.setColumnCount(10)
        self.products_table.setHorizontalHeaderLabels([
            "Barcode", "SKU ID", "Name", "Category", "Subcategory", "Default Unit", "Description", "Price", "Tax Rate", "Image"
        ])
        self.products_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table_layout.addWidget(self.products_table)
        
        table_group.setLayout(table_layout)
        layout.addWidget(table_group)

    def load_categories_subcategories(self):
        try:
            categories = self.db.get_all_categories()
            self.category_combo.clear()
            self.category_combo.addItem("Select Category", None)
            for category in categories:
                self.category_combo.addItem(category[1], category[0])
            if len(categories) == 0:
                QMessageBox.information(self, "No Categories", "No categories found. Please add a category.")
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
                if len(subcategories) == 0:
                    QMessageBox.information(self, "No Subcategories", "No subcategories found for this category. Please add a subcategory.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load subcategories: {str(e)}")

    def load_products(self):
        try:
            products = self.db.get_all_products()
            self.products_table.setRowCount(len(products))
            
            for row, product in enumerate(products):
                self.products_table.setItem(row, 0, QTableWidgetItem(product[1] or ""))  # Barcode
                self.products_table.setItem(row, 1, QTableWidgetItem(product[2] or ""))  # SKU ID
                self.products_table.setItem(row, 2, QTableWidgetItem(product[3]))  # Name
                self.products_table.setItem(row, 3, QTableWidgetItem(product[10]))  # Category
                self.products_table.setItem(row, 4, QTableWidgetItem(product[11]))  # Subcategory
                self.products_table.setItem(row, 5, QTableWidgetItem(product[8] or ""))  # Default Unit
                self.products_table.setItem(row, 6, QTableWidgetItem(product[6]))  # Description
                self.products_table.setItem(row, 7, QTableWidgetItem(f"₹{product[7]:.2f}"))  # Price
                self.products_table.setItem(row, 8, QTableWidgetItem(f"{product[8]}%"))  # Tax Rate
                self.products_table.setItem(row, 9, QTableWidgetItem(product[9] or ""))  # Image Path
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load products: {str(e)}")

    def validate_form(self):
        if not self.barcode_input.text().strip():
            QMessageBox.warning(self, "Validation Error", "Please enter a barcode")
            return False
        if not self.sku_input.text().strip():
            QMessageBox.warning(self, "Validation Error", "Please enter a SKU ID")
            return False
        if not self.name_input.text().strip():
            QMessageBox.warning(self, "Validation Error", "Please enter a product name")
            return False
        if self.category_combo.currentData() is None:
            QMessageBox.warning(self, "Validation Error", "Please select a category")
            return False
        if self.subcategory_combo.currentData() is None:
            QMessageBox.warning(self, "Validation Error", "Please select a subcategory")
            return False
        if not self.default_unit_input.text().strip():
            QMessageBox.warning(self, "Validation Error", "Please enter a default unit of measurement")
            return False
        if not self.description_input.toPlainText().strip():
            QMessageBox.warning(self, "Validation Error", "Please enter a description")
            return False
        if self.price_input.value() <= 0:
            QMessageBox.warning(self, "Validation Error", "Please enter a valid price")
            return False
        return True

    def add_product(self):
        if not self.validate_form():
            return
        try:
            product_data = {
                'barcode': self.barcode_input.text().strip(),
                'sku_id': self.sku_input.text().strip(),
                'name': self.name_input.text().strip(),
                'category_id': self.category_combo.currentData(),
                'subcategory_id': self.subcategory_combo.currentData(),
                'default_unit': self.default_unit_input.text().strip(),
                'description': self.description_input.toPlainText().strip(),
                'price': self.price_input.value(),
                'tax_rate': self.tax_input.value(),
                'image_path': self.image_drop.image_path
            }
            self.db.add_product(product_data)
            QMessageBox.information(self, "Success", "Product added successfully!")
            self.clear_form()
            self.load_products()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add product: {str(e)}")

    def clear_form(self):
        self.barcode_input.clear()
        self.sku_input.clear()
        self.name_input.clear()
        self.category_combo.setCurrentIndex(0)
        self.subcategory_combo.clear()
        self.default_unit_input.clear()
        self.description_input.clear()
        self.price_input.setValue(0)
        self.tax_input.setValue(0)
        self.image_drop.setText("Drag & Drop Image Here\nor Click to Browse")
        self.image_drop.image_path = None

    def add_category(self):
        name, ok = QInputDialog.getText(self, "Add Category", "Category Name:")
        if ok and name.strip():
            try:
                self.db.add_category(name.strip())
                self.load_categories_subcategories()
                QMessageBox.information(self, "Success", "Category added.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to add category: {str(e)}")

    def add_subcategory(self):
        category_id = self.category_combo.currentData()
        if not category_id:
            QMessageBox.warning(self, "Select Category", "Please select a category first.")
            return
        name, ok = QInputDialog.getText(self, "Add Subcategory", "Subcategory Name:")
        if ok and name.strip():
            try:
                self.db.add_subcategory(category_id, name.strip())
                self.filter_subcategories()
                QMessageBox.information(self, "Success", "Subcategory added.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to add subcategory: {str(e)}") 