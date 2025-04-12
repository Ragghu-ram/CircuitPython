import time
import board
import digitalio
import busio
import mfrc522

# Setup the SPI bus and RFID reader
cs = board.GP5  # SDA
sck = board.GP6
mosi = board.GP7
miso = board.GP4
rst = board.GP22

spi = busio.SPI(sck, MOSI=mosi, MISO=miso)

# Initialize the MFRC522 object
rfid = mfrc522.MFRC522(spi, cs, rst)
rfid.set_antenna_gain(0x07 << 4)

print("\n***** Scan your RFID tag/card *****\n")

prev_data = ""

while True:
    # Request for a card
    (status, tag_type) = rfid.request(rfid.REQALL)

    if status == rfid.OK:
        # Read the UID of the card
        (status, raw_uid) = rfid.anticoll()

        if status == rfid.OK:
            rfid_data = "{:02x}{:02x}{:02x}{:02x}".format(raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3])

            # Print UID if it is different from the previous one
            if rfid_data != prev_data:
                prev_data = rfid_data
                print("Card detected! UID: {}".format(rfid_data))
