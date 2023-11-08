from flask import Flask, render_template, request, redirect, url_for, jsonify
from collections import deque

app = Flask(__name__)

orders = deque()
order_index = 0  

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/website_main')
def website_main():
    return render_template('website_main.html')

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/cashier')
def cashier():
    return render_template('cashier.html', orders=orders)

@app.route('/kitchen')
def kitchen():
    return render_template('kitchen.html', orders=orders)

@app.route('/add_order', methods=['POST'])
def add_order():
    global order_index  
    table_number = request.form['table_number']
    item1 = int(request.form['Margherita'])
    item2 = int(request.form['Pepperoni'])
    item3 = int(request.form['Marinara'])
    item4 = int(request.form['Meatlovers'])
    item5 = int(request.form['Coca Cola'])
    item6 = int(request.form['Water Bottle'])
    total_price = item1 * 12.99 + item2 * 14.99 + item3 * 10.99 + item4 * 19.99 + item5 * 3.99 + item6 * 1.99
    
    order = {
        'table_number': table_number,
        'items': {
            'Margherita': item1,
            'Pepperoni': item2,
            'Marinara': item3,
            'Meatlovers': item4,
            'Coca Cola': item5,
            'Water Bottle': item6
        },
        'status': 'pending',
        'total_price': total_price
    }
    
    orders.append(order)
    order_index += 1  
    return redirect(url_for('cashier'))

@app.route('/send_order', methods=['POST'])
def send_order():
    global order_index  
    table_number = request.form['table_number']
    item1 = int(request.form['Margherita'])
    item2 = int(request.form['Pepperoni'])
    item3 = int(request.form['Marinara'])
    item4 = int(request.form['Meatlovers'])
    item5 = int(request.form['Coca Cola'])
    item6 = int(request.form['Water Bottle'])
    total_price = item1 * 12.99 + item2 * 14.99 + item3 * 10.99 + item4 * 19.99 + item5 * 3.99 + item6 * 1.99
    
    order = {
        'table_number': table_number,
        'items': {
            'Margherita': item1,
            'Pepperoni': item2,
            'Marinara': item3,
            'Meatlovers': item4,
            'Coca Cola': item5,
            'Water Bottle': item6
        },
        'status': 'pending',
        'total_price': total_price
    }
    
    orders.append(order)
    order_index += 1  
    return redirect(url_for('cart'))

@app.route('/update_status', methods=['POST'])
def update_status():
    order_index = int(request.form['order_index'])
    
    if 0 <= order_index < len(orders):
        current_status = orders[order_index]['status']
        
        
        if current_status == 'pending':
            orders[order_index]['status'] = 'preparation'
        elif current_status == 'preparation':
            orders[order_index]['status'] = 'done'
    
    return redirect(url_for('kitchen'))

@app.route('/remove_order', methods=['POST'])
def remove_order():
    order_index = int(request.form['order_index'])
    if 0 <= order_index < len(orders):
        orders.remove(orders[order_index])
    
    return redirect(url_for('cashier'))

@app.route('/get_orders', methods=['GET'])
def get_orders():
    return jsonify(list(orders))

if __name__ == '__main__':
    app.run(debug=True, port=5003)
