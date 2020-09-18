import board
import busio
from digitalio import DigitalInOut
from adafruit_pn532.adafruit_pn532 import MIFARE_CMD_AUTH_A, MIFARE_CMD_AUTH_B
from adafruit_pn532.spi import PN532_SPI

from door.utils import pins, config

# SPI connection:
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
cs_pin = DigitalInOut(board.D5)
pn532 = PN532_SPI(spi, cs_pin, debug=False)
key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]

ic, ver, rev, support = pn532.firmware_version
print("Found PN532 with firmware version: {0}.{1}".format(ver, rev))

# Configure PN532 to communicate with MiFare cards
pn532.SAM_configuration()


def write_tag():
    for name in config['CHICKENS']:
        print(f"\nReady to write {name}, place tag")
        cmd = input("Command ('write'(w), 'next'(n), 'exit'(e))")
        if cmd == 'w':
            read = False
            while not read:
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
                        #TODO: accomodate name > 16 bytes
                        while len(to_write) < 16:
                            to_write.append(0)
                        pn532.mifare_classic_write_block(1, to_write)
                        card_data = pn532.mifare_classic_read_block(1).decode('utf-16')
                        if card_data.rstrip('\x00') == name:
                            print(f'Sucessfully wrote {name}')
                            read = True
                        else:
                            print(card_data)
        elif cmd == 'n':
            continue
        elif cmd == 'e':
            break


def read_tag(timeout=10):
    uid = pn532.read_passive_target(timeout=timeout)
    if uid is not None:
        if pn532.mifare_classic_authenticate_block(uid, 1, MIFARE_CMD_AUTH_A, key):
            try:
                card_data = pn532.mifare_classic_read_block(1).decode('utf-16')
                name = card_data.rstrip('\x00')
                return name
            except Exception as e:
                print(e)



if __name__ == "__main__":
    cmd = input("read(r) or write(w)")
    if cmd == 'r':
        read_tag()
    elif cmd == 'w':
        write_tag()
