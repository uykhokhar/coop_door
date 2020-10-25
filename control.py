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
from door.utils import pins, config, notification


########### PARAMETERS #################
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


log.info(f"initial door open sensor value: {main_door.open_sensor.value}")
log.info(f"initial door close sensor value: {main_door.close_sensor.value}")
log.info(f"initial door state: {main_door.state}")


########### METHODS #################

def open_door():
    open_led.blink()
    close_led.off()
    if main_door.open() == State.OPEN:
        log.info("door control: opened")
        notification("Door opened")
        open_led.on()
    else:
        open_led.blink()
        close_led.blink()
        log.debug(f"open_door(): {main_door.state}")
        notification("Door in intermediate state while opening",
                     priority=2)  # priority=2 sometimes not working
        sleep(3)
        notification("Door in intermediate state while opening", priority=1)


def close_door():
    close_led.blink()
    open_led.off()
    if main_door.close() == State.CLOSE:
        close_led.on()
        log.info("door control: closed")
        notification("Door closed")
    else:
        open_led.blink()
        close_led.blink()
        log.info(f"close_door(): {main_door.state}")
        notification("Door intermediate state while closing",
                     priority=2)  # priority=2 sometimes not working
        sleep(3)
        notification("Door intermediate state while closing", priority=1)  # alert level high


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
        # local time used to account for daylight savings time in calculation
        # of local sunset/sunrise
        s = sun(city.observer, date=datetime.now(city.tzinfo), tzinfo=city.tzinfo)
        open_start_time = s['sunrise'] + timedelta(minutes=45)
        open_end_time = s['sunrise'] + timedelta(minutes=45 + config["BUFFER_TIME"])
        close_start_time = s['sunset']
        close_end_time = s['sunset'] + timedelta(minutes=config["BUFFER_TIME"])
        checkin_start_time = s['sunset'] - timedelta(minutes=config["CHECKIN_BUFFER"])
        checkin_end_time = s['sunset']
        now = datetime.now(city.tzinfo)

    ######## RFID ##########
        if (checkin_end_time > now > checkin_start_time) \
                & (main_door.state != State.CLOSE):
            log.debug("in checkin time")
            name = reader.read_tag(timeout=10)  # wait timeout or return name
            if name is not None:
                counter.checkin([name])
                log.info(f'checkin {name}')
                notification(f"{name} checked-in")
            if counter.all_inside():
                log.info("all_inside")
                notification("All chickens checked-in")
                sleep(60)
                close_door()
                food_servo.close()

    ######## SCHEDULE ##########
        if (open_end_time > now > open_start_time) \
                & (main_door.state != State.OPEN):
            s_ost = open_start_time.strftime("%H:%M")
            s_oet = open_end_time.strftime("%H:%M")
            message = f"In scheduled open time: {s_ost} - {s_oet}"
            log.debug(message)
            notification(message)
            open_door()
            counter.reset()
            food_servo.open()

        if (close_end_time > now > close_start_time) \
                & (main_door.state == State.OPEN):
            s_cst = close_start_time.strftime("%H:%M")
            s_cet = close_end_time.strftime("%H:%M")
            message = (f"In scheduled close time: {s_cst} - {s_cet}. "
                       f"{counter.which_inside()}")
            log.debug(message)
            notification(message, priority=1)
            close_door()
            food_servo.close()


if __name__ == '__main__':
    log.info('Program is starting...')
    try:
        loop()
    except KeyboardInterrupt:
        cleanup()
