import time
import json
import hashlib
from mfrc522 import MFRC522
from machine import Pin
from machine import SPI

# Load JSON data from the file
with open("database.json", "r") as json_file:
    json_data = json.load(json_file)

sck = 18
mosi = 23
miso = 19
rst = 27
cs = 5

spi = SPI(2, baudrate=2500000, polarity=0, phase=0, sck=Pin(sck), mosi=Pin(mosi), miso=Pin(miso))

spi.init()
rdr = MFRC522(spi=spi, gpioRst=4, gpioCs=5)
print("Place card")

card_id = "None"
lock = False

while True:
    (stat, tag_type) = rdr.request(rdr.REQIDL)
    if stat == rdr.OK:
        (stat, raw_uid) = rdr.anticoll()
        if stat == rdr.OK:
            card_id = "uid: 0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3])
            card_id = str(card_id)
            hash_object = hashlib.sha256(card_id.encode())
            hashed_string = ''.join('%02x' % byte for byte in hash_object.digest())

            for i in range(len(json_data["keys_true"])):
                if json_data["keys_true"][i]["key"] == hashed_string:
                    lock = True
                    break

            # Open or close the lock based on the card ID
            if lock == True:
                # Code to open the lock
                print("Unlocking")
                time.sleep(2)
                print("Locking")
            else:
                print("Access denied")
