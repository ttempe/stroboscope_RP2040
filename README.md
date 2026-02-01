# stroboscope_RP2040
A MicroPython-based stroboscope driver, using PIO

Runs on the RP2040 series of microcontrollers. 
Outputs the strobe signal on a GPIO, to be re-used as eg: a PWM signal on LED drivers.
This repository contains the MicroPython code.

In addition to the Strobe pin, the code drives:
* a continuous encoder (infinite rotary button) for coarse frequency setting
* a potentiometer (on an analog pin) for fine frequency setting
* an SSD1306 OLED display, for displaying the frequency

Thanks to PIO's deterministic timing, fast execution and direct access to the GPIO, you get:
* speed: goes as fast as your lights will ever go (or the MHz-level, if you ever care to go there).
* very fine, continuous adjustment, without losing sync

