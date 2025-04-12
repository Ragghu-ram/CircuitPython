# Raspberry Pi Pico with rp2040 with TFT
import board, busio, displayio, os
import terminalio  # Just a font
import adafruit_ili9341
from adafruit_display_text import label
import time
import adafruit_sdcard
import board
import busio
import digitalio
import microcontroller
import storage

led = digitalio.DigitalInOut(board.GP13)
led.direction = digitalio.Direction.OUTPUT

# Release any previously held displays
displayio.release_displays()

board_type = os.uname().machine
print(f"Board: {board_type}")

# Define pin configurations based on the board type
# Use any pin that is not taken by SPI
SD_CS = board.GP5
cs_pin, reset_pin, dc_pin, mosi_pin, clk_pin = board.GP10, board.GP9, board.GP8, board.GP7, board.GP6

# Initialize SPI bus
spi = busio.SPI(clock=clk_pin, MOSI=mosi_pin, MISO=board.GP4)
cs_sd = digitalio.DigitalInOut(SD_CS)
sdcard = adafruit_sdcard.SDCard(spi, cs_sd)
vfs = storage.VfsFat(sdcard)
print("Mounting storage device")
time.sleep(0.5)
storage.mount(vfs, "/sd")

# Use the filesystem as normal! Our files are under /sd

print("Logging temperature to filesystem")

file_name = "test.txt"
logging_duration = 5  # seconds
start_time = time.monotonic()

# Log temperature data for 10 seconds
while (time.monotonic() - start_time) < logging_duration:
    # Open file for append
    with open(f"/sd/{file_name}", "a") as f:
        led.value = True  # Turn on LED to indicate we're writing to the file
        t = microcontroller.cpu.temperature
        print("Temperature = %0.1f" % t)
        f.write("%0.1f\n" % t)
        led.value = False  # Turn off LED to indicate we're done
    time.sleep(1)

print("Logged data from filesystem:")
# Read the data from the file after logging
with open(f"/sd/{file_name}", "r") as f:
    data = f.read()
    print(data)

print("Logging complete. Exiting...")

# Set up the display bus using SPI and the appropriate pins
display_bus = displayio.FourWire(spi, command=dc_pin, chip_select=cs_pin, reset=reset_pin)

# Initialize the display
display = adafruit_ili9341.ILI9341(display_bus, width=320, height=240, rotation=180)

# Create the main display group
splash = displayio.Group()
display.root_group = splash

# Create a color bitmap and palette
color_bitmap = displayio.Bitmap(320, 240, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0x00FF00  # Bright Green

# Create a background sprite
bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)

# Draw a smaller inner rectangle
inner_bitmap = displayio.Bitmap(310, 230, 1)
inner_palette = displayio.Palette(2)
inner_palette[0] = 0x000000  # Black
inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=inner_palette, x=5, y=5)
splash.append(inner_sprite)

# Draw a label
text_group = displayio.Group(scale=1, x=11, y=24)
text = "Hello World!\n\nThis is a sample\ntest!\n\nReading data\nfrom SD card."
text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF)
text_group.append(text_area)  # Subgroup for text scaling
splash.append(text_group)

time.sleep(3)
print("Releasing SPI devices")
time.sleep(0.5)
print("Releasing Display device")
# Release any previously held displays
displayio.release_displays()
print("Unmounting Storage device")
storage.umount("/sd")
spi.deinit()  # Deinitialize SPI to ensure clean startup next time
time.sleep(0.5)  # Short delay to ensure the card is properly unmounted
