#program for display all files on the micro SD card
import os
import sys
import board
import busio
import digitalio
import adafruit_sdcard
import storage

# Set up SD card
SD_CS = board.GP5
spi_sd = busio.SPI(board.GP6, board.GP7, board.GP4)
cs_sd = digitalio.DigitalInOut(SD_CS)
sdcard = adafruit_sdcard.SDCard(spi_sd, cs_sd)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")

def print_directory(path, tabs=0):
    for file in os.listdir(path):
        stats = os.stat(path + "/" + file)
        filesize = stats[6]
        isdir = stats[0] & 0x4000

        if filesize < 1000:
            sizestr = str(filesize) + " by"
        elif filesize < 1000000:
            sizestr = "%0.1f KB" % (filesize / 1000)
        else:
            sizestr = "%0.1f MB" % (filesize / 1000000)

        prettyprintname = ""
        for _ in range(tabs):
            prettyprintname += "   "
        prettyprintname += file
        if isdir:
            prettyprintname += "/"
        print('{0:<40} Size: {1:>10}'.format(prettyprintname, sizestr))

        # recursively print directory contents
        if isdir:
            print_directory(path + "/" + file, tabs + 1)


print("Files on filesystem:")
print("====================")
print_directory("/sd")

