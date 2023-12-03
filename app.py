from flask import Flask, render_template, request, redirect, url_for
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime

app = Flask(__name__)

# Custom Jinja filter
def format_datetime(value, format='%m/%d/%Y'):
    if value is None:
        return ""
    return datetime.strptime(value, '%Y-%m-%d %H:%M:%S.%f').strftime(format)

app.jinja_env.filters['datetime'] = format_datetime

def get_db_connection():
    conn = psycopg2.connect(os.environ.get('DATABASE_URL'))
    return conn

@app.route('/', methods=['GET', 'POST'])
def index():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    if request.method == 'POST':
        product_name = request.form.get('productName')
        product_link = request.form.get('productLink')

        cursor.execute("INSERT INTO products (name, link) VALUES (%s, %s)", (product_name, product_link))
        conn.commit()

        return redirect(url_for('index'))

    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()

    return render_template('index.html', products=products)


if __name__ == '__main__':
    app.run(debug=True)
