# feather-office-status

Do you share a (home) office with someone who you like to talk to?  Do you your
day getting stuck in chit-chat? And are you the geeky sort who might struggle to
say "Sorry, I need to get some work done now?"  If so, this might be for you!

This DIY project results in a little device you can set on your office desk or
wall with a nice bright light that indicates to those you share space with
whether you are available to chat.


## Hardware Setup

This project has two hardware requirements:

* A CircuitPython-compatible microcontroller board with NeoPixels.  I used the
  [Adafruit Feather M4 Express](https://www.adafruit.com/product/3857), but this
  should be just as compatible with the cheaper
  [Adafruit Feather M0 Express](https://www.adafruit.com/product/3403). Or you
  can probably use just about any CircuitPython-compatible board if you connect
  your own separate [NeoPixels](https://www.adafruit.com/category/168).
* A [VCNL4010 Proximity sensor](https://www.adafruit.com/product/466).

With those components the only wiring necessary should be connecting the
VCNL4010 to your microcontroller board - See for example
[this diagram on Learn Adafruit](https://learn.adafruit.com/using-vcnl4010-proximity-sensor/python-circuitpython#circuitpython-microcontroller-wiring-2997895-1).

If you're using your own NeoPixel you'll also need to [connect those to the
microcontroller board](https://learn.adafruit.com/adafruit-neopixel-uberguide).

Optionally, if you want more freedom, you can
[connect a battery](https://learn.adafruit.com/adafruit-feather-m4-express-atsamd51/power-management).
If so and you are using a Feather this project will check the battery level and
warn when you need to charge by blinking.


## Software Dependencies

You will need the following software:

* [Adafruit CircuitPython](https://github.com/adafruit/circuitpython)

Adafruit provides plenty of tutorials for getting started with CircuitPython.
You'll probably want to use the resources for your particular board like
[this one for the M4 Express](https://learn.adafruit.com/adafruit-feather-m4-express-atsamd51/circuitpython).

* [Adafruit CircuitPython NeoPixel](https://github.com/adafruit/Adafruit_CircuitPython_NeoPixel)
* [Adafruit_CircuitPython_VCNL4010](https://github.com/adafruit/Adafruit_CircuitPython_VCNL4010)
* [Adafruit CircuitPython BusDevice](https://github.com/adafruit/Adafruit_CircuitPython_BusDevice)

Note that the last three are most easily obtained as releases via the
[Adafruit CircuitPython Library Bundle](https://github.com/adafruit/Adafruit_CircuitPython_Bundle)
 - see the documentation there for more details.

## Software Setup & Usage

To get this working, all that's necessary is:

1. Connect your board via USB
2. Copy over the two .py files in this repo to the CIRCUITPY drive that appears
3. Modify or create a `main.py`  that has the following content:

```
import feather_office_status

feather_office_status.main_loop()
```

And that's it! If you want to configure the behavior, though, see below.

Once it's reset you should see your NeoPixel in bright green.  Wave your hand
in front of the proximity sensor and it should cycle through yellow, red, and
then back to green.

### Default Color Meaning

You are free to use whatever meaning for the colors you like, and can customize
the colors as you prefer as described below. However, if you use the default
colors, here's my recommended interpretation:

* Green / Blue: "I am working, but don't mind being interrupted for idle chat."
* Yellow: "I am busy and don't want to be interrupted unless it's something
  timely or otherwise kinda important."
* Red: "Please don't interrupt me unless the building is burning down."

### Options

The easiest way to modify behavior is via the arguments to the `main_loop`
function. These include the following:

* `prox_threshold`: this sets the distance threshold at which the color change
  gets triggered - a larger number here means you have to be closer to trigger
  it number means more sensitive, and a smaller number makes it less so.
  Although note that at some point (for my office and device this was around
  2000), you might find it's *always* getting triggered and therefore useless.
* `brightness`: A number between 0 and 1 indicating how bright the LED should
  be (where 1 is the maximum brightness the LED can do and 0 is off).
* `colors`: The set of colors to use as a list of RGB tuples. See
  ``feather_office_status.py`` for a few hand-calibrated colors that are
  known-good on the M4 Express.
* `sampling_time`: the time (in seconds) between proximity tests. Turn down if
  you find your hand isn't getting recognized because you wave it too quickly
  (at the expense of battery life).
* `neopixels`: Arguments to be passed into the `neopixel.NeoPixel` class
  initializer.  This is only needed if you're using a separate NeoPixel instead
  of the built-in one.  For example, if you have a string of 5 NeoPixels
  connected to pin 12 on your feather, you'd do ``(board.D12, 5)``.
* `do_battery_check`: Set this to False if you're on a board that isn't
  compatible with the battery checker.


As an example, if your office is dimly late, and think your officemate might be
colorblind (and you should find out if you're not sure... around 5% of people
are at some level), you can use the following to turn down the brightness and
switch to a more colorblind-friendly scheme:

```
import feather_office_status

feather_office_status.main_loop(brightness=.2, colors=feather_office_status.DEFAULT_CB_FRIENDLY_COLORS)
```


## Contributions

This is an open source project so any contributions or suggestions are welcome!
Feel free to use the Github issue tracker or make Pull Requests.
