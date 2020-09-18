from astral import LocationInfo
from astral.sun import sun
from datetime import date, datetime, timedelta
from gpiozero import Button, DigitalInputDevice, LED, Motor
from pytz import utc
from signal import pause
from time import sleep

from door import log
from door.coop_door import CoopDoor, State
from door.counter import Counter
from door.rfid import read_tag
from door.utils import pins, config


########### PARAMETERS #################

BUFFER_TIME = config["BUFFER_TIME"]  # minutes
MAX_TIME = config["MAX_TIME"]
CHICKENS = config["CHICKENS"]
CHECKIN_BUFFER = config["CHECKIN_BUFFER"]

open_button = Button(pins["OPEN_BUTTON"])
close_button = Button(pins["CLOSE_BUTTON"])
open_led = LED(pins["OPEN_LED"])
close_led = LED(pins["CLOSE_LED"])
main_door = CoopDoor(pins["MOTOR_MAIN_1"], pins["MOTOR_MAIN_2"],
                     pins["OPEN_SENSOR"], pins["CLOSE_SENSOR"],
                     max_time=MAX_TIME)
counter = Counter(CHICKENS, pins['SEG_DATA'], pins['SEG_LATCH'],
                  pins['SEG_CLOCK'])
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
        log.debug(f"close_door(): {main_door.state}")


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


while True:
    s = sun(city.observer, date=date.today())
    open_start_time = (s['sunrise'] + timedelta(
        hours=1)).replace(tzinfo=utc)
    open_end_time = (s['sunrise'] + timedelta(
        hours=1, minutes=BUFFER_TIME)).replace(tzinfo=utc)
    close_start_time = (s['sunset']).replace(tzinfo=utc)
    close_end_time = (s['sunset'] + timedelta(
        minutes=BUFFER_TIME)).replace(tzinfo=utc)
    checkin_start_time = (s['sunset'] - timedelta(
        hours=9, minutes=CHECKIN_BUFFER)).replace(tzinfo=utc)
    checkin_end_time = (s['sunset']).replace(tzinfo=utc)
    now = datetime.now().replace(tzinfo=utc)

######## RFID ##########
    if checkin_end_time > now > checkin_start_time:
        log.debug("in checkin time")
        #import pdb; pdb.set_trace()
        name = read_tag()
        if name is not None:
            counter.checkin([name])
            log.debug(f'checkin {name}')
        if counter.all_inside():
            log.debug("all_inside")
            close_door()
            #log/alert that door closed b/c all inside

######## SCHEDULE ##########
    if open_end_time > now > open_start_time:
        open_door()
        counter.reset()
        log.debug("in open period")

    if close_end_time > now > close_start_time:
        close_door()
        # alert that door closed with schedule
        log.debug("in sunset time")


# cleanup segment display display.cleanup(), cleanup all pins
pause()
