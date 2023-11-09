import time, sys
import requests
from fhict_cb_01.custom_telemetrix import CustomTelemetrix
board = CustomTelemetrix()

BUTTON1PIN = 8
BUTTON2PIN = 9
BUZZER = 3
pin_red = 4
pin_green = 5
pin_blue = 6
pin_yellow = 7
trigger = 0
add_time = 0
orderIndex = 0
# Define the URL for your kitchen server
kitchen_server_url = 'http://145.93.148.56:5003/update_status'
orders_endpoint = 'http://145.93.148.56:5003/get_orders'  # URL to fetch orders


def load_orders():
    global orders
    global orderIndex
    orderIndex = None  # Initialize orderIndex to None
    try:
        response = requests.get(orders_endpoint)
        if response.status_code == 200:
            response_data = response.json()
            for order_index, order in enumerate(response_data):
                print(f"Order {order_index}: {order['status']}")
                if order['status'] == 'pending':
                    orderIndex = order_index
                    print(orderIndex)
                    break  # Break out of the loop if a pending order is found
        else:
            print("Failed to load orders from the server")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching orders: {e}")
        orders = []

def safetycheck(safety_break):
    global trigger, order_status_updated
    trigger = safety_break[2]
    
    

def set_timer(time_up):
    global add_time
    add_time = time_up[2]

def update_status_on_kitchen_server(status):
    # Send a POST request to update the status of the first item on the kitchen server
    payload = {'order_index': orderIndex, 'status': status}
    response = requests.post(kitchen_server_url, data=payload)
    
    if response.status_code == 200:
        print(f"Status updated to '{status}' on the kitchen server")
    else:
        print("Failed to update status on the kitchen server")

def setup():
    board.set_pin_mode_digital_input_pullup(BUTTON1PIN, callback=safetycheck)
    board.set_pin_mode_digital_input_pullup(BUTTON2PIN, callback=set_timer)
    board.set_pin_mode_digital_output(BUZZER)
    board.displayOn()
    load_orders()

import time

def loop():
    global order_status_updated
    time.sleep(1)
    board.displayShow('0')
    board.digital_write(pin_green, 1)
    Timer = 0

    while trigger != 0:
        load_orders()
        board.digital_read(BUTTON1PIN)
        time.sleep(0.5)

    board.digital_write(pin_green, 0)
    board.digital_write(pin_blue, 1)

    while add_time != 0:
        board.displayShow(Timer)
        Timer += 1
        minutes = Timer // 60
        seconds = Timer % 60
        display_time = '{:02d}.{:02d}'.format(minutes, seconds)
        board.displayShow(display_time)
        board.digital_read(BUTTON2PIN)
        time.sleep(0.5)

    board.digital_write(pin_yellow, 1)
    board.digital_write(pin_blue, 0)
    print('Press the button to start the timer Sir Luigi')

    while trigger != 0:
        board.digital_read(BUTTON1PIN)
        time.sleep(0.2)

    while Timer != 0 and add_time != 0:
        board.digital_write(pin_red, 1)
        board.digital_write(pin_yellow, 0)
        minutes = Timer // 60
        seconds = Timer % 60
        display_time = '{:02d}.{:02d}'.format(minutes, seconds)
        Timer -= 1

        # Check if Timer is greater than 0, and change the order status to "In Preparation"
        if Timer > 0 :
            update_status_on_kitchen_server('in_preparation')

        time.sleep(1)
        board.displayShow(display_time)

    board.displayShow('0000')
    board.digital_write(pin_green, 1)
    board.digital_write(pin_red, 0)
    board.digital_write(BUZZER, 1)
    time.sleep(5)
    board.digital_write(BUZZER, 0)

    # Timer has reached 0, update the order status to "Done"
    if Timer == 0:
        update_status_on_kitchen_server('done')
    

if __name__ == '__main__':
    setup()
    while True:
        try:
            loop()
        except KeyboardInterrupt:
            print('Bye Bye')
            board.shutdown()
            sys.exit(0)
