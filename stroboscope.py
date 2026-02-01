from machine import Pin, ADC
import machine
from math import pow
from time import sleep_ms
from rp2 import PIO, StateMachine, asm_pio
import gc
from disp import display_freq
import neopixel
import encoder
import potentiometer

# TODO:
# * Set a duty cycle, not a duration

sleep_ms(1000)
machine.freq(125_000_000) #Should be default ; to ensure correct PIO frequency
max_freq = 10_000_000
#GPIO definition
button = Pin(6, Pin.IN, Pin.PULL_UP)
led    = Pin(25, Pin.OUT)
np     = neopixel.NeoPixel(Pin(16), 1) #np[0]=(0,0,0) ; np.write()
p      = potentiometer.Potentiometer(ADC(26))

pin_s = Pin(3, Pin.OUT) #stroboscope output
pin_a = Pin(4, Pin.IN)  #stroboscope trigger (internal usage: PIO1 triggers PIO0)
sm0 = None
sm1 = None
    
@asm_pio(set_init=PIO.OUT_LOW)
def pulse():
    """Turns on the light for the duration of the duty cycle.
    Reads the duration of the pulse from FIFO once when executed"""
    pull()               # Read the "high" delay from the FIFO (once)
    mov(x, osr)          # store it to X

    label("loop")
    wait(1, pin, 0)      # wait for the trigger (1) from PIO1 on GPIO4   
    set(pins, 1)         # set GPIO3 on (turn on the light)
    mov(y, x)

    label("delay")       # delay
    jmp(y_dec, "delay")

    set(pins, 0)         # turn off
    jmp("loop")

@asm_pio(set_init=PIO.OUT_LOW)
def delay():
    "Sends one pulse per cycle on GPIO4, to trigger PIO0"
    label("cycle")
    mov(x,  osr)          # keep a copy of the current period
    pull(noblock)         # try to fetch a new one…
                          # …if FIFO empty, HW copies X to OSR
    mov(x,  osr)          # reload X with the (new or old) period

    set(pins, 1)          # flash start
    set(pins, 0)          # flash end

    label("delay")
    jmp(x_dec, "delay")   # inter-flash delay
    jmp("cycle")          # next flash

class Stroboscope():   
    def __init__(self):
#        self.strobe_count = 0
        self.next_delay = 0          #stroboscope delay
        self.duty_max = 0.1          # 10% max, to protect the (overdriven) LEDs
        self.duration_max = 0.002    # 2ms max, (same reason)
        #self.set_frequency(1)
        #self.set_duration(0.1)
        
        self.sm1 = StateMachine(1, delay, freq=125_000_000, set_base=pin_a)
        self.sm1.put(2_000_000) #1st cycle, any value

        self.sm0 = StateMachine(0, pulse, freq=125_000_000, set_base=pin_s, in_base=pin_a)

    def start(self):
        self.sm1.active(1)

    def stop(self):
        self.sm1.active(0)
        
    def set_frequency(self, freq):
        "Seems to be working allright between 1 Hz and 50 kHz"
        self.freq = freq
        self.next_delay = int(125_000_000//freq)
        self.sm1.put(self.next_delay) #1st cycle, any value
    
    def _set_duration(self, duration):
        "takes seconds. Sets nb of clock cycles"
        self.duration = min( 125_000_000/self.freq*self.duty_max, 125_000_000*self.duration_max, 125_000_000*duration)

    def set_duration(self, duration):
        "Set pulse width. Take a (float) number of seconds."
        self._set_duration(duration)
        self.sm0.active(0)
        pin_s.value(0) #Turn stroboscope off, just in case
        self.sm0.restart()
        self.sm0.put(int(125_000_000*duration))
        self.sm0.active(1)

def freq(self):
    "Calculate frequency based on rotary encoder value"
    return 

def strobe():
    duty = 0.05
    enc_old = 0
    fine_freq_old = 0
    s = Stroboscope()
    while True:
        if encoder.value<0:
            encoder.value = 0
        enc = max(encoder.value/2, 0)
        fine_freq = p.value()
        if enc_old != enc or abs(fine_freq_old - fine_freq)>0.0012:
            f = pow(1.2, enc) * (1 + (fine_freq-0.5)*1)
            if f > max_freq:
                encoder.value = enc*2-2
                continue
            print(f"Enc: {enc}, {pow(1.2, enc)} Hz base, {f} fine");sleep_ms(100)
            s.set_frequency( f )
            if enc_old != enc:
                s.set_duration(duty/f)
                enc_old = enc
            fine_freq_old = fine_freq
            s.start()
            #print(f"Freq: {freq} Hz, duty: {duty}");sleep_ms(200)
            display_freq(f)
        gc.collect()


strobe()
