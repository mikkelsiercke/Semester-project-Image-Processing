import time
from rpi_ws281x import *
import socket
import json
from json.decoder import JSONDecodeError

# LED strip configuration:
LED_COUNT = 300  # Number of LED pixels.
LED_PIN = 18  # GPIO pin connected to the pixels (18 uses PWM!).
# LED_PIN = 10 # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10  # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 10  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0  # set to '1' for GPIOs 13, 19, 41, 45 or 53

# Socket variables
HOST = '172.20.10.6'
PORT = 65432

# Global variables
RED_COLOR = Color(255, 0, 0)
GREEN_COLOR = Color(0, 255, 0)
NO_COLOR = Color(0, 0, 0)

index0_1 = 0
index1_1 = 0

index0_2 = 0
index1_2 = 0

index0_3 = 0
index1_3 = 0


def colorWipe(strip):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, GREEN_COLOR)
        for j in range(index0_1, index1_1):
            strip.setPixelColor(j, RED_COLOR)
        for k in range(index0_2, index1_2):
            strip.setPixelColor(k, RED_COLOR)
        for l in range(index0_3, index1_3):
            strip.setPixelColor(l, RED_COLOR)
    strip.show()
    time.sleep(0.1)
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, GREEN_COLOR)
        for j in range(index0_1, index1_1):
            strip.setPixelColor(j, GREEN_COLOR)
        for k in range(index0_2, index1_2):
            strip.setPixelColor(k, GREEN_COLOR)
        for l in range(index0_3, index1_3):
            strip.setPixelColor(l, GREEN_COLOR)
    strip.show()
    time.sleep(0.1)


# Main program logic follows:
if __name__ == '__main__':
    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Initialize the library (must be called once before other functions).
    strip.begin()

    # Turn off all LEDs when program starts
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, NO_COLOR)
    strip.show()

    print('Press Ctrl-C to quit.')

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()

        with conn:
            while True:
                try:
                    # Receive JSON data and decode
                    data = conn.recv(1024)
                    data = json.loads(data.decode())

                    # Assign decoded data to index variables
                    index0_1 = data.get("index0_1")
                    index1_1 = data.get("index1_1")
                    index0_2 = data.get("index0_2")
                    index1_2 = data.get("index1_2")
                    index0_3 = data.get("index0_3")
                    index1_3 = data.get("index1_3")

                    # Calls function to display colors on LED-strip
                    colorWipe(strip)

                # Continue while-loop if decode error happens
                except JSONDecodeError:
                    continue
