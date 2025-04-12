#program for remove specific line of data
import time
import adafruit_sdcard
import board
import busio
import digitalio, displayio
import microcontroller
import storage

# Use any pin that is not taken by SPI
SD_CS = board.GP5
# Connect to the card and mount the filesystem.
spi = busio.SPI(board.GP6, board.GP7, board.GP4)
cs = digitalio.DigitalInOut(SD_CS)
sdcard = adafruit_sdcard.SDCard(spi, cs)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")

file_name = "new.txt"
line_number_to_remove = 7

# Read the data from the file line by line
with open(f"/sd/{file_name}", "r") as f:
    print("\nPrinting lines in file before removal:")
    lines = f.readlines()
    for line in lines:
        print(line.strip())  # Use .strip() to remove the newline character at the end


# Function to remove a specific line from a file
def remove_line_from_file(file_path, line_number):
    with open(file_path, "r") as file:
        lines = file.readlines()
    
    if 0 < line_number <= len(lines):
        lines.pop(line_number - 1)  # Remove the specified line

    with open(file_path, "w") as file:
        for line in lines:
            file.write(line)

# Remove the specified line from the file
remove_line_from_file(f"/sd/{file_name}", line_number_to_remove)

# Verify the removal by reading the file again
with open(f"/sd/{file_name}", "r") as f:
    print("\nPrinting lines in file after removal:")
    lines = f.readlines()
    for line in lines:
        print(line.strip())  # Use .strip() to remove the newline character at the end



