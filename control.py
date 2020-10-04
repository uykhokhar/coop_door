from astral import LocationInfo
from astral.sun import sun
from datetime import date, datetime, timedelta
from gpiozero import AngularServo, Button, DigitalInputDevice, LED, Motor
from pytz import utc
from RPi import GPIO
from signal import pause
from time import sleep

from door import log
from door.coop_door import CoopDoor, State
from door.counter import Counter
from door.rfid import RFID
from door.servo import Servo
from door.utils import pins, config


########### PARAMETERS #################

BUFFER_TIME = config["BUFFER_TIME"]  # minutes
CHECKIN_BUFFER = config["CHECKIN_BUFFER"]

open_button = Button(pins["OPEN_BUTTON"])
close_button = Button(pins["CLOSE_BUTTON"])
open_led = LED(pins["OPEN_LED"])
close_led = LED(pins["CLOSE_LED"])
main_door = CoopDoor(pins["MOTOR_MAIN_1"], pins["MOTOR_MAIN_2"],
                     pins["OPEN_SENSOR"], pins["CLOSE_SENSOR"],
                     max_time_open=config["MAX_TIME_OPEN"],
                     max_time_close=config["MAX_TIME_CLOSE"])
counter = Counter(config["CHICKENS"], pins['SEG_DATA'], pins['SEG_LATCH'],
                  pins['SEG_CLOCK'])
reader = RFID()
food_servo = Servo(pins['FOOD_SERVO'], open_angle=135, close_angle=65)
city = LocationInfo(name=config["LOC_CITY"],
                    region='USA',
                    timezone=config["LOC_TIMEZONE"],
                    latitude=config["LOC_LATITUDE"],
                    longitude=config["LOC_LONGITUDE"])


log.debug(f"initial door open sensor value: {main_door.open_sensor.value}")
log.debug(f"initial door close sensor value: {main_door.close_sensor.value}")
log.debug(f"initial door state: {main_door.state}")


########### METHODS #################

def open_door():
    # TODO: reset counter of chickens
    open_led.blink()
    close_led.off()
    if main_door.open() == State.OPEN:
        log.info("door control: opened")
        open_led.on()
    else:
        open_led.blink()
        close_led.blink()
        log.debug(f"open_door(): {main_door.state}")


def close_door():
    # TODO: if all chickens not in, send message
    close_led.blink()
    open_led.off()
    if main_door.close() == State.CLOSE:
        close_led.on()
        log.info("door control: closed")
    else:
        open_led.blink()
        close_led.blink()
        log.info(f"close_door(): {main_door.state}")
        # todo: Alert that door didn't close


def cleanup():
    GPIO.cleanup()


########### MAIN #################

if main_door.state == State.OPEN:
    open_led.on()
    close_led.off()
elif main_door.state == State.CLOSE:
    open_led.off()
    close_led.on()
else:
    open_led.blink()
    close_led.blink()


######## MANUAL CONTROL ##########
open_button.when_pressed = open_door
close_button.when_pressed = close_door


def loop():
    while True:
        s = sun(city.observer, date=date.today(), tzinfo=city.tzinfo)
        open_start_time = s['sunrise'] + timedelta(hours=1)
        open_end_time = s['sunrise'] + timedelta(hours=1, minutes=BUFFER_TIME)
        close_start_time = s['sunset']
        close_end_time = s['sunset'] + timedelta(minutes=BUFFER_TIME)
        checkin_start_time = s['sunset'] - timedelta(minutes=CHECKIN_BUFFER)
        checkin_end_time = s['sunset']
        now = datetime.now(city.tzinfo)

    ######## RFID ##########
        if (checkin_end_time > now > checkin_start_time) \
                & (main_door.state != State.CLOSE):
            log.info("in checkin time")
            name = reader.read_tag(timeout=10)  # wait timeout or return name
            if name is not None:
                counter.checkin([name])
                log.info(f'checkin {name}')
            if counter.all_inside():
                log.info("all_inside")
                sleep(60)
                close_door()
                food_servo.close()
                # log/alert that door closed b/c all inside

    ######## SCHEDULE ##########
        if (open_end_time > now > open_start_time) \
                & (main_door.state != State.OPEN):
            log.info(f"in open period: {open_start_time} - {open_end_time}")
            open_door()
            counter.reset()
            food_servo.open()  # open

        if (close_end_time > now > close_start_time) \
                & (main_door.state != State.CLOSE):
            log.info(f"in sunset time: {close_start_time} - {close_end_time}")
            close_door()
            food_servo.close()  # close
            # alert that door closed with schedule

        # sleep(120)  # only if RFID reading not setup


if __name__ == '__main__':
    print('Program is starting...')
    try:
        loop()
    except KeyboardInterrupt:
        cleanup()
