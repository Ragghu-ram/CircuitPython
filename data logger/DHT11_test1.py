
import time
import adafruit_dht
import board

dht = adafruit_dht.DHT11(board.GP15)
logging_duration = 10  # seconds
start_time = time.monotonic()

while (time.monotonic() - start_time) < logging_duration:
    try:
        temperature = dht.temperature
        humidity = dht.humidity
        # Print what we got to the REPL
        print("Temp: {:.1f} *C \t Humidity: {}%".format(temperature, humidity))
    except RuntimeError as e:
        # Reading doesn't always work! Just print error and we'll try again
        print("Reading from DHT failure: ", e.args)

    time.sleep(1)

