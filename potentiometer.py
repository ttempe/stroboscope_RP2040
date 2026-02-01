from machine import Pin
from time import sleep_ms

class Potentiometer:
    def __init__(self, pin, cal_min=1000, cal_max=64000, invert=False):
        self.pin = pin
        self.min = cal_min
        self.max = cal_max
        self.invert = invert
    
    @property
    def read(self):
        avg = 0
        for i in range(32):
            avg += self.pin.read_u16()
        return avg//32
    
    def value(self):
        "Return a float between 0 and 1"
        val = self.read
        self.min = min(val, self.min)
        self.max = max(val, self.max)
        ret = (val-self.min)/(self.max-self.min)
        return 1-ret if self.invert else ret

    def calibrate(self):
        vmax=0
        vmin=65535
        while True:
            v = self.read
            vmax = max(v, vmax)
            vmin = min(v, vmin)
            print(v, vmin, vmax)
            sleep_ms(300)
