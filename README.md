# Inventory Management System

A modern inventory management system built with PySide6 and SQLite for Infoware India internship assignment.

## Features
- **Login for operators** (two accounts: admin/admin, operator1/operator1)
- **Product Master List**: Add products with barcode, SKU, category, subcategory, image, name, description, tax, price, and default unit
- **Goods Receiving**: Record goods received with product, supplier, quantity, unit, rate, total, and tax
- **Sales Form**: Record sales with product, customer, quantity, unit, rate, total, and tax
- **Category & Subcategory Management**: Add categories and subcategories from the UI
- **Modern, user-friendly UI**: Clean, professional theme and validation

## Setup Instructions
1. **Clone or download this repository**
2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On Linux/Mac:
   source venv/bin/activate
   ```
3. **Install requirements**
   ```bash
   pip install -r requirements.txt
   ```
4. **(Optional) Reset the database**
   Delete `inventory.db` if you want a fresh start.
5. **Add sample categories/subcategories**
   ```bash
   python add_sample_categories.py
   ```
6. **Run the application**
   ```bash
   python main.py
   ```

## Operator Logins
- **admin / admin**
- **operator1 / operator1**

## Usage
- **Product Master**: Add products, categories, and subcategories. Upload product images.
- **Goods Receiving**: Select product and supplier, enter quantity and rate. Unit auto-fills from product.
- **Sales**: Select product and customer, enter quantity and rate. Unit auto-fills from product.
- **All forms validate required fields and show clear error messages.**

## Notes
- If dropdowns are empty, add categories/subcategories (and suppliers/customers) using the UI.
- The UI is designed for clarity and ease of use.
- If you want to package as an EXE, use PyInstaller:
  ```bash
  pyinstaller --onefile --windowed main.py
  ```
