import time
import board
import digitalio
import simpleio
import busio
import mfrc522

# Define the buzzer and note frequencies
NOTE_C5 = 523
NOTE_G5 = 784
buzzer = board.GP25

# Setup the relay
relay = digitalio.DigitalInOut(board.GP3)
relay.switch_to_output()

# Setup the SPI bus and RFID reader
cs = board.GP5 #SDA 
sck = board.GP6
mosi = board.GP7
miso = board.GP4
rst = board.GP22

spi = busio.SPI(sck, MOSI=mosi, MISO=miso)

# Pass the pin objects directly, not wrapped in DigitalInOut

rfid = mfrc522.MFRC522(spi, cs, rst)
rfid.set_antenna_gain(0x07 << 4)

print("\n***** Scan your RFID tag/card *****\n")

prev_data = ""
prev_time = 0
timeout = 1

while True:
    (status, tag_type) = rfid.request(rfid.REQALL)

    if status == rfid.OK:
        (status, raw_uid) = rfid.anticoll()

        if status == rfid.OK:
            rfid_data = "{:02x}{:02x}{:02x}{:02x}".format(raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3])

            if rfid_data != prev_data:
                prev_data = rfid_data

                print("Card detected! UID: {}".format(rfid_data))

                if rfid_data == "cc40b773":
                    simpleio.tone(buzzer, NOTE_C5, 0.08)
                    simpleio.tone(buzzer, NOTE_G5, 0.08)

                    time.sleep(1)
                    print("Activate relay for 5 seconds")
                    relay.value = True
                    time.sleep(5)
                    relay.value = False

                else:
                    simpleio.tone(buzzer, NOTE_C5, 0.3)

            prev_time = time.monotonic()

    else:
        if time.monotonic() - prev_time > timeout:
            prev_data = ""
