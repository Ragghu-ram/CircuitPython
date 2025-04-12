#program for clear data in the file
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

file_name = "new.txt"

# Clear the file before logging
print("Clearing file...")
with open(f"/sd/{file_name}", "w") as f:
    f.write("")
