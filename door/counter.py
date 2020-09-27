from RPi import GPIO
from time import perf_counter, sleep


class Counter():

    chickens = {}
    # TODO: checkin times = {}

    def __init__(self, names, dataPin, latchPin, clockPin):
        self.names = names
        self.segment = SevenSegmentDisplay(dataPin, latchPin, clockPin)
        self.reset()

    def _count(self):
        return sum(self.chickens.values())

    def reset(self):
        self.chickens = {n: False for n in self.names}
        self.segment.display(self._count())

    def checkin(self, names):
        for c in names:
            self.chickens[c] = True
        self.segment.display(self._count())

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

    def __init__(self, data_pin, latch_pin, clock_pin):
        self.data_pin = data_pin
        self.latch_pin = latch_pin
        self.clock_pin = clock_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.data_pin, GPIO.OUT)
        GPIO.setup(self.latch_pin, GPIO.OUT)
        GPIO.setup(self.clock_pin, GPIO.OUT)

    def display(self, num):
        val = self.num_hex[num]
        GPIO.output(self.latch_pin, GPIO.LOW)
        for i in range(0, 8):
            GPIO.output(self.clock_pin, GPIO.LOW)
            GPIO.output(self.data_pin, (0x80 & (val << i) == 0x80) and GPIO.HIGH or GPIO.LOW)
            GPIO.output(self.clock_pin, GPIO.HIGH)
        GPIO.output(self.latch_pin, GPIO.HIGH)

    def cleanup(self):
        GPIO.cleanup()
