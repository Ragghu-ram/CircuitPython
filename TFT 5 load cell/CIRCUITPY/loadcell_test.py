import board
import digitalio
from hx711_gpio import HX711
import time

pin_OUT = digitalio.DigitalInOut(board.GP17)
pin_SCK = digitalio.DigitalInOut(board.GP18)
pin_SCK.direction = digitalio.Direction.OUTPUT

hx = HX711(pin_SCK, pin_OUT)
hx.OFFSET = 0 # -150000
hx.set_gain(128)
time.sleep(0.050)
scale = 25000.0


while True:
    data = hx.read() / scale
    sai = f"{abs(data):.2f}"
    print(sai)
    time.sleep(0.050)

