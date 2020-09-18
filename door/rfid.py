import board
import busio
from digitalio import DigitalInOut
from adafruit_pn532.adafruit_pn532 import MIFARE_CMD_AUTH_A, MIFARE_CMD_AUTH_B
from adafruit_pn532.spi import PN532_SPI

from utils import config, pins

# SPI connection:
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
cs_pin = DigitalInOut(board.D5)
pn532 = PN532_SPI(spi, cs_pin, debug=False)
key = config['RFID_KEY']

ic, ver, rev, support = pn532.firmware_version
print("Found PN532 with firmware version: {0}.{1}".format(ver, rev))

# Configure PN532 to communicate with MiFare cards
pn532.SAM_configuration()


def write_tag():
    for name in config['CHICKENS']:
        print(f"Ready to write {name}, place tag")
        cmd = input("Command ('write', 'exit')")
        if cmd == 'write':
            while True:
                uid = pn532.read_passive_target(timeout=0.5)
                if uid is None:
                    continue
                else:
                    res = pn532.mifare_classic_authenticate_block(
                        uid, 1,
                        MIFARE_CMD_AUTH_A,
                        key)
                    card_data = pn532.mifare_classic_read_block(1).decode('utf-16')
                    if card_data == name:
                        print(f"Card already has {name}")
                    else:
                        to_write = bytearray(name, 'utf-16')
                        while len(to_write) <= 16:
                            to_write.append(0)
                        pn532.mifare_classic_write_block(1, to_write)
                        card_data = pn532.mifare_classic_read_block(1).decode('utf-16')
                        if card_data == name:
                            print(f'Sucessfully wrote {name}')
        elif cmd == 'exit':
            break


def read_tag():
    pass
