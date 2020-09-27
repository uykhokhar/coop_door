from RPi import GPIO
from time import sleep

from door import log


class Servo():

    def __init__(self, pin, min_duty=2.5, max_duty=12.5, min_angle=0,
                 max_angle=180, open_angle=0, close_angle=160):
        self.pin = pin
        self.open_angle = open_angle
        self.close_angle = close_angle
        self.min_angle = min_angle
        self.max_angle = max_angle
        OFFSE_DUTY = 0.5  # define pulse offset of servo
        self.min_duty = 2.5+OFFSE_DUTY  # pulse duty cycle for minimum angle of servo
        self.max_duty = 12.5+OFFSE_DUTY
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)   # Set servoPin to OUTPUT mode
        GPIO.output(pin, GPIO.LOW)
        self.p = GPIO.PWM(pin, 50)     # set Frequece to 50Hz
        self.p.start(0)

    def calc_pulse_duty(self, angle):
        return (self.max_duty - self.min_duty) * (angle - self.min_angle) \
            / (self.max_angle - self.min_angle) + self.min_duty

    def move(self, from_angle, to_angle, incr):
        for angle in range(from_angle, to_angle, incr):
            self.p.ChangeDutyCycle(self.calc_pulse_duty(angle))
            sleep(0.001)

    def open(self):
        log.debug("open servo")
        self.move(self.close_angle, self.open_angle, -1)

    def close(self):
        log.debug("close servo")
        self.move(self.open_angle, self.close_angle, 1)
