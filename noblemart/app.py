from flask import Flask, render_template, redirect, url_for, request, session, jsonify, flash, send_from_directory
from database import *  
from users import *
import os
from werkzeug.utils import secure_filename
from base64 import b64encode
from upc import *

app = Flask(__name__, template_folder='templates', static_folder='static')
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.secret_key = 'noble_mart'

@app.before_request
def initialize_cart():
    if 'cart' not in session:
        session['cart'] = []

@app.route('/api/brands')
def get_brands():
    brands = getBrands()
    brands = list(set(brands))
    return jsonify(brands)

@app.route('/')
def home():
    items = getItems('mens', 'fragrance')
    return render_template('index.html', items = items)

@app.route('/sign-in', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = getUsers([username, password])
        if user and user[2] == 1:
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template('sign-in.html', error='Username or Password is Wrong! Please try again.')
    else:
        return render_template('sign-in.html', error=None)

@app.route('/admin-dashboard', methods=['GET'])
def admin_dashboard():
    return render_template('admin/admin-dashboard.html')

@app.route('/admin-dashboard-orders', methods=['GET'])
def admin_orders():
    pendingItems = get_pending_orders()
    completedItems = get_completed_orders()
    return render_template('admin/orders.html', pendingItems = pendingItems, completedItems = completedItems)

def handle_image_upload(img, hidden_img_url):
    if img:
        filename = secure_filename(img.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        img.save(file_path)
        with open(file_path, "rb") as f:
            file_data = f.read()
        img_data = base64.b64encode(file_data).decode('utf-8')
        os.remove(file_path)
    elif hidden_img_url and hidden_img_url.startswith('http'):
        response = requests.get(hidden_img_url)
        if response.status_code == 200:
            img_data = base64.b64encode(response.content).decode('utf-8')
            short_filename = 'image.jpg'
            img_data = os.path.join(app.config['UPLOAD_FOLDER'], short_filename)
            with open(img_data, 'wb') as f:
                f.write(response.content)
        else:
            raise ValueError("Failed to download image from URL")
    else:
        img_data = None 
    return img_data

@app.route('/admin-dashboard-inventory', methods=['GET', 'POST'])
def admin_inventory():
    if request.method == 'POST':
        brand = request.form.get('brand')
        collection = request.form.get('collection')
        stock = request.form.get('stock')
        name = request.form.get('name')
        price = request.form.get('price')
        img = request.files.get('new_img')
        hidden_img = request.form.get('img')
        img_data = handle_image_upload(img, hidden_img)
        upc_code = request.form.get('upc_code')
        itemType = request.form.get('itemType')
        description = request.form.get('desc')
        size = request.form.get('size')
        addItem([brand, collection, stock, name, price, img_data, 0, itemType, description, upc_code, size])
        return render_template('admin/manage-inventory.html')
    else:
        return render_template('admin/manage-inventory.html')
    
@app.route('/brands<brand>', methods=['GET'])
def brands(brand):
    brand = request.args.get('brand')
    items = getItemByBrand(brand)
    return render_template('items.html',title = brand + " Items", items = items)

@app.route('/mens-collection-fragrances', methods=['GET'])
def mens_fragrances():
    items = getItems('mens', 'fragrance')
    return render_template('items.html',title = "Men's Fragrances Collection", items = items)

@app.route('/mens-collection-deodorants', methods=['GET'])
def mens_deodorants():
    items = getItems('mens', 'deodorant')
    return render_template('items.html',title = "Men's Deodorant Collection", items = items)

@app.route('/mens-collection-after-shave', methods=['GET'])
def mens_afterShave():
    items = getItems('mens', 'after shave')
    return render_template('items.html',title = "Men's After Shave Collection", items = items)

@app.route('/mens-collection-gift-sets', methods=['GET'])
def mens_giftSets():
    items = getItems('mens', 'gift set')
    return render_template('items.html',title = "Men's Gift Set Collection", items = items)

@app.route('/womens-collection-fragrances', methods=['GET'])
def womens_fragrances():
    items = getItems('womens', 'fragrance')
    return render_template('items.html', title = "Women's Fragrances", items = items)

@app.route('/womens-collection-gift-sets', methods=['GET'])
def womens_giftSets():
    items = getItems('womens', 'gift set')
    return render_template('items.html',title = "Women's Gift Set Collection", items = items)

@app.route('/womens-collection-deodorants', methods=['GET'])
def womens_deodorants():
    items = getItems('womens', 'deodorant')
    return render_template('items.html',title = "Women's Deodorant Collection", items = items)

@app.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    id = request.form.get('item_id')
    cart = session.get('cart', [])
    for item in cart:
        if int(item['id']) == int(id):
            item['quantity'] += 1  
            session['cart'] = cart
            return redirect(url_for('cart'))
    new_item = getItemByID(id)
    new_item['quantity'] = 1
    cart.append(new_item)
    session['cart'] = cart  
    return redirect(url_for('cart'))

@app.route('/remove-from-cart/<item_id>', methods=['POST'])
def remove_from_cart(item_id):
    item_id = int(item_id)  
    cart = session.get('cart', [])
    updated_cart = [item for item in cart if int(item['id']) != item_id]
    session['cart'] = updated_cart
    session.modified = True  
    return redirect(url_for('cart'))

@app.route('/clear-cart', methods=['POST'])
def clear_cart():
    session['cart'] = [] 
    session.modified = True 
    return redirect(url_for('cart'))

@app.route('/admin-dashboard-upc-code-lookup', methods=['GET', 'POST'])
def upc_lookup():
    if request.method == 'POST':
        upc_code = request.form.get('upc')
        print(upc_code)
        data = retrieveItemData(upc_code)
        if data is not None:
            brand = data[1]
            name = data[0]
            img = data[4]
            desc = data[2]
            return render_template('admin/manage-inventory.html', name = name, brand = brand, img = img, desc = desc, upc_code = upc_code)
        else:
            return render_template('admin/manage-inventory.html')
    else:
       return render_template('admin/upc-lookup.html')

@app.template_filter('b64encode')
def b64encode_filter(data):
    return base64.b64encode(data).decode('utf-8')

@app.route('/cart', methods=['GET'])
def cart():
    subtotal = 0.00
    for item in session.get('cart', []):
        subtotal += item['price'] * item['quantity'] 
    tax = subtotal * 0.0675
    total = subtotal + tax
    return render_template('cart.html', items=session.get('cart', []), subtotal=subtotal, tax=tax, total=total)


@app.route('/place-order', methods=['POST'])
def place_order():
    email = request.form.get('email')
    firstName = request.form.get('firstName')
    lastName = request.form.get('lastName')
    address = request.form.get('address')
    apartment = request.form.get('apartment')
    city = request.form.get('city')
    country = request.form.get('country')
    state = request.form.get('state')
    phone = request.form.get('phone')
    shipping = request.form.get('delivery')
    shippingData = [email, firstName, lastName, address, apartment, city, state, country, phone, shipping]
    try:
        for item in session['cart']:
            orderData = [item['id'], item['quantity'], item['price']]
            item_ordered(shippingData, orderData)
        session['cart'] = []
        return render_template('checkout.html', success=True)
    except ValueError as e:
        flash(str(e), 'error')
        return redirect(url_for('cart'))

@app.route('/admin-complete-order', methods=['POST'])
def order_complete():
    order_item_id = request.json.get('item_id')
    complete_order(order_item_id)
    return jsonify({"status": "success", "message": f"Order {order_item_id} marked as complete!"}), 200

@app.route('/update_item/<int:item_id>', methods=['POST'])
def update_item(item_id):
    data = request.json
    price = data.get('price')
    quantity = data.get('quantity')
    updateInventory(price, quantity, item_id)
    return jsonify(success=True)

@app.route('/delete_item/<int:item_id>', methods=['POST'])
def delete_item(item_id):
    deleteItemFromInventory(item_id)
    return jsonify(success=True)

@app.route('/admin-view-inventory', methods=['GET'])
def view_inventory():
    inventory = getInventory()
    print(len(inventory))
    return render_template('admin/inventory.html', inventory = inventory)

@app.route('/uploads/<path:filename>')
def uploads(filename):
    return send_from_directory('uploads', filename)

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/about-us')
def about_us():
    return render_template('about-us.html')

@app.route('/delivery')
def delivery():
    return render_template('delivery.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)


