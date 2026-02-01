from machine import Pin, I2C
import ssd1306, framebuf

# using default address 0x3C
i2c = I2C(id=0, sda=Pin(12), scl=Pin(13), freq=100_000)
display = ssd1306.SSD1306_I2C(128, 32, i2c)

def draw_scaled_text(display, text, x, y, addr=60, scale=2):
    for i, c in enumerate(text):
        char = framebuf.FrameBuffer(bytearray(8), 8, 8, framebuf.MONO_HLSB)
        char.text(c, 0, 0, 1)
        for cx in range(8):
            for cy in range(8):
                if char.pixel(cx, cy):
                    display.framebuf.fill_rect(x + i * 8 * scale + cx * scale, y + cy * scale, scale, scale, 1)

def display_freq(freq):
    display.fill(0)
    if freq <10:
        t = f"{freq:4.3f} Hz"
    elif freq <100:
        t = f"{freq:4.2f} Hz"
    elif freq <1000:
        t = f"{freq:4.1f} Hz"
    elif freq <10_000:
        t = f"{freq/1000:3.2f} kHz"
    elif freq <100_000:
        t = f"{freq/1000:3.1f} kHz"
    elif freq <1_000_000:
        t = f"{freq/1000:3.0f} kHz"
    elif freq <10_000_000:
        t = f"{freq/1_000_000:3.2f} MHz"
    elif freq <100_000_000:
        t = f"{freq/1_000_000:3.1f} MHz"
    else:
        t = "Trop rapide!!"
    draw_scaled_text(display, t, 0, 0, framebuf.MONO_HLSB)
    #display.text( f"{duty*100:3.0f}%", 48, 24)
    display.show()

display.contrast(255)

#i2c.writeto(0x3C, b'\x00\xA0') #Hz flip
#i2c.writeto(0x3C, b'\x00\xC0') #Vert flip
display.fill(0)
display.text("Stroboscope V3", 0, 0, framebuf.MONO_HLSB)
display.show()

#draw_scaled_text(display, "Hi", 0, 0, scale=3)  # 24 pixels tall
#display.text("Hello world", 10, 10)
#display.fill(0)
#display.pixel(10, 10, 1)
#display.show()