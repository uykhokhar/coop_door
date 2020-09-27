import sys

from door.rfid import RFID
from door.utils import config

reader = RFID()


def loop():
    while True:
        cmd = input("read(r) or write(w)")
        if cmd == 'r':
            print(reader.read_tag())
        elif cmd == 'w':
            for name in config['CHICKENS']:
                print(f"\nReady to write {name}, place tag")
                cmd = input("Command ('write'(w), 'next'(n), 'exit'(e))")
                if cmd == 'w':
                    reader.write_tag(name)
                elif cmd == 'n':
                    continue
                elif cmd == 'e':
                    break


if __name__ == "__main__":
    try:
        loop()
    except KeyboardInterrupt:
        sys.exit()
