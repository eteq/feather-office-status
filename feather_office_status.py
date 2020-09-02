import time

import board
import busio

import adafruit_vcnl4010
import neopixel

import battery_check_feather


green = (0, 255, 0)
yellow = (255, 150, 0)
orange = (255, 50, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
DEFAULT_COLORS = [green, yellow, red]
DEFAULT_CB_FRIENDLY_COLORS = [blue, yellow, red]


def blink_pixels(ntimes, secpertime):
    bi = pixels.brightness
    for i in range(ntimes):
        pixels.brightness = 0
        time.sleep(secpertime/2)
        pixels.brightness = bi
        time.sleep(secpertime/2)


def _setup(neopixels):
    i2c = busio.I2C(board.SCL, board.SDA)
    prox_sensor = adafruit_vcnl4010.VCNL4010(i2c)
    pixels = neopixel.NeoPixel(*neopixels)

    return i2c, prox_sensor, pixels


def main_loop(prox_threshold=3000, brightness=1, colors=DEFAULT_COLORS,
              sampling_time=.02, neopixels=(board.NEOPIXEL, 1),
              do_battery_check=True):
    """
    See REAME.md for description of the keyword arguments.
    """
    i2c, prox_sensor, pixels = _setup(neopixels)
    ncolors = len(colors)

    print("Starting up neopixel at brightness", brightness)
    pixels.brightness = brightness

    i = 0
    color_idx = 0
    last_prox = -1

    # loop forever, updating the color whenever consecutive proximity samples go
    # from "close" to "far"
    while True:
        prox = prox_sensor.proximity
        if last_prox < 0 or last_prox > prox_threshold and prox < prox_threshold:
            color_idx += 1
            print('transitioning color to', color_idx)
            pixels[0] = colors[color_idx % ncolors]
            pixels.brightness = brightness

        if do_battery_check and i % 50 == 0:
            battery_voltage = battery_check_feather.get_battery_voltage()
            if battery_voltage < 3.6:
                if battery_voltage < 3.35:
                    print("battery very low!", battery_voltage)
                    blink_pixels(5, .05)
                else:
                    print("battery low", battery_voltage)
                    blink_pixels(2, .1)
            else:
                print("battery OK", battery_voltage)

        last_prox = prox
        i += 1

        time.sleep(sampling_time)
