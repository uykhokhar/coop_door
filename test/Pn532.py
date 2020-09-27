"""
This example shows connecting to the PN532 with I2C (requires clock
stretching support), SPI, or UART. SPI is best, it uses the most pins but
is the most reliable and universally supported.
After initialization, try waving various 13.56MHz RFID cards over it!
"""

import board
import busio
from digitalio import DigitalInOut
from adafruit_pn532.adafruit_pn532 import MIFARE_CMD_AUTH_A, MIFARE_CMD_AUTH_B
from adafruit_pn532.spi import PN532_SPI

# SPI connection:
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
cs_pin = DigitalInOut(board.D5)
pn532 = PN532_SPI(spi, cs_pin, debug=False)


ic, ver, rev, support = pn532.firmware_version
print("Found PN532 with firmware version: {0}.{1}".format(ver, rev))

# Configure PN532 to communicate with MiFare cards
pn532.SAM_configuration()

print("Waiting for RFID/NFC card...")
while True:
    # Check if a card is available to read
    uid = pn532.read_passive_target(timeout=0.5)

    # Try again if no card is available.
    if uid is None:
        continue
    else:
        key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
        res = pn532.mifare_classic_authenticate_block(uid, 1, MIFARE_CMD_AUTH_A, key)
        print("Found card with UID:", [hex(i) for i in uid])
        print(res)
        card_data = pn532.mifare_classic_read_block(1)
        print(card_data)
        print(f"""cards says: .{card_data.decode('utf-16')}.""")
        name = bytearray('crispy', 'utf-16')
        name.append(0)
        name.append(0)
        print(len(name))
        pn532.mifare_classic_write_block(1, name)
