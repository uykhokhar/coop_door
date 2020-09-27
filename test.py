#from door.rfid import write_tag
from door.servo import Servo
import time
from time import sleep

from gpiozero import Button, DigitalInputDevice, LED, Motor
from gpiozero import AngularServo

from RPi import GPIO
from signal import pause

from door import log
# from door.coop_door import CoopDoor, State
# from door.counter import Counter, SevenSegmentDisplay
# from door.rfid import read_tag
from door.utils import pins, config


GPIO.setmode(GPIO.BCM)


BUFFER_TIME = config["BUFFER_TIME"]  # minutes
CHICKENS = config["CHICKENS"]
CHECKIN_BUFFER = config["CHECKIN_BUFFER"]

open_button = Button(pins["OPEN_BUTTON"])
close_button = Button(pins["CLOSE_BUTTON"])
open_led = LED(pins["OPEN_LED"])
close_led = LED(pins["CLOSE_LED"])

#
# servo = AngularServo(18, initial_angle=None, min_angle=-90, max_angle=90,
#                      min_pulse_width=0.0005, max_pulse_width=0.0025)
# sleep(2)
# print(servo.min_pulse_width)
# print(servo.max_pulse_width)
#
#
# servo.angle = -90
# sleep(15)
# servo.angle = 80
# sleep(15)


# OFFSE_DUTY = 0.5  # define pulse offset of servo
# SERVO_MIN_DUTY = 2.5+OFFSE_DUTY  # define pulse duty cycle for minimum angle of servo
# SERVO_MAX_DUTY = 12.5+OFFSE_DUTY  # define pulse duty cycle for maximum angle of servo
# servoPin = 18
#
#
# def map(value, fromLow, fromHigh, toLow, toHigh):  # map a value from one range to another range
#     return (toHigh-toLow)*(value-fromLow) / (fromHigh-fromLow) + toLow
#
#
# global p
# GPIO.setmode(GPIO.BCM)         # use PHYSICAL GPIO Numbering
# GPIO.setup(servoPin, GPIO.OUT)   # Set servoPin to OUTPUT mode
# GPIO.output(servoPin, GPIO.LOW)  # Make servoPin output LOW level
#
# p = GPIO.PWM(servoPin, 50)     # set Frequece to 50Hz
# p.start(0)                     # Set initial Duty Cycle to 0
#
#
# def servoWrite(angle):      # make the servo rotate to specific angle, 0-180
#     if(angle < 0):
#         angle = 0
#     elif(angle > 180):
#         angle = 180
#     p.ChangeDutyCycle(map(angle, 0, 180, SERVO_MIN_DUTY, SERVO_MAX_DUTY)
#                       )  # map the angle to duty cycle and output it
#
#
# def open_button_pressed():
#     print("0 to 180")  # close
#     for dc in range(0, 181, 1):   # make servo rotate from 0 to 180 deg
#         servoWrite(dc)     # Write dc value to servo
#         time.sleep(0.001)
#
#
# def close_button_pressed():
#     print("180 to 0")  # opens
#     for dc in range(180, -1, -1):  # make servo rotate from 180 to 0 deg
#         servoWrite(dc)
#         time.sleep(0.001)
#     time.sleep(5)
#
#
# open_button_pressed()
# sleep(5)
# close_button_pressed()
# sleep(5)
#
# open_button.when_pressed = open_button_pressed
# close_button.when_pressed = close_button_pressed
#
# pause()

# TEST SERVO CLASS

servo = Servo(18, close_angle=150)


open_button.when_pressed = servo.open
close_button.when_pressed = servo.close

servo.open()
servo.close()

pause()


# print("min max test")
# servo.min()
# sleep(5)
# servo.mid()
# sleep(5)
# servo.max()
# sleep(5)
# servo.mid()
# sleep(5)
# GPIO.cleanup()
# main_door = CoopDoor(pins["MOTOR_MAIN_1"], pins["MOTOR_MAIN_2"],
#                      pins["OPEN_SENSOR"], pins["CLOSE_SENSOR"],
#                      max_time=MAX_TIME)
# display = SevenSegmentDisplay(pins['SEG_DATA'], pins['SEG_LATCH'], pins['SEG_CLOCK'])
#
# log.debug(f"initial door open sensor value: {main_door.open_sensor.value}")
# log.debug(f"initial door close sensor value: {main_door.close_sensor.value}")
# log.debug(f"initial door state: {main_door.state}")


# open_sensor = DigitalInputDevice(pins["OPEN_SENSOR"])
# close_sensor = DigitalInputDevice(pins["CLOSE_SENSOR"])
#
# ov = open_sensor.value
# cv = close_sensor.value
#
# print(f"open_sensor initial {ov}")
# print(f"close initial {cv}")
#
# while True:
#     if open_sensor.value != ov:
#         ov = open_sensor.value
#         print(f"open_sensor: {open_sensor.value}")
#     if close_sensor.value != cv:
#         cv = close_sensor.value
#         print(f"close_sensor: {close_sensor.value}")


# now = (s['sunset'] - timedelta(minutes=(CHECKIN_BUFFER - 3))).replace(tzinfo=utc)


#
# current_state = main_door.determine_state()
# i = 0
#
# display.display(i)
#
# log.debug("checking state")
# # while i < 10:
# #     state = main_door.determine_state()
# #
# #     if state == State.OPEN:
# #         log.debug('state open')
# #         open_led.on()
# #         close_led.off()
# #     elif state == State.CLOSE:
# #         log.debug('state closed')
# #         open_led.off()
# #         close_led.on()
# #     else:
# #         log.debug('state indeterminate')
# #         open_led.blink()
# #         close_led.blink()
# #
# #     if state != current_state:
# #         current_state = state
# #         log.debug(f"state changed to {current_state}")
# #
# #     display.display(i)
# #     i += 1
# #     sleep(1)
# display.display(4)
# sleep(2)
# display.display(6)
# sleep(1)
# display.display(5)
#
# for num in range(9, -1, -1):
#     display.display(num)
#     sleep(2)
# display.cleanup()
