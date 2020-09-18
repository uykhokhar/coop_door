from RPi import GPIO
from time import perf_counter

from rfid_reader.MFRC522 import MFRC522


MIFAREReader = MFRC522()


def scan_cards(seconds=60):

    start = perf_counter()
    vals = []

    while (perf_counter() - start) < seconds:
        (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

        # If a card is found
        if status == MIFAREReader.MI_OK:
            print("Card detected")

        # Get the UID of the card
        (status, uid) = MIFAREReader.MFRC522_Anticoll()

        # If we have the UID, continue
        if status == MIFAREReader.MI_OK:

            # Print UID
            print("Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3]))

            # This is the default key for authentication
            key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

            # Select the scanned tag
            MIFAREReader.MFRC522_SelectTag(uid)

            # Authenticate
            status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)

            # Check if authenticated
            if status == MIFAREReader.MI_OK:
                MIFAREReader.MFRC522_DumpClassic1K()
                val = MIFAREReader.MFRC522_Returnstr(0)
                vals.append(val)
                MIFAREReader.MFRC522_StopCrypto1()
            else:
                print("Authentication error")
    GPIO.cleanup()
    return vals


class Counter():

    chickens = {}
    # TODO: checkin times = {}

    def __init__(self, names, dataPin, latchPin, clockPin):
        self.names = names
        self.segment = SevenSegmentDisplay(dataPin, latchPin, clockPin)
        self.reset()

    def reset(self):
        self.chickens = {n: False for n in self.names}

    def checkin(self, names):
        for c in names:
            self.chickens[c] = True
        self.segment.display(self.count())

    def count(self):
        return sum(self.chickens.values())

    def all_inside(self):
        return sum(self.chickens.values()) == len(self.chickens)


class SevenSegmentDisplay():

    num_hex = {0: 0xc0,
               1: 0xf9,
               2: 0xa4,
               3: 0xb0,
               4: 0x99,
               5: 0x92,
               6: 0x82,
               7: 0xf8,
               8: 0x80,
               9: 0x90}

    def __init__(self, dataPin, latchPin, clockPin):
        self.dataPin = dataPin
        self.latchPin = latchPin
        self.clockPin = clockPin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.dataPin, GPIO.OUT)
        GPIO.setup(self.latchPin, GPIO.OUT)
        GPIO.setup(self.clockPin, GPIO.OUT)

    def display(self, num):
        val = self.num_hex[num]
        GPIO.output(self.latchPin, GPIO.LOW)
        for i in range(0, 8):
            GPIO.output(self.clockPin, GPIO.LOW)
            GPIO.output(self.dataPin, (0x80 & (val << i) == 0x80) and GPIO.HIGH or GPIO.LOW)
            GPIO.output(self.clockPin, GPIO.HIGH)
        GPIO.output(self.latchPin, GPIO.HIGH)

    def cleanup(self):
        GPIO.cleanup()
