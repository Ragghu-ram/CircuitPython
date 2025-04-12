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

led = digitalio.DigitalInOut(board.GP25)
led.direction = digitalio.Direction.OUTPUT

# Connect to the card and mount the filesystem.
spi = busio.SPI(board.GP6, board.GP7, board.GP4)
cs = digitalio.DigitalInOut(SD_CS)
sdcard = adafruit_sdcard.SDCard(spi, cs)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")

file_name = "new.txt"
logging_duration = 10  # seconds
logging_interval = 1  # seconds
start_time = time.monotonic()

# Clear the file before logging
print("Clearing file...")
with open(f"/sd/{file_name}", "w") as f:
    f.write("")
time.sleep(logging_interval)

print("Logging temperature to filesystem")
with open(f"/sd/{file_name}", "w") as f:
    f.write(f"logging_interval = {logging_interval}\r\nlogging_duration = {logging_duration}\r\n")

# Log temperature data for 10 seconds
while (time.monotonic() - start_time) <= logging_duration:
    # Open file for append
    with open(f"/sd/{file_name}", "a") as f:
        led.value = True  # Turn on LED to indicate we're writing to the file
        t = microcontroller.cpu.temperature
        print("Temperature = %0.1f" % t)
        f.write("%0.1f\n" % t)
        led.value = False  # Turn off LED to indicate we're done
    time.sleep(logging_interval)
print("Logging complete.")

# Read the data from the file line by line after logging
with open(f"/sd/{file_name}", "r") as f:
    print("\nPrinting lines in file:")
    line = f.readline()
    while line != '':
        print(line.strip())  # Use .strip() to remove the newline character at the end
        line = f.readline()

# Function to read a specific line from a file
def read_line_from_file(file_path, line_number):
    with open(file_path, "r") as file:
        for current_line_number, line in enumerate(file, start=1):
            if current_line_number == line_number:
                return line.strip()  # Remove any leading/trailing whitespace
    return None  # Return None if the line number is out of range

# Read the specific lines from the file
first_line = read_line_from_file(f"/sd/{file_name}", 1)
second_line = read_line_from_file(f"/sd/{file_name}", 2)

logging_interval = int(first_line.split('=')[1].strip())
logging_duration = int(second_line.split('=')[1].strip())
print(f"Logging interval from the first line: {logging_interval} seconds")
print(f"Logging duration from the second line: {logging_duration} seconds")


