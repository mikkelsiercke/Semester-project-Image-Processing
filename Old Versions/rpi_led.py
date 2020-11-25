import time
from rpi_ws281x import *
import argparse
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

# Socket varibales
HOST = '172.20.10.6'
PORT = 65432


# Global variables
RED_COLOR = Color(255, 0, 0)
GREEN_COLOR = Color(0, 255, 0)
NO_COLOR = Color(0, 0, 0)
SIZE_RATIO = 2
index0 = 0
index1 = 0
index2 = 0
index3 = 0
index4 = 0


# Define functions which animate LEDs in various ways.
def colorWipe(strip):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, GREEN_COLOR)
        for j in range(index0, index1):
            strip.setPixelColor(j, RED_COLOR)
        for k in range(index2, index1):
            strip.setPixelColor(k, RED_COLOR)
        for l in range(index2, index3):
            strip.setPixelColor(l, RED_COLOR)
        for m in range(index3, index4):
            strip.setPixelColor(m, RED_COLOR)
    strip.show()


# Main program logic follows:
if __name__ == '__main__':
    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()
    for i in range(0,300):
        strip.setPixelColor(i, Color(0,0,0))
    strip.show()
    print('Press Ctrl-C to quit.')

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()

        with conn:
            while True:
                try:
                    data = conn.recv(1024)
                    data = json.loads(data.decode())
                    centers = data.get("x")
                    centers.sort()

                    if len(centers) == 2:
                        index0 = int(centers[0] / SIZE_RATIO)
                        index1 = int(centers[1] / SIZE_RATIO)
                        colorWipe(strip)
                    elif len(centers) == 3:
                        index0 = int(centers[0] / SIZE_RATIO)
                        index1 = int(centers[1] / SIZE_RATIO)
                        index2 = int(centers[2] / SIZE_RATIO)
                        colorWipe(strip)
                    elif len(centers) == 4:
                        index0 = int(centers[0] / SIZE_RATIO)
                        index1 = int(centers[1] / SIZE_RATIO)
                        index2 = int(centers[2] / SIZE_RATIO)
                        index3 = int(centers[3] / SIZE_RATIO)
                        colorWipe(strip)
                    elif len(centers) == 5:
                        index0 = int(centers[0] / SIZE_RATIO)
                        index1 = int(centers[1] / SIZE_RATIO)
                        index2 = int(centers[2] / SIZE_RATIO)
                        index3 = int(centers[3] / SIZE_RATIO)
                        index4 = int(centers[4] / SIZE_RATIO)
                        colorWipe(strip)
                    else:
                        index0 = 0
                        index1 = 0
                        index2 = 0
                        index3 = 0
                        index4 = 0
                        index5 = 0
                        colorWipe(strip)
                except JSONDecodeError:
                    continue
