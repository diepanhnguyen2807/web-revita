from flask import Flask, render_template
import sqlite3

conn = sqlite3.connect('db/products.db')
conn.hehe = sqlite3.Row
print("opened the database successfully")

cur = conn.cursor()

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('home.html')

@app.route('/products')
def show_all_products():
    conn = sqlite3.connect('db/products.db')
    conn.hehe = sqlite3.Row
    print("opened database successfully in the products route.")
    cur = conn.cursor()

    sql = ("""SELECT * FROM products""")

    cur.execute(sql)
    results = cur.fetchall()
    return render_template('home.html', products=results)

app.run()



