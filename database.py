import psycopg2
from datetime import datetime

conn = psycopg2.connect(user="postgres", password="12039",
                        host="localhost", port="5432", database="myduka")

cur = conn.cursor()

# getting products
def get_products():
    cur.execute("select * from products")
    products = cur.fetchall()
    return products


# getting  sales
def get_sales():
    cur.execute("select * from sales")
    sales = cur.fetchall()
    return sales

# getting stock
def get_stock():
    cur.execute("select * from stock")
    stock = cur.fetchall()
    return stock


# method 1 inserting products
def insert_products(values):
    insert_query = "insert into products(name,buying_price,selling_price)values(%s,%s,%s)"
    cur.execute(insert_query, values)
    conn.commit()



# current_datetime = str(datetime.now())

# inserting stock
def insert_stock(values):
    insert_stock = "insert into stock(pid,stock_quantity,created_at)values(%s,%s,now())"
    cur.execute(insert_stock, values)
    conn.commit()


# inserting sale
def insert_sales(values):
    insert_sales = "insert into sales(pid,quantity,created_at)values(%s,%s,now())"
    cur.execute(insert_sales, values)
    conn.commit()


# getting sales per products
def sales_per_products():
    cur.execute("select p.name AS product_name, SUM(s.quantity) AS total_quantity_sold FROM sales s JOIN products p ON s.pid = p.id GROUP BY p.name ORDER BY total_quantity_sold DESC")
    s_p_p = cur.fetchall()
    return s_p_p

# sales per day
def sales_per_day():
    cur.execute("SELECT DATE(created_at) AS sale_date, SUM(quantity) AS total_quantity_sold FROM sales GROUP BY sale_date ORDER BY sale_date")
    s_p_d = cur.fetchall() 
    return s_p_d

# profit per product
def profit_per_prouct():
    cur.execute("SELECT p.name AS product_name, SUM((p.selling_price - p.buying_price) * s.quantity) AS total_profit FROM sales s JOIN products p ON s.pid = p.id GROUP BY p.name ORDER BY total_profit DESC")
    p_p_p = cur.fetchall() 
    return p_p_p

# profit per day
def profit_per_day():
    cur.execute("SELECT DATE(s.created_at) AS sale_date, SUM((p.selling_price - p.buying_price) * s.quantity) AS daily_profit FROM sales s JOIN products p ON s.pid = p.id GROUP BY sale_date ORDER BY sale_date")
    p_p_d = cur.fetchall() 
    return p_p_d

def available_stock(pid):
    cur.execute("select sum(stock.stock_quantity)from stock where pid = %s,(pid,)")
    total_stock = cur.fetchone()[0] or 0
    cur.execute("select sum(sales.quantity)from sales where pid = %s",(pid,))
    total_sold = cur.fetchone()[0] or 0

    return total_stock - total_sold
