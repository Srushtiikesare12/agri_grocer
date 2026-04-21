import sqlite3

conn = sqlite3.connect('agri_grocer.db')
cursor = conn.cursor()

# --- Tables ---

# Vendors
cursor.execute('''
CREATE TABLE IF NOT EXISTS vendors (
    vendor_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL,
    shop_name TEXT NOT NULL
)
''')

# Products
cursor.execute('''
CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    vendor_id INTEGER,
    name TEXT NOT NULL,
    description TEXT,
    price INTEGER,
    stock INTEGER,
    image TEXT,
    FOREIGN KEY(vendor_id) REFERENCES vendors(vendor_id)
)
''')

# Subsidies
cursor.execute('''
CREATE TABLE IF NOT EXISTS subsidies (
    subsidy_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER,
    info TEXT,
    FOREIGN KEY(product_id) REFERENCES products(product_id)
)
''')

# Users
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
''')

# Cart
cursor.execute('''
CREATE TABLE IF NOT EXISTS cart (
    cart_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(product_id) REFERENCES products(product_id)
)
''')

# --- Insert Sample Vendors ---
cursor.execute("INSERT OR IGNORE INTO vendors (vendor_id,name,email,password,shop_name) VALUES (1,'Rohit Sharma','rohit@example.com','1234','Fresh Veggies')")
cursor.execute("INSERT OR IGNORE INTO vendors (vendor_id,name,email,password,shop_name) VALUES (2,'Virat Kohli','virat@example.com','1234','Green Farm')")
cursor.execute("INSERT OR IGNORE INTO vendors (vendor_id,name,email,password,shop_name) VALUES (3,'MS Dhoni','dhoni@example.com','1234','Farm Fresh')")

# --- Insert Sample Products ---
products = [
    (1,'Tomato','Fresh red tomatoes',50,100,'tomato.jpg'),
    (1,'Potato','Organic potatoes',30,200,'potato.jpg'),
    (2,'Onion','Local onions',40,150,'onion.jpg'),
    (2,'Carrot','Fresh carrots',60,120,'carrot.jpg'),
    (3,'Spinach','Organic spinach',20,80,'spinach.jpg')
]

for p in products:
    cursor.execute("INSERT OR IGNORE INTO products (vendor_id,name,description,price,stock,image) VALUES (?,?,?,?,?,?)", p)

# --- Insert Sample Subsidies ---
cursor.execute("INSERT OR IGNORE INTO subsidies (product_id, info) VALUES (1, 'Farmer subsidy 10% off')")
cursor.execute("INSERT OR IGNORE INTO subsidies (product_id, info) VALUES (2, 'Govt subsidy 5%')")
cursor.execute("INSERT OR IGNORE INTO subsidies (product_id, info) VALUES (3, 'Special seasonal subsidy')")

conn.commit()
conn.close()

print("Database setup complete!")