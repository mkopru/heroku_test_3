from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# This will store the products in-memory; note that this data will be lost when the app restarts
products = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        product_name = request.form.get('productName')
        product_link = request.form.get('productLink')

        # Append the new product to the list
        products.append({'name': product_name, 'link': product_link})

        return redirect(url_for('index'))

    return render_template('index.html', products=products)

if __name__ == '__main__':
    app.run(debug=True)
