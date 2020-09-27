import board
import busio
from digitalio import DigitalInOut
import os

from adafruit_pn532.adafruit_pn532 import MIFARE_CMD_AUTH_A as AUTH
from adafruit_pn532.spi import PN532_SPI

from door import log


class RFID:

    key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

    def __init__(self):
        # SPI connection:
        spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
        cs_pin = DigitalInOut(board.D5)
        self.pn532 = PN532_SPI(spi, cs_pin, debug=False)
        ic, ver, rev, support = self.pn532.firmware_version
        log.info(f"Found PN532 with firmware version: {ver}.{rev}")

        # Configure PN532 to communicate with MiFare cards
        self.pn532.SAM_configuration()

    def write_tag(self, name):
        cont_read = False
        while not cont_read:
            uid = self.pn532.read_passive_target(timeout=0.5)
            if uid is None:
                continue
            else:
                res = self.pn532.mifare_classic_authenticate_block(
                    uid, 1, AUTH, self.key)
                card_data = self.pn532.mifare_classic_read_block(1).decode('utf-16')
                if card_data == name:
                    print(f"Card already has {name}")
                else:
                    to_write = bytearray(name, 'utf-16')
                    # TODO: accomodate name > 16 bytes
                    while len(to_write) < 16:
                        to_write.append(0)
                    self.pn532.mifare_classic_write_block(1, to_write)
                    card_data = self.pn532.mifare_classic_read_block(1).decode('utf-16')
                    if card_data.rstrip('\x00') == name:
                        print(f'Sucessfully wrote {name}')
                        cont_read = True
                    else:
                        print(card_data)

    def read_tag(self, timeout=10):
        uid = self.pn532.read_passive_target(timeout=timeout)
        if uid is not None:
            if self.pn532.mifare_classic_authenticate_block(uid, 1, AUTH, self.key):
                try:
                    card_data = self.pn532.mifare_classic_read_block(1).decode('utf-16')
                    name = card_data.rstrip('\x00')
                    return name
                except Exception as e:
                    log.error(e)
