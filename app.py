import time
import sys
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

# Define the URL for your kitchen server
kitchen_server_url = 'http://10.0.0.191:5003'

def safetycheck(safety_break):
    global trigger
    trigger = safety_break[2]

def set_timer(time_up):
    global add_time
    add_time = time_up[2]

def update_status_on_kitchen_server(order_index, status):
    # Send a POST request to update the status of an order on the kitchen server
    payload = {'order_index': order_index, 'status': status}
    response = requests.post(f'{kitchen_server_url}/update_status', data=payload)

def fetch_orders_from_server():
    # Fetch orders from the server (use the endpoint defined in your Flask app)
    response = requests.get(f'{kitchen_server_url}/get_orders')
    if response.status_code == 200:
        orders = response.json()
        return orders
    else:
        print("Failed to fetch orders from the server")
        return []

def setup():
    board.set_pin_mode_digital_input_pullup(BUTTON1PIN, callback=safetycheck)
    board.set_pin_mode_digital_input_pullup(BUTTON2PIN, callback=set_timer)
    board.set_pin_mode_digital_output(BUZZER)
    board.displayOn()

def loop():
    time.sleep(1)
    board.displayShow('0')
    board.digital_write(pin_green, 1)
    Timer = 0

    while trigger != 0:
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

    orders = fetch_orders_from_server()

    if not orders:
        print("No orders available.")
    else:
        first_order = orders[0]  # Assuming orders is a list of dictionaries
        order_index = first_order['order_index']

        while Timer != 0 and add_time != 0:
            board.digital_write(pin_red, 1)
            board.digital_write(pin_yellow, 0)
            minutes = Timer // 60
            seconds = Timer % 60
            display_time = '{:02d}.{:02d}'.format(minutes, seconds)
            Timer -= 1

            # Check if Timer is greater than 0, and change the order status to "In Preparation"
            if Timer > 0:
                update_status_on_kitchen_server(order_index, 'in_preparation')

            time.sleep(1)
            board.displayShow(display_time)

        board.displayShow('0000')
        board.digital_write(pin_green, 1)
        board.digital_write(pin_red, 0)
        board.digital_write(BUZZER, 1)
        time.sleep(5)
        board.digital_write(BUZZER, 0)

        # Change the order status to "Done" when Timer reaches 0
        update_status_on_kitchen_server(order_index, 'done')

if __name__ == '__main__':
    setup()
    while True:
        try:
            loop()
        except KeyboardInterrupt:
            print('Bye Bye')
            board.shutdown()
            sys.exit(0)
