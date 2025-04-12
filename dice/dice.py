import board, time
import digitalio

a = digitalio.DigitalInOut(board.GP17)
b = digitalio.DigitalInOut(board.GP16)
c = digitalio.DigitalInOut(board.GP18)
d = digitalio.DigitalInOut(board.GP21)
e = digitalio.DigitalInOut(board.GP20)
f = digitalio.DigitalInOut(board.GP26)
g = digitalio.DigitalInOut(board.GP27)
p = digitalio.DigitalInOut(board.GP19)

a.direction = digitalio.Direction.OUTPUT
b.direction = digitalio.Direction.OUTPUT
c.direction = digitalio.Direction.OUTPUT
d.direction = digitalio.Direction.OUTPUT
e.direction = digitalio.Direction.OUTPUT
f.direction = digitalio.Direction.OUTPUT
g.direction = digitalio.Direction.OUTPUT
p.direction = digitalio.Direction.OUTPUT
while True:
    a.value = True
    b.value = True
    c.value = True
    d.value = True
    e.value = True
    f.value = True
    g.value = True
    p.value = True

