#from door.rfid import write_tag
# from door.servo import Servo
import urllib
import http.client
from astral import LocationInfo
from astral.sun import sun
from datetime import date, datetime, timedelta
import time
from time import sleep

from gpiozero import Button, DigitalInputDevice, LED, Motor
from gpiozero import AngularServo

from RPi import GPIO
from signal import pause

# from door import log
# # from door.coop_door import CoopDoor, State
from door.counter import Counter
# # from door.rfid import read_tag
from door.utils import pins, config, notification

config = {
    "MAX_TIME_OPEN": 140,
    "MAX_TIME_CLOSE": 70,
    "CHICKENS": ["Creamy", "Crunchy", "Salty", "Saucy", "Spicy"],
    "BUFFER_TIME": 30,
    "CHECKIN_BUFFER": 30,
    "LOC_CITY": "Cleveland",
    "LOC_LATITUDE": 41.4667,
    "LOC_LONGITUDE": -81.6667,
    "LOC_TIMEZONE": "US/Eastern"
}

counter = Counter(config["CHICKENS"], pins['SEG_DATA'], pins['SEG_LATCH'],
                  pins['SEG_CLOCK'])

notification(counter.which_inside())

counter.checkin(['Creamy', "Crunchy"])

notification(f"test priority=2 {counter.which_inside()}", priority=2)

sleep(3)

notification(f"test priority=1 {counter.which_inside()}", priority=1)


print(counter.all_inside())

counter.cleanup()

# GPIO.setmode(GPIO.BCM)
#
#
# BUFFER_TIME = config["BUFFER_TIME"]  # minutes
# CHICKENS = config["CHICKENS"]
# CHECKIN_BUFFER = config["CHECKIN_BUFFER"]
#
# open_button = Button(pins["OPEN_BUTTON"])
# close_button = Button(pins["CLOSE_BUTTON"])
# open_led = LED(pins["OPEN_LED"])
# close_led = LED(pins["CLOSE_LED"])


# time

# city = LocationInfo(name=config["LOC_CITY"],
#                     region='USA',
#                     timezone=config["LOC_TIMEZONE"],
#                     latitude=config["LOC_LATITUDE"],
#                     longitude=config["LOC_LONGITUDE"])
#
# # , tzinfo=city.tzinfo
# s = sun(city.observer, date=datetime.now(city.tzinfo), tzinfo=city.tzinfo)
# open_start_time = s['sunrise'] + timedelta(hours=1)
# open_end_time = s['sunrise'] + timedelta(hours=1, minutes=config["BUFFER_TIME"])
# close_start_time = s['sunset']
# close_end_time = s['sunset'] + timedelta(minutes=config["BUFFER_TIME"])
# checkin_start_time = s['sunset'] - timedelta(minutes=config["CHECKIN_BUFFER"])
# checkin_end_time = s['sunset']
# now = datetime.now(city.tzinfo)
# now2 = datetime.now(city.tzinfo) - timedelta(hours=2, minutes=10)
#
# if (open_end_time > now2 > open_start_time):
#     print("in open")
# if (checkin_end_time > now2 > checkin_start_time):
#     print("in checkin")
# if (close_end_time > now2 > close_start_time):
#     print("in close")
#
# today = datetime.now(city.tzinfo).strftime("%m/%d/%Y")
#
# print(f"today {today}")
#
# vals = {
#     "today by city": datetime.now(city.tzinfo),
#     "sunrise": s['sunrise'],
#     "open_start_time": open_start_time, "open_end_time": open_end_time,
#     "sunset": s['sunset'],
#     "close_start_time": close_start_time, "close_end_time": close_end_time,
#     "checkin_start_time": checkin_start_time, "checkin_end_time": checkin_end_time,
#     "now": now,
#     "now2": now2}
# for k, v in vals.items():
#     print("{}: {}".format(k, v.strftime("%m/%d/%Y, %H:%M:%S")))
#
#
# conn = http.client.HTTPSConnection("api.pushover.net:443")
# conn.request("POST", "/1/messages.json",
#              urllib.parse.urlencode({
#                  "token": "abwj3qh4879xr862wgippumitfywrs",
#                  "user": "ucrggbq8tmbuv5wxa71rycvf2cqrmt",
#                  "message": "Test from coop"
#              }), {"Content-type": "application/x-www-form-urlencoded"})
# print(conn.getresponse())
#


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

# servo = Servo(18, close_angle=150)
#
#
# open_button.when_pressed = servo.open
# close_button.when_pressed = servo.close
#
# servo.open()
# servo.close()
#
# pause()


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
