from mfrc522 import MFRC522
from machine import Pin, SPI
import time

sck = Pin(18)
mosi = Pin(23) 
miso = Pin(19) 
rst = Pin(27) 
cs = Pin(5)  

spi = SPI(2, baudrate=2500000, polarity=0, phase=0, sck=sck, mosi=mosi, miso=miso)

spi.init()
rdr = MFRC522(spi=spi, gpioRst=4, gpioCs=5)
print("Place card")

locked = True  # Variable to track the lock status

def read_card():
    (stat, tag_type) = rdr.request(rdr.REQIDL)
    if stat == rdr.OK:
        (stat, raw_uid) = rdr.anticoll()
        if stat == rdr.OK:
            card_id = "uid: 0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3])
            
            # Open or close the lock based on the card ID
            if card_id == "uid: 0xa4d6b15b":  # Replace with the actual card ID
                # Code to open the lock
                print("Unlocking")
                time.sleep(2)
                print("Locking")
            else:
                print("Access denied")

while True:
    read_card()
