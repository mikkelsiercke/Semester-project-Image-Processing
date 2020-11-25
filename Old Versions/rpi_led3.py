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
distance_pixels = 180

index0_1 = 0
index1_1 = 0

index0_2 = 0
index1_2 = 0

index0_3 = 0
index1_3 = 0

# Define functions which animate LEDs in various ways.
def colorWipe(strip):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, GREEN_COLOR)
    strip.show()

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(255, 0, 0)
    elif pos < 170:
        pos -= 85
        return Color(255, 50, 0)
        #return Color(0, 255, 255 - pos * 3)
    else:
        pos -= 170
        return Color(255, 0, 0)
        #return Color(0, 255, 27)

def animation(strip, wait_ms=1, range_begin=0, range_end=-1, iteration_step=-1):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    if range_end == 1:
        range_end = strip.numPixels()

    j = iteration_step

    for i in range(range_begin, range_end):
        strip.setPixelColor(i, wheel((int(i * 256 / range_end-range_begin) + j) & 255))

    strip.show()
    #time.sleep(wait_ms/1000.0)

def animation1(strip, wait_ms=1, range_begin=0, range_end=-1, iteration_step=-1):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    if range_end == 1:
        range_end = strip.numPixels()

    j = iteration_step

    pixel_to_change = iteration_step % (range_end - range_begin) + range_begin

    if pixel_to_change - range_begin == 0:
        for i in range(range_begin, range_end):
            strip.setPixelColor(i, Color(0, 0, 255))
        strip.show()
        time.sleep(wait_ms/1000)
        for i in range(range_begin, range_end):
            strip.setPixelColor(i, Color(255, 0, 0))
        strip.show()
    #time.sleep(wait_ms/1000.0)

# Main program logic follows:
if __name__ == '__main__':
    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0, 0, 0))
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

                    for i in range(256):
                        if len(centers) == 2:
                            if abs(centers[1] - centers[0]) < distance_pixels:
                                index0_1 = int(centers[0] / SIZE_RATIO)
                                index1_1 = int(centers[1] / SIZE_RATIO)
                                animation1(strip, range_begin=index0_1, range_end=index1_1, iteration_step=i)
                            else:
                                index0_1 = 0
                                index1_1 = 0
                                colorWipe(strip)
                        elif len(centers) == 3:
                            if abs(centers[1] - centers[0]) < distance_pixels:
                                index0_1 = int(centers[0] / SIZE_RATIO)
                                index1_1 = int(centers[1] / SIZE_RATIO)
                                animation1(strip, range_begin=index0_1, range_end=index1_1, iteration_step=i)
                            else:
                                index0_1 = 0
                                index1_1 = 0
                                colorWipe(strip)
                            if abs(centers[2] - centers[1]) < distance_pixels:
                                index0_2 = int(centers[1] / SIZE_RATIO)
                                index1_2 = int(centers[2] / SIZE_RATIO)
                                animation1(strip, range_begin=index0_2, range_end=index1_2, iteration_step=i)
                            else:
                                index0_2 = 0
                                index1_2 = 0
                                colorWipe(strip)
                        elif len(centers) == 4:
                            if abs(centers[1] - centers[0]) < distance_pixels:
                                index0_1 = int(centers[0] / SIZE_RATIO)
                                index1_1 = int(centers[1] / SIZE_RATIO)
                                animation1(strip, range_begin=index0_1, range_end=index1_1, iteration_step=i)
                            else:
                                index0_1 = 0
                                index1_1 = 0
                                colorWipe(strip)
                            if abs(centers[2] - centers[1]) < distance_pixels:
                                index0_2 = int(centers[1] / SIZE_RATIO)
                                index1_2 = int(centers[2] / SIZE_RATIO)
                                animation1(strip, range_begin=index0_2, range_end=index1_3, iteration_step=i)
                            else:
                                index0_2 = 0
                                index1_2 = 0
                                colorWipe(strip)
                            if abs(centers[3] - centers[2]) < distance_pixels:
                                index0_3 = int(centers[2] / SIZE_RATIO)
                                index1_3 = int(centers[3] / SIZE_RATIO)
                                animation1(strip, range_begin=index0_3, range_end=index1_3, iteration_step=i)
                            else:
                                index0_3 = 0
                                index1_3 = 0
                                colorWipe(strip)
                        else:
                            index0_1 = 0
                            index1_1 = 0
                            index0_2 = 0
                            index1_2 = 0
                            index0_3 = 0
                            index1_3 = 0
                            colorWipe(strip)
                except JSONDecodeError:
                    continue
