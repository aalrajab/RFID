import time
import json
import hashlib
from mfrc522 import MFRC522
from machine import Pin
from machine import SPI
import network
import usocket as socket
import ujson as json

# Load JSON data from the file
with open("database.json", "r") as json_file:
    json_data = json.load(json_file)

# Set up Wi-Fi connection
ssid = "ssid"
password = "password"
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)

# Wait until connected to Wi-Fi
while not station.isconnected():
    pass

# Set up the MFRC522 RFID reader
sck = 18
mosi = 23
miso = 19
rst = 27
cs = 5

spi = SPI(2, baudrate=2500000, polarity=0, phase=0, sck=Pin(sck), mosi=Pin(mosi), miso=Pin(miso))
spi.init()
rdr = MFRC522(spi=spi, gpioRst=4, gpioCs=5)

# Function to handle incoming HTTP requests
def handle_request(conn):
    response_headers = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"

    # Build HTML content from JSON data
    html_content = "<html><body><h2>Keys True:</h2><ul>"
    for key_info in json_data["keys_true"]:
        html_content += f"<li>ID: {key_info['id']}, Key: {key_info['key']}</li>"
    html_content += "</ul><h2>Key False:</h2><ul>"
    for key_info in json_data["key_false"]:
        html_content += f"<li>ID: {key_info['id']}, Key: {key_info['key']}, Date: {key_info['date']}</li>"
    html_content += "</ul></body></html>"

    # Send HTTP response
    conn.send(response_headers)
    conn.send(html_content)
    conn.close()

# Set up a socket for the web server
web_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
web_socket.bind(('', 80))
web_socket.listen(5)

print("Connected to Wi-Fi")
print("ESP32 IP address:", station.ifconfig()[0])

card_id = "None"
lock = False

while True:
    # Check RFID card ID
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
            if lock:
                # Code to open the lock
                print("Unlocking")
                time.sleep(2)
                print("Locking")
            else:
                print("Access denied")
