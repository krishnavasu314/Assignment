import sqlite3
import os
from datetime import datetime

class Database:
    def __init__(self):
        self.db_name = "inventory.db"
        self.create_tables()

    def connect(self):
        try:
            conn = sqlite3.connect(self.db_name)
            conn.row_factory = sqlite3.Row
            return conn
        except sqlite3.Error as e:
            raise Exception(f"Database connection error: {str(e)}")

    def create_tables(self):
        try:
            conn = self.connect()
            cursor = conn.cursor()

            # Users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Categories table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Subcategories table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS subcategories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category_id INTEGER NOT NULL,
                    name TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (category_id) REFERENCES categories (id),
                    UNIQUE (category_id, name)
                )
            ''')

            # Products table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    barcode TEXT,
                    sku_id TEXT,
                    name TEXT NOT NULL,
                    category_id INTEGER NOT NULL,
                    subcategory_id INTEGER NOT NULL,
                    description TEXT,
                    price REAL NOT NULL,
                    tax_rate REAL NOT NULL,
                    default_unit TEXT,
                    image_path TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (category_id) REFERENCES categories (id),
                    FOREIGN KEY (subcategory_id) REFERENCES subcategories (id)
                )
            ''')

            # Suppliers table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS suppliers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    phone TEXT,
                    email TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Customers table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS customers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    phone TEXT,
                    email TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Goods Receiving table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS goods_receiving (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    product_id INTEGER NOT NULL,
                    supplier_id INTEGER NOT NULL,
                    user_id INTEGER NOT NULL,
                    quantity INTEGER NOT NULL,
                    rate REAL NOT NULL,
                    tax_rate REAL NOT NULL,
                    tax_amount REAL NOT NULL,
                    total_amount REAL NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (product_id) REFERENCES products (id),
                    FOREIGN KEY (supplier_id) REFERENCES suppliers (id),
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')

            # Sales table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sales (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    product_id INTEGER NOT NULL,
                    customer_id INTEGER NOT NULL,
                    user_id INTEGER NOT NULL,
                    quantity INTEGER NOT NULL,
                    rate REAL NOT NULL,
                    tax_rate REAL NOT NULL,
                    tax_amount REAL NOT NULL,
                    total_amount REAL NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (product_id) REFERENCES products (id),
                    FOREIGN KEY (customer_id) REFERENCES customers (id),
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')

            # Create default admin user if not exists
            cursor.execute('''
                INSERT OR IGNORE INTO users (username, password)
                VALUES (?, ?)
            ''', ('admin', 'admin'))

            conn.commit()
        except sqlite3.Error as e:
            raise Exception(f"Error creating tables: {str(e)}")
        finally:
            conn.close()

    def execute_query(self, query, params=None):
        try:
            conn = self.connect()
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            result = cursor.fetchall()
            conn.commit()
            return result
        except sqlite3.Error as e:
            raise Exception(f"Query execution error: {str(e)}")
        finally:
            conn.close()

    def execute_insert(self, query, params):
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute(query, params)
            last_id = cursor.lastrowid
            conn.commit()
            return last_id
        except sqlite3.Error as e:
            raise Exception(f"Insert execution error: {str(e)}")
        finally:
            conn.close()

    # User methods
    def validate_user(self, username, password):
        try:
            result = self.execute_query(
                "SELECT id FROM users WHERE username = ? AND password = ?",
                (username, password)
            )
            return result[0][0] if result else None
        except Exception as e:
            raise Exception(f"User validation error: {str(e)}")

    # Category methods
    def get_all_categories(self):
        try:
            return self.execute_query("SELECT * FROM categories ORDER BY name")
        except Exception as e:
            raise Exception(f"Error getting categories: {str(e)}")

    def add_category(self, name):
        try:
            return self.execute_insert(
                "INSERT INTO categories (name) VALUES (?)",
                (name,)
            )
        except Exception as e:
            raise Exception(f"Error adding category: {str(e)}")

    # Subcategory methods
    def get_subcategories_by_category(self, category_id):
        try:
            return self.execute_query(
                "SELECT * FROM subcategories WHERE category_id = ? ORDER BY name",
                (category_id,)
            )
        except Exception as e:
            raise Exception(f"Error getting subcategories: {str(e)}")

    def add_subcategory(self, category_id, name):
        try:
            return self.execute_insert(
                "INSERT INTO subcategories (category_id, name) VALUES (?, ?)",
                (category_id, name)
            )
        except Exception as e:
            raise Exception(f"Error adding subcategory: {str(e)}")

    # Product methods
    def get_all_products(self):
        try:
            return self.execute_query('''
                SELECT p.*, c.name as category_name, s.name as subcategory_name
                FROM products p
                JOIN categories c ON p.category_id = c.id
                JOIN subcategories s ON p.subcategory_id = s.id
                ORDER BY p.name
            ''')
        except Exception as e:
            raise Exception(f"Error getting products: {str(e)}")

    def get_products_by_category_subcategory(self, category_id, subcategory_id):
        try:
            return self.execute_query('''
                SELECT p.*, c.name as category_name, s.name as subcategory_name
                FROM products p
                JOIN categories c ON p.category_id = c.id
                JOIN subcategories s ON p.subcategory_id = s.id
                WHERE p.category_id = ? AND p.subcategory_id = ?
                ORDER BY p.name
            ''', (category_id, subcategory_id))
        except Exception as e:
            raise Exception(f"Error getting products: {str(e)}")

    def get_product_by_id(self, product_id):
        try:
            result = self.execute_query(
                "SELECT * FROM products WHERE id = ?",
                (product_id,)
            )
            return result[0] if result else None
        except Exception as e:
            raise Exception(f"Error getting product: {str(e)}")

    def add_product(self, product_data):
        try:
            return self.execute_insert('''
                INSERT INTO products (barcode, sku_id, name, category_id, subcategory_id, description, price, tax_rate, default_unit, image_path)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                product_data.get('barcode'),
                product_data.get('sku_id'),
                product_data['name'],
                product_data['category_id'],
                product_data['subcategory_id'],
                product_data['description'],
                product_data['price'],
                product_data['tax_rate'],
                product_data.get('default_unit'),
                product_data.get('image_path')
            ))
        except Exception as e:
            raise Exception(f"Error adding product: {str(e)}")

    # Supplier methods
    def get_all_suppliers(self):
        try:
            return self.execute_query("SELECT * FROM suppliers ORDER BY name")
        except Exception as e:
            raise Exception(f"Error getting suppliers: {str(e)}")

    def get_supplier_by_id(self, supplier_id):
        try:
            result = self.execute_query(
                "SELECT * FROM suppliers WHERE id = ?",
                (supplier_id,)
            )
            return result[0] if result else None
        except Exception as e:
            raise Exception(f"Error getting supplier: {str(e)}")

    def add_supplier(self, supplier_data):
        try:
            return self.execute_insert('''
                INSERT INTO suppliers (name, phone, email)
                VALUES (?, ?, ?)
            ''', (
                supplier_data['name'],
                supplier_data['phone'],
                supplier_data['email']
            ))
        except Exception as e:
            raise Exception(f"Error adding supplier: {str(e)}")

    # Customer methods
    def get_all_customers(self):
        try:
            return self.execute_query("SELECT * FROM customers ORDER BY name")
        except Exception as e:
            raise Exception(f"Error getting customers: {str(e)}")

    def get_customer_by_id(self, customer_id):
        try:
            result = self.execute_query(
                "SELECT * FROM customers WHERE id = ?",
                (customer_id,)
            )
            return result[0] if result else None
        except Exception as e:
            raise Exception(f"Error getting customer: {str(e)}")

    def add_customer(self, customer_data):
        try:
            return self.execute_insert('''
                INSERT INTO customers (name, phone, email)
                VALUES (?, ?, ?)
            ''', (
                customer_data['name'],
                customer_data['phone'],
                customer_data['email']
            ))
        except Exception as e:
            raise Exception(f"Error adding customer: {str(e)}")

    # Goods Receiving methods
    def add_goods_receiving(self, goods_data):
        try:
            return self.execute_insert('''
                INSERT INTO goods_receiving (
                    product_id, supplier_id, user_id, quantity, rate,
                    tax_rate, tax_amount, total_amount
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                goods_data['product_id'],
                goods_data['supplier_id'],
                goods_data['user_id'],
                goods_data['quantity'],
                goods_data['rate'],
                goods_data['tax_rate'],
                goods_data['tax_amount'],
                goods_data['total_amount']
            ))
        except Exception as e:
            raise Exception(f"Error adding goods receiving: {str(e)}")

    # Sales methods
    def add_sale(self, sale_data):
        try:
            return self.execute_insert('''
                INSERT INTO sales (
                    product_id, customer_id, user_id, quantity, rate,
                    tax_rate, tax_amount, total_amount
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                sale_data['product_id'],
                sale_data['customer_id'],
                sale_data['user_id'],
                sale_data['quantity'],
                sale_data['rate'],
                sale_data['tax_rate'],
                sale_data['tax_amount'],
                sale_data['total_amount']
            ))
        except Exception as e:
            raise Exception(f"Error adding sale: {str(e)}") 