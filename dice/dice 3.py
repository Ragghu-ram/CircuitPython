import board
import digitalio
import time
import random

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

# Set up the button
button = digitalio.DigitalInOut(board.GP1)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

# Define the digit to segment mapping
digit_to_segments = {
    1: ['b', 'c'],
    2: ['a', 'b', 'g', 'e', 'd'],
    3: ['a', 'b', 'g', 'c', 'd'],
    4: ['f', 'g', 'b', 'c'],
    5: ['a', 'f', 'g', 'c', 'd'],
    6: ['a', 'f', 'g', 'e', 'c', 'd'],
}

def display_digit(digit, decimal_on):
    # Turn off all segments
    for segment in segments.values():
        segment.value = False
    
    # Turn on the required segments for the digit
    for segment in digit_to_segments[digit]:
        segments[segment].value = True
    
    # Control the decimal point
    segments['p'].value = decimal_on

# Initialize the last two numbers
last_two_numbers = []

def get_new_number():
    available_numbers = [1, 2, 3, 4, 5, 6]
    # Remove the last two numbers from the list of available numbers
    for number in last_two_numbers:
        if number in available_numbers:
            available_numbers.remove(number)
    # Randomly select a new number from the remaining options
    dice_value = random.choice(available_numbers)
    print(f"Number : {dice_value} ")
    return dice_value

while True:
    if not button.value:  # Button is pressed (connected to ground)
        time.sleep(0.2)  # Debounce delay
        new_number = get_new_number()
        blink_duration = 5  # Blink for 3 seconds
        start_time = time.time()
        
        while time.time() - start_time < blink_duration:
            # Blink the decimal point on and off
            display_digit(new_number, decimal_on=True)
            time.sleep(0.5)
            display_digit(new_number, decimal_on=False)
            time.sleep(0.5)
        
        # Update the last two numbers list
        last_two_numbers.append(new_number)
        if len(last_two_numbers) > 2:
            last_two_numbers.pop(0)
        
        # Wait for button release
        while not button.value:
            time.sleep(0.1)

