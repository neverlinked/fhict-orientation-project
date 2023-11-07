import serial
import time
import pyfirmata

# Set the port where your Arduino is connected
# On Windows, it should look like 'COM3' or similar
port = 'COM3'  # Change this to your port

try:
    # Open a serial connection to the Arduino
    ser = serial.Serial(port, baudrate=57600, timeout=1)

    print(ser.readline().decode('utf-8')) 

    # Define pin for the speaker
    speaker_pin = 9  # Change this to the pin where your speaker is connected

    # Define the countdown time in seconds for the oven
    oven_countdown_time = 5  # 5 minutes for demonstration, change as needed

    # Function to start the oven countdown with music
    def start_oven_countdown_with_music(countdown_time):
        print("Oven countdown with music started!")

        # Send a message to the Arduino to start the countdown with music
        ser.write(b'START_WITH_MUSIC\n')

        for i in range(countdown_time, 0, -1):
            print("Time remaining:", i)
            time.sleep(1)

        # Send a message to the Arduino to stop the music
        ser.write(b'STOP_MUSIC\n')

        print("Oven countdown with music complete!")

        # Close the serial connection
        ser.close()

    # Start the oven countdown with music
    start_oven_countdown_with_music(oven_countdown_time)

except Exception as e:
    print(f"An error occurred: {e}")

arduino_port = 'COM3'  # Update with your port
baud_rate = 9600

try:
    # Open a serial connection to the Arduino
    ser = serial.Serial(arduino_port, baudrate=baud_rate, timeout=1)

    # Define pin for the buzzer
    buzzer_pin = 9  # Change this to the pin where your buzzer is connected

    while True:
        # Send 1KHz sound signal for 1 second
        ser.write(b'START\n')
        time.sleep(1)

        # Stop sound for 1 second
        ser.write(b'STOP\n')
        time.sleep(1)

except KeyboardInterrupt:
    # Clean up when the program is interrupted
    ser.close()
    