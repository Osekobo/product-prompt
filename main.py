from flask import Flask, render_template, request, redirect, url_for,flash
from database import get_products, get_sales, insert_products,insert_stock, get_stock, insert_sales

app = Flask(__name__)

app.secret_key = '123wtrdfdcxcf'

@app.route('/')
def home():
    flash("home page successful", "success")
    return render_template("index.html")


@app.route('/products')
def products():
    products = get_products()
    return render_template("products.html", products=products)


@app.route('/sales')
def sales():
    products= get_products()
    sales= get_sales()
    return render_template('sales.html', sales = sales, products = products)


@app.route('/stock')
def stock():
    products= get_products()
    stock = get_stock()
    return render_template("stock.html", products= products, stock = stock)


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/add_products', methods=['GET', 'POST'])
def add_products():
    product_name = request.form['product_name']
    buying_price = request.form["buying"]
    selling_price = request.form["selling"]
    new_product = (product_name, buying_price, selling_price)
    insert_products(new_product)
    flash("Product added successfully!", "success")
    return redirect(url_for('products'))


@app.route('/add_stock', methods=['GET', 'POST'])
def add_stock():
    product_id = request.form['pid']
    stock_quantity = request.form['stock_quantity']
    new_stock = (product_id, stock_quantity)
    insert_stock(new_stock)
    flash("Stock added successfully!", "success")
    return redirect(url_for('stock'))


@app.route('/add_sales', methods=['GET', 'POST'])
def add_sales():
    product_id = request.form['id']
    sales_quantity = request.form['quantity']
    new_sales = (product_id, sales_quantity)
    insert_sales(new_sales)
    flash("Sale made successfully!", "success")
    return redirect(url_for('sales'))

app.run(debug=True)

# debugging from browser and relation with productiion , html escaping, variable rules
