import time
import adafruit_sdcard
import board
import busio
import digitalio, displayio
import microcontroller
import storage

# Release any previously held displays
displayio.release_displays()

# Use any pin that is not taken by SPI
SD_CS = board.GP5
# Connect to the card and mount the filesystem.
spi = busio.SPI(board.GP6, board.GP7, board.GP4)
cs = digitalio.DigitalInOut(SD_CS)
sdcard = adafruit_sdcard.SDCard(spi, cs)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")

file_name = "temp.txt"
start_time = time.monotonic()

# Read the data from the file line by line after logging
with open(f"/sd/{file_name}", "r") as f:
    print(f"Reading data from {file_name} file:")
    line = f.readline()
    while line != '':
        print(line.strip())  # Use .strip() to remove the newline character at the end
        line = f.readline()


