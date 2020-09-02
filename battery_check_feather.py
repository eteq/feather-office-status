import time
import board
import analogio

__all__ = ['get_battery_voltage']

def get_battery_voltage(battery_pin='guess'):
    if battery_pin == 'guess':
        if hasattr(board, 'BATTERY'):
            battery_pin = board.BATTERY
        elif hasattr(board, 'VOLTAGE_MONITOR'):
            battery_pin = board.VOLTAGE_MONITOR
        else:
            battery_pin = None
    a = analogio.AnalogIn(battery_pin)
    try:
        return a.reference_voltage * a.value * 2**-15  # 16-bit, then multiply by 2
    finally:
        a.deinit()

def led_voltage_loop(pin, led_neopixel=True, brightness=1, waittime=.3):
    if led_neopixel:
        import neopixel
        led = neopixel.NeoPixel(pin, 1, brightness=brightness)
    else:
        import adafruit_dotstar
        led = adafruit_dotstar.DotStar(pin[0], pin[1], 1, brightness=brightness)

    while True:
        voltage = get_battery_voltage()
        print("Battery Voltage:", voltage)
        vs = repr(int(voltage*100))
        for i in range(3):
            pxs = [0, 0, 0]
            for _ in range(int(vs[i])):
                pxs[i] = 255
                led.fill(pxs)
                time.sleep(waittime)
                pxs[i] = 0
                led.fill(pxs)
                time.sleep(waittime)
        time.sleep(waittime*3)
