import board
import digitalio
import time

# Define the segment pins
segments = {
    'a': digitalio.DigitalInOut(board.GP17),
    'b': digitalio.DigitalInOut(board.GP16),
    'c': digitalio.DigitalInOut(board.GP18),
    'd': digitalio.DigitalInOut(board.GP21),
    'e': digitalio.DigitalInOut(board.GP20),
    'f': digitalio.DigitalInOut(board.GP26),
    'g': digitalio.DigitalInOut(board.GP27),
    'p': digitalio.DigitalInOut(board.GP19)  # Decimal point
}

# Set all segments to output
for segment in segments.values():
    segment.direction = digitalio.Direction.OUTPUT

# Define the digit to segment mapping
digit_to_segments = {
    0: ['a', 'b', 'c', 'd', 'e', 'f'],
    1: ['b', 'c'],
    2: ['a', 'b', 'g', 'e', 'd'],
    3: ['a', 'b', 'g', 'c', 'd'],
    4: ['f', 'g', 'b', 'c'],
    5: ['a', 'f', 'g', 'c', 'd'],
    6: ['a', 'f', 'g', 'e', 'c', 'd'],
    7: ['a', 'b', 'c'],
    8: ['a', 'b', 'c', 'd', 'e', 'f', 'g'],
    9: ['a', 'b', 'c', 'd', 'f', 'g'],
    10:['a', 'b', 'c', 'e', 'f', 'g'],
    11:['c', 'd', 'e', 'f', 'g'],
    12:['a', 'd', 'e', 'f'],
    13:['b', 'c', 'd', 'e','g'],
    14:['a', 'd', 'e', 'f', 'g'],
    15:['a', 'e', 'f', 'g'],
}

def blink_segments():
    for segment_name in ['a', 'b', 'c', 'd', 'e', 'f', 'g']:
        segments[segment_name].value = True  # Turn on the segment
        time.sleep(0.2)                      # Wait for 0.5 seconds
        segments[segment_name].value = False # Turn off the segment
        time.sleep(0.2)                      # Wait for 0.5 seconds

# Start blinking the segments in sequence from a to g
blink_segments()

def display_digit(digit):
    # Turn off all segments
    for segment in segments.values():
        segment.value = False
    
    # Turn on the required segments for the digit
    for segment in digit_to_segments[digit]:
        segments[segment].value = True
for digit in range(16):
    display_digit(digit)
    time.sleep(0.5)  # Display each digit for 1 second

def blink_decimal_point():
    while True:
        segments['p'].value = True  # Turn on the decimal point
        time.sleep(0.5)             # Wait for 0.5 seconds
        segments['p'].value = False # Turn off the decimal point
        time.sleep(0.5)             # Wait for 0.5 seconds

while True:
    # Ensure all segments except the decimal point are turned off
    for segment_name, segment in segments.items():
        if segment_name != 'p':
            segment.value = False

    # Start blinking the decimal point
    blink_decimal_point()

