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
    insert_products = "insert into products(name,buying_price,selling_price) values(%s,%s,%s)"
    cur.execute(insert_products, values)
    conn.commit()

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

# sales per products
def sales_per_product():
    cur.execute("""
        select products.name as p_name , sum(sales.quantity * products.selling_price) from products
         join sales on products.id = sales.pid group by p_name ;
    """)
    sales_product = cur.fetchall()
    return sales_product

# sales per day
def sales_per_day():
    cur.execute("""
        select date(sales.created_at) as date , sum(sales.quantity * products.selling_price) from sales join
        products on products.id = sales.pid group by date order by date;
    """)
    sales_day = cur.fetchall()
    return sales_day

# profit per product
def profit_per_product():
    cur.execute("""
        select products.name as p_name , sum(sales.quantity * (products.selling_price - products.buying_price))
        as profit from products join sales on products.id = sales.pid group by p_name ;
    """)
    profit_product = cur.fetchall()
    return profit_product

# profit per day
def profit_per_day():
    cur.execute("""
        select date(sales.created_at) as date , sum(sales.quantity * (products.selling_price - products.buying_price))
        as profit from  products join sales on products.id = sales.pid group by date order by date;
    """)
    profit_day = cur.fetchall()
    return profit_day

def available_stock(pid):
    cur.execute(
        "select sum(stock.stock_quantity)from stock where pid = %s", (pid,))
    total_stock = cur.fetchone()[0] or 0
    cur.execute("select sum(sales.quantity)from sales where pid = %s", (pid,))
    total_sold = cur.fetchone()[0] or 0
    return total_stock - total_sold

# checking if user exists
def check_user(email):
    cur.execute("select * from users where users.email = %s",(email,))
    user = cur.fetchone()
    return user

def insert_user(user_details):
    cur.execute("insert into users(full_name,email,phone_number,password)values(%s,%s,%s,%s)",(user_details))
    conn.commit()

#update edited product
def edited_product(x):
    cur.execute("update products set name = %s, buying_price = %s, selling_price = %s where id =%s",x)
    conn.commit()
    
sales_product = sales_per_product()
