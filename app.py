
from flask import Flask
from flask import render_template
from flask import request, redirect

import random


app = Flask(__name__)
currentQueue = []


@app.route('/')
def show_and_register():
    return render_template('cashier.html',
                            pizzas = currentQueue)


@app.route('/register', methods = ['POST'])
def add_volunteer():
    type = request.form['type']
    Qty = request.form['Qty']

    newPizza = (type, Qty)
    currentQueue.append(newPizza)

    return redirect('/')


@app.route('/take', methods = ['GET'])
def send_away_volunteer():

    if len(currentQueue) == 0:
        return {}

    pizza = random.choice(currentQueue)
    currentQueue.remove(pizza)

    (type, Qty) = pizza
    return { 'sent_name': type, 'sent_age': Qty }

