import sqlite3

conn = sqlite3.connect('inventory.db')
cur = conn.cursor()

# Add categories
cur.execute("INSERT OR IGNORE INTO categories (name) VALUES ('Electronics')")
cur.execute("INSERT OR IGNORE INTO categories (name) VALUES ('Groceries')")
cur.execute("INSERT OR IGNORE INTO categories (name) VALUES ('Clothing')")

# Get category IDs
cur.execute("SELECT id FROM categories WHERE name='Electronics'")
electronics_id = cur.fetchone()[0]
cur.execute("SELECT id FROM categories WHERE name='Groceries'")
groceries_id = cur.fetchone()[0]
cur.execute("SELECT id FROM categories WHERE name='Clothing'")
clothing_id = cur.fetchone()[0]

# Add subcategories
cur.execute("INSERT OR IGNORE INTO subcategories (category_id, name) VALUES (?, ?)", (electronics_id, 'Mobile Phones'))
cur.execute("INSERT OR IGNORE INTO subcategories (category_id, name) VALUES (?, ?)", (electronics_id, 'Laptops'))
cur.execute("INSERT OR IGNORE INTO subcategories (category_id, name) VALUES (?, ?)", (groceries_id, 'Fruits'))
cur.execute("INSERT OR IGNORE INTO subcategories (category_id, name) VALUES (?, ?)", (groceries_id, 'Vegetables'))
cur.execute("INSERT OR IGNORE INTO subcategories (category_id, name) VALUES (?, ?)", (clothing_id, 'Men'))
cur.execute("INSERT OR IGNORE INTO subcategories (category_id, name) VALUES (?, ?)", (clothing_id, 'Women'))

conn.commit()
conn.close()
print('Sample categories and subcategories added.') 