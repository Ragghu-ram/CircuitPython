#program for log DHT11 data into two files 
import time
import adafruit_dht
import board
import busio
import digitalio
import adafruit_sdcard
import storage

# SD card configuration
SD_CS = board.GP5

# Setup SD card
spi = busio.SPI(board.GP6, board.GP7, board.GP4)
cs = digitalio.DigitalInOut(SD_CS)
sdcard = adafruit_sdcard.SDCard(spi, cs)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")

# DHT sensor configuration
dht = adafruit_dht.DHT11(board.GP15)

# Logging configuration
logging_duration = 10  # seconds
start_time = time.monotonic()

def get_timestamp():
    current_time = time.localtime()
    return "{:02}:{:02}:{:02}".format(current_time[3], current_time[4], current_time[5])

# Open files for appending
with open("/sd/hum.txt", "a") as hum_file, open("/sd/temp.txt", "a") as temp_file:
    while (time.monotonic() - start_time) < logging_duration:
        try:
            temperature = dht.temperature
            humidity = dht.humidity
            current_time = get_timestamp()

            # Print what we got to the REPL
            print(f"Temp: {current_time} -> {temperature}  Hum: {current_time} -> {humidity}")

            # Write the data to the respective files
            hum_file.write(f"{current_time} -> {humidity}\n")
            temp_file.write(f"{current_time} -> {temperature}\n")
        except RuntimeError as e:
            # Reading doesn't always work! Just print error and we'll try again
            print("Reading from DHT failure: ", e.args)

        time.sleep(1)

