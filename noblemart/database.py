import sqlite3
import base64
import os
from uuid import uuid4

conn = sqlite3.connect('noblemart.db')
cursor = conn.cursor()  
def createTables():
    conn = sqlite3.connect('noblemart.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS inventory(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        brand VARCHAR(255) NOT NULL,
        collection VARCHAR(255) NOT NULL,
        stock INTEGER NOT NULL,
        name VARCHAR(255) NOT NULL,
        price REAL NOT NULL,
        img BLOB NOT NULL,
        qtySold INTEGER NOT NULL,
        item_type VARCHAR(255) NOT NULL,
        description VARCHAR(255) NOT NULL,
        upc_code INTEGER NOT NULL, 
        size VARCHAR(255) NOT NULL
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS orders(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email VARCHAR(255) NOT NULL,
            firstName VARCHAR(255) NOT NULL,
            lastName VARCHAR(255) NOT NULL,
            address VARCHAR(255) NOT NULL,
            apartment VARCHAR(255) NOT NULL,
            city VARCHAR(255) NOT NULL,
            state VARCHAR(255) NOT NULL,
            country VARCHAR(255) NOT NULL,
            phone VARCHAR(255) NOT NULL,
            delivery VARCHAR(255) NOT NULL
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS order_items(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            item_id INTEGER NOT NULL,
            qty INTEGER NOT NULL,
            price REAL NOT NULL,
            status VARCHAR(255) NOT NULL,
            order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
            FOREIGN KEY (item_id) REFERENCES inventory(id) ON DELETE CASCADE
    )''')
    conn.commit()
    conn.close

def addItem(data): 
    conn = sqlite3.connect('noblemart.db')
    cursor = conn.cursor()      
    data[5] = convertToBinaryData(data[5])
    cursor.execute('''INSERT INTO inventory (brand, collection, stock, name, price, img, qtySold, item_type, description, upc_code, size) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', data)
    conn.commit()
    conn.close()

def getItems(collection, type):
    conn = sqlite3.connect('noblemart.db')
    cursor = conn.cursor()   
    cursor.execute("SELECT * FROM inventory WHERE collection = ? AND item_type = ?", (collection, type,))
    items = cursor.fetchall()
    conn.close()
    return items

def getItemByBrand(brand):
    conn = sqlite3.connect('noblemart.db')
    cursor = conn.cursor()   
    cursor.execute("SELECT * FROM inventory WHERE brand = ?", (brand,))
    items = cursor.fetchall()
    conn.close()
    return items

def getItemByID(item_id):
    conn = sqlite3.connect('noblemart.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM inventory WHERE id = ?", (item_id,))
    item = cursor.fetchone()
    conn.close()
    filename = f"{uuid4()}.png"
    file_path = os.path.join('uploads', filename)
    writeTofile(item[6], file_path)
    item = {
        'id': item[0],
        'brand': item[1],
        'collection': item[2],
        'stock': item[3],
        'name': item[4],
        'price': item[5],
        'img': filename, 
        'qtySold': item[7],
        'item_type': item[8],
        'description': item[9],
        'upc_code': item[10],
        'size': item[11]
    }
    return item

def getSizes(brand, name, collection):
    conn = sqlite3.connect('noblemart.db')
    cursor = conn.cursor()   
    cursor.execute("SELECT * FROM inventory WHERE brand = ? AND name = ? AND collection = ?",(brand, name, collection))
    items = cursor.fetchall()
    conn.close()
    return items
    
def item_ordered(shippingData, orderData):
    conn = sqlite3.connect('noblemart.db')
    cursor = conn.cursor()
    cursor.execute("SELECT qtySold, stock FROM inventory WHERE id = ?", (orderData[0],))
    result = cursor.fetchone()
    if result:
        current_qty_sold, current_stock = result
        if current_stock < orderData[1]:
            raise ValueError(f"Insufficient stock for item ID {orderData[0]}")
        new_qty_sold = current_qty_sold + orderData[1]
        new_stock = current_stock - orderData[1]
        cursor.execute("UPDATE inventory SET qtySold = ?, stock = ? WHERE id = ?", (new_qty_sold, new_stock, orderData[0]))
        conn.commit()
    else:
        raise ValueError(f"Item ID {orderData[0]} not found in inventory.")
    cursor.execute('''SELECT id FROM orders WHERE email = ? AND firstName = ? AND lastName = ? 
                      AND address = ? AND apartment = ? AND city = ? AND state = ? 
                      AND country = ? AND phone = ? AND delivery = ?''', shippingData)
    existing_record = cursor.fetchone()
    if existing_record:
        order_id = existing_record[0]
    else:
        cursor.execute('''INSERT INTO orders (email, firstName, lastName, address, apartment, city, state, country, phone, delivery) 
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', shippingData)
        conn.commit()
        order_id = cursor.lastrowid
    orderData.insert(0, order_id)
    orderData.append("Pending")
    cursor.execute('''INSERT INTO order_items (order_id, item_id, qty, price, status) VALUES (?, ?, ?, ?, ?)''', orderData)
    conn.commit()
    conn.close()

def get_pending_orders():
    conn = sqlite3.connect('noblemart.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT order_items.id, order_items.order_id, order_items.item_id, order_items.qty,
               order_items.price, order_items.status, order_items.order_date,
               orders.email, orders.firstName, orders.lastName, orders.address,
               orders.apartment, orders.city, orders.state, orders.country, orders.phone,
               inventory.brand, inventory.img, inventory.description, inventory.name
        FROM order_items
        JOIN orders ON order_items.order_id = orders.id
        JOIN inventory ON order_items.item_id = inventory.id
        WHERE order_items.status = ?
    ''', ("Pending",))
    items = cursor.fetchall()
    conn.close()
    pending_orders = []
    for item in items:
        pending_orders.append({
            'order_item_id': item[0],
            'order_id': item[1],
            'item_id': item[2],
            'quantity': item[3],
            'price': item[4],
            'status': item[5],
            'order_date': item[6],
            'email': item[7],
            'first_name': item[8],
            'last_name': item[9],
            'address': item[10],
            'apartment': item[11],
            'city': item[12],
            'state': item[13],
            'country': item[14],
            'phone': item[15],
            'brand': item[16],
            'img': item[17],        
            'description': item[18],
            'name': item[19]
        })
    return pending_orders
     
def get_completed_orders():
    conn = sqlite3.connect('noblemart.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT order_items.id, order_items.order_id, order_items.item_id, order_items.qty,
               order_items.price, order_items.status, order_items.order_date,
               orders.email, orders.firstName, orders.lastName, orders.address,
               orders.apartment, orders.city, orders.state, orders.country, orders.phone,
               inventory.brand, inventory.img, inventory.description, inventory.name
        FROM order_items
        JOIN orders ON order_items.order_id = orders.id
        JOIN inventory ON order_items.item_id = inventory.id
        WHERE order_items.status = ?
    ''', ("Completed",))
    items = cursor.fetchall()
    conn.close()
    pending_orders = []
    for item in items:
        pending_orders.append({
            'order_item_id': item[0],
            'order_id': item[1],
            'item_id': item[2],
            'quantity': item[3],
            'price': item[4],
            'status': item[5],
            'order_date': item[6],
            'email': item[7],
            'first_name': item[8],
            'last_name': item[9],
            'address': item[10],
            'apartment': item[11],
            'city': item[12],
            'state': item[13],
            'country': item[14],
            'phone': item[15],
            'brand': item[16],
            'img': item[17],        
            'description': item[18],
            'name': item[19]
        })
    return pending_orders

def complete_order(order_id):
    conn = sqlite3.connect('noblemart.db')
    cursor = conn.cursor()   
    cursor.execute("UPDATE order_items SET status = ? WHERE id = ?", ("Completed", order_id))
    conn.commit()
    conn.close()
    
def convertToBinaryData(filename):
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData

def writeTofile(data, filename):
    with open(filename, 'wb') as file:
        file.write(data)
    print("Stored blob data into: ", filename, "\n")

def getBrands():
    conn = sqlite3.connect('noblemart.db')
    cursor = conn.cursor()   
    cursor.execute("SELECT brand FROM inventory")
    brands = cursor.fetchall()
    conn.close()
    return brands

def getInventory():
    conn = sqlite3.connect('noblemart.db')
    conn.row_factory = sqlite3.Row 
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM inventory")
    inventory = cursor.fetchall()
    conn.close()
    return inventory

def updateInventory(price, quantity, item_id):
    conn = sqlite3.connect('noblemart.db')
    cursor = conn.cursor()   
    cursor.execute("UPDATE inventory SET price = ?, stock = ? WHERE id = ?", (price, quantity, item_id))
    conn.commit()
    conn.close()

def deleteItemFromInventory(item_id):
    conn = sqlite3.connect('noblemart.db')
    cursor = conn.cursor() 
    cursor.execute("DELETE FROM inventory WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()
