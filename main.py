import time
import json
import hashlib
from mfrc522 import MFRC522
from machine import Pin, SPI
import network
import usocket as socket
import ujson as json
import _thread


# Load JSON data from the file
with open("database.json", "r") as json_file:
    json_data = json.load(json_file)

# Set up Wi-Fi connection
ssid = "iphone"
password = "ahmed12345"
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
lk = Pin(32, Pin.OUT)

spi = SPI(2, baudrate=2500000, polarity=0, phase=0, sck=Pin(sck), mosi=Pin(mosi), miso=Pin(miso))
spi.init()
rdr = MFRC522(spi=spi, gpioRst=4, gpioCs=5)


def run_server(): # Create an instance of the Pin class
    if lk.value() == 1:
        lk_state = "locked"
    else:
        lk_state = "unlocked"

    with open("index.html", "r") as file:
        html = file.read()
        html = html.replace("{{lock_state}}", lk_state)

    return html 


# Function to handle incoming HTTP requests
def handle_request(conn):
    request = conn.recv(1024).decode('utf-8')

    if 'POST /lock' in request:
        # Code to lock the RFID lock
        lock = True
        conn.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n")
        conn.close()
        return

    if 'POST /unlock' in request:
        # Code to unlock the RFID lock
        lock = False
        conn.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n")
        conn.close()
        return

    # # Build HTML content from JSON data
    # html_content = "<html><body><h2>Keys True:</h2><ul>"
    # for key_info in json_data["keys_true"]:
    #     html_content += f"<li>ID: {key_info['id']}, Key: {key_info['key']}</li>"
    # html_content += "</ul><h2>Key False:</h2><ul>"
    # for key_info in json_data["keys_false"]:
    #     html_content += f"<li>ID: {key_info['id']}, Key: {key_info['key']}</li>"
    # html_content += "</ul></body></html>"

    # Send HTTP response
    html = run_server()
    conn.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n")
    conn.sendall(html)
    conn.close()


# Set up a socket for the web server
web_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
web_socket.bind(('', 80))
web_socket.listen(5)

print("Connected to Wi-Fi")
print("ESP32 IP address:", station.ifconfig()[0])

while True:
    # Accept incoming connections and handle requests
    conn, addr = web_socket.accept()
    handle_request(conn)

    # Start the server thread
    _thread.start_new_thread(run_server, ())

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

                # Check if the card ID is in the list of registered keys
                if any(key_info["key"] == hashed_string for key_info in json_data["keys_true"]):
                    lock = True
                else:
                    lock = False

                # Open or close the lock based on the card ID
                if lock:
                    # Code to open the lock
                    print("Unlocking")
                    time.sleep(2)
                    print("Locking")
                else:
                    print("Access denied")

                    if any(key_info["key"] == hashed_string for key_info in json_data["keys_false"]):
                        print("NO")
                    else:
                
                        # Save the denied card in the JSON file
                        denied_card = {"id": card_id, "key": hashed_string}
                    
                        json_data["keys_false"].append(denied_card)
                        print(json_data)

                        # Update the JSON file
                        with open("database.json", "w") as json_file:
                            json.dump(json_data, json_file)

        time.sleep(0.1) # Sleep to avoid high CPU usage
        handle_request(conn)
