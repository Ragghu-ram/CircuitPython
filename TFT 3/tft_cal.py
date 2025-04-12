import board
import busio
import displayio
import os
import terminalio  # Just a font
import adafruit_ili9341
from adafruit_display_text import label
import digitalio
import time
from adafruit_bitmap_font import bitmap_font

# Release any previously held displays
displayio.release_displays()

board_type = os.uname().machine
print(f"Board: {board_type}")

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

# Load a larger font
font = bitmap_font.load_font("/Arial-16.bdf")  # Ensure the font file is in the correct path

# Days of the week mapping
days_of_week = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

# Touch buttons setup
touch_pins = [board.GP13, board.GP14, board.GP15]
touch_buttons = []

for pin in touch_pins:
    touch = digitalio.DigitalInOut(pin)
    touch.direction = digitalio.Direction.INPUT
    touch.pull = digitalio.Pull.DOWN
    touch_buttons.append(touch)

def display_calendar(year, month, day_of_week, today):
    # Clear previous content
    while len(splash) > 0:
        splash.pop()

    # Define colors
    white = 0xFFFFFF
    black = 0x000000

    # Create a color bitmap and palette
    color_bitmap = displayio.Bitmap(320, 240, 1)
    color_palette = displayio.Palette(1)
    color_palette[0] = black

    # Create a background sprite
    bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
    splash.append(bg_sprite)

    # Create a label for the current year and month
    month_names = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    header_text = f"< {month_names[month-1]} {year} >"
    header = label.Label(font, text=header_text, color=white)
    header.x = (320 - header.bounding_box[2]) // 2  # Center the header
    header.y = 10
    splash.append(header)

    # Create text labels for the days of the week
    day_labels = ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"]
    x = 0
    y = 35
    for label_text in day_labels:
        text_area = label.Label(font, text=label_text, color=white, x=x, y=y)
        splash.append(text_area)
        x += 45

    # Calculate starting position for the days
    x = day_of_week * 45
    y = 60

    # Display the days of the month
    num_days = get_days_in_month(year, month)
    for day in range(1, num_days + 1):
        text_area = label.Label(font, text=str(day), color=white, x=x, y=y)
        splash.append(text_area)
        x += 45
        day_of_week = (day_of_week + 1) % 7

        if day_of_week == 0:
            x = 0
            y += 28  # Start a new line

        if y >= 220:  # if the calendar exceeds the display height, wrap to top
            x = 0
            y = 30

def zellers_congruence(day, month, year):
    if month < 3:
        month += 12
        year -= 1
    K = year % 100
    J = year // 100
    h = (day + (13 * (month + 1)) // 5 + K + (K // 4) + (J // 4) + 5 * J) % 7
    # Convert to day of the week (0 = Saturday, 1 = Sunday, ..., 6 = Friday)
    day_of_week = (h + 6) % 7  # Adjust to 0 = Sunday, 1 = Monday, ..., 6 = Saturday
    return day_of_week

def is_leap_year(year):
    # Check if a year is a leap year
    if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
        return True
    return False

def get_days_in_month(year, month):
    # Determine the number of days in a month, considering leap year
    days_in_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if month == 2 and is_leap_year(year):
        return 29  # February has 29 days in a leap year
    return days_in_month[month]

# Initial values for year and month
year = 2024
month = 1

# Display initial year and month
def display_year_month(year, month, selecting_year):
    global year_label, month_label, selection_indicator

    # Clear previous content
    while len(splash) > 0:
        splash.pop()

    # Create and display text labels for year and month
    year_label = label.Label(font, text=f"Year: {year}", color=0xFFFFFF, x=30, y=50)
    splash.append(year_label)
    month_label = label.Label(font, text=f"Month: {month}", color=0xFFFFFF, x=30, y=80)
    splash.append(month_label)

    # Update selection indicator
    selection_indicator = label.Label(font, text=">", color=0xFFFFFF, x=10, y=50 if selecting_year else 80)
    splash.append(selection_indicator)

# Main function to handle the selection and display process
def main():
    global year, month, selecting_year, year_label, month_label, selection_indicator

    # Initialize values
    year = 2024
    month = 1
    selecting_year = True

    # Display initial values
    display_year_month(year, month, selecting_year)

    calendar_displayed = False

    # Main loop to handle touch inputs
    while True:
        if touch_buttons[0].value:  # Up button
            if calendar_displayed:
                month += 1
                if month > 12:
                    month = 1
                    year += 1
                day = 1
                week = zellers_congruence(day, month, year)
                display_calendar(year, month, week, day)
            elif selecting_year:
                year += 1
                display_year_month(year, month, selecting_year)
            else:
                month += 1
                if month > 12:
                    month = 1
                display_year_month(year, month, selecting_year)
            time.sleep(0.2)  # Debounce delay

        if touch_buttons[1].value:  # Down button
            if calendar_displayed:
                month -= 1
                if month < 1:
                    month = 12
                    year -= 1
                day = 1
                week = zellers_congruence(day, month, year)
                display_calendar(year, month, week, day)
            elif selecting_year:
                year -= 1
                display_year_month(year, month, selecting_year)
            else:
                month -= 1
                if month < 1:
                    month = 12
                display_year_month(year, month, selecting_year)
            time.sleep(0.2)  # Debounce delay

        if touch_buttons[2].value:  # Selection button
            if calendar_displayed:
                calendar_displayed = False
                selecting_year = True
                display_year_month(year, month, selecting_year)
            else:
                if selecting_year:
                    selecting_year = False
                    display_year_month(year, month, selecting_year)  # Update to show indicator for month
                else:
                    # Display the calendar for the given year and month
                    day = 1
                    week = zellers_congruence(day, month, year)
                    display_calendar(year, month, week, day)
                    calendar_displayed = True

            time.sleep(0.2)  # Debounce delay
            
# Run the main function
main()

