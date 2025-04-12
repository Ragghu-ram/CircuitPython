import board
import busio
import displayio
import terminalio
import adafruit_ili9341
from adafruit_display_shapes.triangle import Triangle
from adafruit_display_shapes.circle import Circle
from adafruit_display_shapes.line import Line
from adafruit_display_text.label import Label
import math
import time

class Gauge(displayio.Group):
    def __init__(self, min_val, max_val, width, height, base_size=8, 
                 colour=0x0000FF, outline_colour=0x0000FF, outline=True, bg_colour=0x000000, display_value=True, 
                 value_label="", arc_colour=0xFF0000, colour_fade=False, arc_thickness=5, num_ticks=5):
        super().__init__()
        self.width = width
        self.height = height
        self.pivot1 = [(width//2)-(base_size//2), height - 40]  # Adjusted the pivot points to be higher
        self.pivot2 = [(width//2)+(base_size//2), height - 40]
        self.mid = width // 2
        self.min_val = min_val
        self.max_val = max_val
        self.colour = colour
        self.value_label = value_label
        self.outline_colour = outline_colour
        self.outline = outline

        self.length = int(1.4 * (width / 2))
        if outline:
            self.arrow = Triangle(self.pivot1[0], self.pivot1[1] - self.length, self.pivot2[0], self.pivot2[1] - self.length, self.mid,
                                  self.pivot1[1], fill=self.colour, outline=self.outline_colour)
        else:
            self.arrow = Triangle(self.pivot1[0], self.pivot1[1] - self.length, self.pivot2[0], self.pivot2[1] - self.length, self.mid,
                                  self.pivot1[1], fill=self.colour)

        self.pointer_circle = Circle(self.mid, self.pivot1[1], 8, fill=self.colour)  # Small circle at the pointer's middle
        self.data = Label(terminalio.FONT, text="0.0", color=0xFFFFFF, font_size=100)
        self.data.x = width // 2
        self.data.y = height - 20  # Adjust the position of the data label
        if display_value:
            super().append(self.data)
        super().append(self.pointer_circle)  # Add the small circle to the display
        super().append(self.arrow)
        
    def update(self, val):
        max_angle = 180
        if val < self.min_val:
            angle = 0
        elif val > self.max_val:
            angle = max_angle
        else:
            angle = ((((val - self.min_val) / (self.max_val - self.min_val))) * max_angle)

        top_point_x = self.mid - int(math.cos(math.radians(angle)) * self.length)
        top_point_y = self.height - 40 - int(math.sin(math.radians(angle)) * self.length)

        if self.outline:
            self.arrow = Triangle(self.pivot1[0], self.pivot1[1], self.pivot2[0], self.pivot2[1], top_point_x,
                                  top_point_y, fill=self.colour, outline=self.outline_colour)
        else:
            self.arrow = Triangle(self.pivot1[0], self.pivot1[1], self.pivot2[0], self.pivot2[1], top_point_x,
                                  top_point_y, fill=self.colour)
        super().pop()
        super().append(self.arrow)

        self.data.text = self.value_label + str(int(val))
        
# Function to update the displayed image
def show_bitmap(bitmap):
    # Clear the previous bitmap
    if len(group) > 0:
        group.pop()
    # Add the new bitmap
    tile_grid = displayio.TileGrid(bitmap, pixel_shader=bitmap.pixel_shader)
    group.append(tile_grid)

    
# Main script
# Release any previously held displays
displayio.release_displays()

# Define pin configurations based on the board type
cs_pin, reset_pin, dc_pin, mosi_pin, clk_pin = board.GP10, board.GP9, board.GP8, board.GP7, board.GP6

# Initialize SPI bus
spi = busio.SPI(clock=clk_pin, MOSI=mosi_pin)

# Set up the display bus using SPI and the appropriate pins
display_bus = displayio.FourWire(spi, command=dc_pin, chip_select=cs_pin, reset=reset_pin)

# Initialize the display
display = adafruit_ili9341.ILI9341(display_bus, width=320, height=240, rotation=180)

# Load bitmaps
bitmap = displayio.OnDiskBitmap("/10.bmp")

# Create the main display group
group = displayio.Group()
display.root_group = group

# Adjust the width and height of the gauge
gauge = Gauge(0, 100, 190, 100, value_label="x:", arc_colour=0xFF0000, colour=0x0000FF, outline_colour=0x0000FF, arc_thickness=7, num_ticks = 11)
gauge.x = 62
gauge.y = 120

group = displayio.Group(scale=1)
show_bitmap(bitmap)
group.append(gauge)

# Set group as root group for display
display.root_group = group
display.auto_refresh = True

x = 0

while x < 100:
    x += 10
    gauge.update(x)
    time.sleep(0.1)  # Adding a small delay for smoother updates




