
from enum import Enum
from gpiozero import DigitalInputDevice, Motor
from signal import pause
from time import perf_counter

from utils import log

class State(Enum):
    OPEN = 1
    CLOSE = 2
    INTERMEDIATE = 5


class CoopDoor():

    def __init__(self, motor_forward, motor_backward, open_sensor, close_sensor, max_time=45):
        self.max_time = max_time
        self.motor = Motor(motor_forward, motor_backward)
        self.open_sensor = DigitalInputDevice(open_sensor)
        self.close_sensor = DigitalInputDevice(close_sensor)
        self.state = self.determine_state()

    def close(self):
        start = perf_counter()
        if self.determine_state() != State.CLOSE:
            while (self.state != State.CLOSE) & ((perf_counter() - start) < self.max_time):
                self.motor.forward()
                self.state = self.determine_state()
            else:
                self.motor.stop()
        return self.state

    def open(self):
        start = perf_counter()
        self.state = self.determine_state()
        log.debug(f"door.open() state: {self.state}")
        if self.state != State.OPEN:
            while (self.state != State.OPEN) & ((perf_counter() - start) < self.max_time):
                self.motor.backward()
                self.state = self.determine_state()
            else:
                self.motor.stop()
        return self.state

    def determine_state(self):
        state = None
        if self.open_sensor.value == 0:
            state = State.OPEN
        elif self.close_sensor.value == 0:
            state = State.CLOSE
        else:
            state = State.INTERMEDIATE
        return state
