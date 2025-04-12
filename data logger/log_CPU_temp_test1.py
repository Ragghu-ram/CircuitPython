import time
import adafruit_sdcard
import board
import busio
import digitalio, displayio
import microcontroller
import storage

# Use any pin that is not taken by SPI
SD_CS = board.GP5
spi = busio.SPI(board.GP6, board.GP7, board.GP4)
# Connect to the card and mount the filesystem.
cs = digitalio.DigitalInOut(SD_CS)
sdcard = adafruit_sdcard.SDCard(spi, cs)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")

file_name = "new.txt"

# Log temperature data for 10 seconds
while True:
    # Open file for append
    with open(f"/sd/{file_name}", "a") as f:
        t = microcontroller.cpu.temperature
        print("Temperature = %0.1f" % t)
        f.write("%0.1f\n" % t)
    time.sleep(1)
print("Logging complete.")



