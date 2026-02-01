from machine import Pin

#Driver for rotary encoder.
#Just read variable value

# Encoder pins
pin_a = Pin(7, Pin.IN, Pin.PULL_UP)
pin_b = Pin(8, Pin.IN, Pin.PULL_UP)

# value counter
value = 0

# Previous state of encoder A pin
prev_a = pin_a.value()

def update_value(pin):
    global value, prev_a
    a = pin_a.value()
    b = pin_b.value()

    if a != prev_a:  # Check if A has changed
        if a == b:
            value += 1
        else:
            value -= 1

        prev_a = a

# Set up interrupts on both pins
pin_a.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=update_value)
pin_b.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=update_value)

# Usage loop
#import time

#while True:
#    print("value:", value)
#    time.sleep(0.2)