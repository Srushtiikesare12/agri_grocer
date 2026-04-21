import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = "your_secret_key"

# ------------------- Home -------------------
@app.route('/')
def home():
    return render_template('home.html')

# ------------------- Register -------------------
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('agri_grocer.db')
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username,email,password) VALUES (?,?,?)", 
                           (username,email,password))
            conn.commit()
            flash("Registration successful! Please login.")
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash("Email already exists!")
        finally:
            conn.close()

    return render_template('register.html')

# ------------------- Login -------------------
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('agri_grocer.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email=? AND password=?", (email,password))
        user = cursor.fetchone()
        conn.close()
        if user:
            session['loggedin'] = True
            session['id'] = user[0]
            session['username'] = user[1]
            flash("Login successful!")
            return redirect(url_for('home'))
        else:
            flash("Invalid email or password!")
    return render_template('login.html')

# ------------------- Products -------------------
@app.route('/products')
def products():
    conn = sqlite3.connect('agri_grocer.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()
    return render_template('products.html', products=products)

# ------------------- Add to Cart -------------------
@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    if 'loggedin' not in session:
        flash("Please login first!")
        return redirect(url_for('login'))
    conn = sqlite3.connect('agri_grocer.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cart WHERE user_id=? AND product_id=?", (session['id'],product_id))
    exists = cursor.fetchone()
    if exists:
        cursor.execute("UPDATE cart SET quantity = quantity + 1 WHERE user_id=? AND product_id=?", (session['id'],product_id))
    else:
        cursor.execute("INSERT INTO cart (user_id, product_id, quantity) VALUES (?,?,1)", (session['id'],product_id))
    conn.commit()
    conn.close()
    flash("Product added to cart!")
    return redirect(url_for('products'))

# ------------------- Cart -------------------
@app.route('/cart')
def cart():
    if 'loggedin' in session:
        conn = sqlite3.connect('agri_grocer.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT p.product_id, p.name, p.image, p.price, c.quantity, v.shop_name
            FROM cart c
            JOIN products p ON c.product_id = p.product_id
            JOIN vendors v ON p.vendor_id = v.vendor_id
            WHERE c.user_id=?
        ''', (session['id'],))
        cart_items = cursor.fetchall()
        conn.close()
        return render_template('cart.html', cart_items=cart_items)
    else:
        flash("Please login first!")
        return redirect(url_for('login'))

# ------------------- Remove Item from Cart -------------------
@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    if 'loggedin' in session:
        conn = sqlite3.connect('agri_grocer.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cart WHERE product_id=? AND user_id=?", (product_id, session['id']))
        conn.commit()
        conn.close()
        flash("Item removed from cart!")
    return redirect(url_for('cart'))

# ------------------- Vendor Page -------------------
@app.route('/vendor/<int:vendor_id>')
def vendor(vendor_id):
    conn = sqlite3.connect('agri_grocer.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM vendors WHERE vendor_id=?', (vendor_id,))
    vendor = cursor.fetchone()
    cursor.execute('SELECT * FROM products WHERE vendor_id=?', (vendor_id,))
    products = cursor.fetchall()
    conn.close()
    return render_template('vendor.html', vendor=vendor, products=products)

# ------------------- Subsidy Page -------------------
@app.route('/subsidy/<int:product_id>')
def subsidy(product_id):
    conn = sqlite3.connect('agri_grocer.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM products WHERE product_id=?', (product_id,))
    product = cursor.fetchone()
    cursor.execute('SELECT info FROM subsidies WHERE product_id=?', (product_id,))
    subsidy_info = cursor.fetchone()
    conn.close()
    return render_template('subsidy.html', product=product, subsidy_info=subsidy_info[0] if subsidy_info else "No subsidy available")

# ------------------- Checkout -------------------
@app.route('/checkout', methods=['GET','POST'])
def checkout():
    if 'loggedin' not in session:
        flash("Please login first!")
        return redirect(url_for('login'))
    conn = sqlite3.connect('agri_grocer.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT p.name, p.price, c.quantity FROM cart c
        JOIN products p ON c.product_id=p.product_id
        WHERE c.user_id=?
    ''', (session['id'],))
    cart_items = cursor.fetchall()
    total = sum([item[1]*item[2] for item in cart_items])
    conn.close()
    if request.method=='POST':
        name = request.form['name']
        address = request.form['address']
        payment_method = request.form['payment_method']
        flash("Payment Successful!")
        return redirect(url_for('cart'))
    return render_template('checkout.html', cart_items=cart_items, total=total)

# ------------------- Logout -------------------
@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully!")
    return redirect(url_for('login'))

# ------------------- Run App -------------------
if __name__ == '__main__':
    app.run(debug=True)