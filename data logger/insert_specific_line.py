#program for insert data in a specific line
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
line_number = 2
new_data = "this is line number two"


# Function to read a specific line from a file
def read_line_from_file(file_path, line_number):
    with open(file_path, "r") as file:
        for current_line_number, line in enumerate(file, start=1):
            if current_line_number == line_number:
                return line.strip()  # Remove any leading/trailing whitespace
    return None  # Return None if the line number is out of range

# Function to insert data at a specific line number
def insert_line_in_file(file_path, line_number, new_data):
    with open(file_path, "r") as file:
        lines = file.readlines()
    
    if line_number > len(lines):
        lines.append(new_data + '\n')
    else:
        lines.insert(line_number - 1, new_data + '\n')
    
    with open(file_path, "w") as file:
        for line in lines:
            file.write(line)

# Insert the new data at the specified line number
insert_line_in_file(f"/sd/{file_name}", line_number, new_data)

# Verify the insertion by reading the file again
with open(f"/sd/{file_name}", "r") as f:
    print("\nPrinting lines in file after insertion:")
    lines = f.readlines()
    for line in lines:
        print(line.strip())  # Use .strip() to remove the newline character at the end

# Read the specific lines from the file
data = read_line_from_file(f"/sd/{file_name}", line_number)

print(f"Reading data from {file_name} line number {line_number} is: {data}")


