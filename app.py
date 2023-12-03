from flask import Flask, render_template, request, redirect, url_for, g
import sqlite3

app = Flask(__name__)
DATABASE = 'product_db.sqlite'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS products (name TEXT, link TEXT)")
        db.commit()

@app.route('/', methods=['GET', 'POST'])
def index():
    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        product_name = request.form.get('productName')
        product_link = request.form.get('productLink')

        cursor.execute("INSERT INTO products (name, link) VALUES (?, ?)", (product_name, product_link))
        db.commit()

        return redirect(url_for('index'))

    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    return render_template('index.html', products=products)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
