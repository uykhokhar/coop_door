from enum import Enum
from gpiozero import DigitalInputDevice, Motor
from signal import pause
from time import perf_counter

from door import log


class State(Enum):
    OPEN = 1
    CLOSE = 2
    INTERMEDIATE = 5


class CoopDoor():

    def __init__(self, motor_forward, motor_backward, open_sensor,
                 close_sensor, max_time_open=60, max_time_close=45):
        self.max_time_open = max_time_open
        self.max_time_close = max_time_close
        self.motor = Motor(motor_forward, motor_backward)
        self.open_sensor = DigitalInputDevice(open_sensor)
        self.close_sensor = DigitalInputDevice(close_sensor)
        self.determine_state()

    def close(self):
        start = perf_counter()
        self.determine_state()
        log.debug(f"door.close() state: {self.state}")
        if self.state != State.CLOSE:
            while (self.state != State.CLOSE) \
                    & ((perf_counter() - start) < self.max_time_close):
                self.motor.forward()
                self.determine_state()
            else:
                self.motor.stop()
        return self.state

    def open(self):
        start = perf_counter()
        self.determine_state()
        log.debug(f"door.open() state: {self.state}")
        if self.state != State.OPEN:
            while (self.state != State.OPEN) \
                    & ((perf_counter() - start) < self.max_time_open):
                self.motor.backward()
                self.determine_state()
            else:
                self.motor.stop()
        return self.state

    def determine_state(self):
        if self.open_sensor.value == 0:
            self.state = State.OPEN
        elif self.close_sensor.value == 0:
            self.state = State.CLOSE
        else:
            self.state = State.INTERMEDIATE
        return self.state
