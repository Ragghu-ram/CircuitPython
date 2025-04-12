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
import digitalio
from hx711_gpio import HX711

pin_OUT = digitalio.DigitalInOut(board.GP17)
pin_SCK = digitalio.DigitalInOut(board.GP18)
pin_SCK.direction = digitalio.Direction.OUTPUT

hx = HX711(pin_SCK, pin_OUT)
hx.OFFSET = 0  # Adjust if needed
hx.set_gain(128)
time.sleep(0.5)
scale = 25000.0

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
        self.data = Label(terminalio.FONT, text="0.0", color=0xFFFFFF, scale=2)  # Adjusted scale for better readability
        self.data.anchor_point = (0.5, 0.5)
        self.data.anchored_position = (width // 2, height - 20)  # Adjust the position of the data label
        if display_value:
            super().append(self.data)

        arc = self.draw_thick_half_circle_arc(width // 2, height - 40, self.length, arc_colour, arc_thickness)
        for segment in arc:
            super().append(segment)

        ticks_and_labels = self.draw_ticks_and_labels(width // 2, height - 40, self.length, num_ticks, min_val, max_val)
        for item in ticks_and_labels:
            super().append(item)
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

    def draw_thick_half_circle_arc(self, centerpoint_x, centerpoint_y, radius, colour, thickness=5):
        arc_segments = []
        num_segments = 20  # Reduce segments to lower memory usage
        for i in range(num_segments):
            start_angle = math.radians(i * 180 / num_segments)
            end_angle = math.radians((i + 1) * 180 / num_segments)
            for offset in range(thickness):
                inner_radius = radius - offset
                x1 = centerpoint_x + int(math.cos(start_angle) * inner_radius)
                y1 = centerpoint_y - int(math.sin(start_angle) * inner_radius)
                x2 = centerpoint_x + int(math.cos(end_angle) * inner_radius)
                y2 = centerpoint_y - int(math.sin(end_angle) * inner_radius)
                arc_segments.append(Line(x1, y1, x2, y2, color=colour))
        return arc_segments

    def draw_ticks_and_labels(self, centerpoint_x, centerpoint_y, radius, num_ticks, min_val, max_val):
        ticks_and_labels = []
        tick_angle_increment = 180 / (num_ticks - 1)
        value_increment = (max_val - min_val) / (num_ticks - 1)
        for i in range(num_ticks):
            tick_angle = math.radians(i * tick_angle_increment)
            inner_x = centerpoint_x + int(math.cos(tick_angle) * (radius - 25))
            inner_y = centerpoint_y - int(math.sin(tick_angle) * (radius - 25))
            outer_x = centerpoint_x + int(math.cos(tick_angle) * radius)
            outer_y = centerpoint_y - int(math.sin(tick_angle) * radius)
            ticks_and_labels.append(Line(inner_x, inner_y, outer_x, outer_y, color=0xFFFFFF))
            
            # Add labels
            label_x = centerpoint_x + int(math.cos(tick_angle) * (radius + 15))
            label_y = centerpoint_y - int(math.sin(tick_angle) * (radius + 15))
            value = max_val - (min_val + i * value_increment)
            label = Label(terminalio.FONT, text=str(int(value)), color=0xFFFFFF)
            label.anchor_point = (0.5, 0.5)
            label.anchored_position = (label_x, label_y)
            ticks_and_labels.append(label)
            
            # Add small ticks at the middle of existing ticks
            if i < num_ticks - 1:
                mid_angle = math.radians((i + 0.5) * tick_angle_increment)
                mid_inner_x = centerpoint_x + int(math.cos(mid_angle) * (radius - 10))
                mid_inner_y = centerpoint_y - int(math.sin(mid_angle) * (radius - 10))
                mid_outer_x = centerpoint_x + int(math.cos(mid_angle) * radius)
                mid_outer_y = centerpoint_y - int(math.sin(mid_angle) * radius)
                ticks_and_labels.append(Line(mid_inner_x, mid_inner_y, mid_outer_x, mid_outer_y, color=0xFFFFFF))

        return ticks_and_labels

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

# Create the main display group
splash = displayio.Group()
display.root_group = splash

# Adjust the width and height of the gauge
gauge = Gauge(0, 1000, 190, 100, value_label="Weight:", arc_colour=0xFF0000, colour=0xFFFF00, outline_colour=0xFFFF00, arc_thickness=7, num_ticks=11)
gauge.x = 62
gauge.y = 120

group = displayio.Group(scale=1)
group.append(gauge)

# Set group as root group for display
display.root_group = group
display.auto_refresh = True

x = 0

while True:
    data = (hx.read() / scale) * 10
    if data < 0:
        data = 0  # If data is below 0, show it as 0
    print(f"{data:.2f}")
    
    gauge.update(data)
    time.sleep(0.1)

