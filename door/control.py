from astral import LocationInfo
from astral.sun import sun
from datetime import date, datetime, timedelta
from gpiozero import Button, DigitalInputDevice, LED, Motor
from pytz import utc
from signal import pause
from time import sleep

from coop_door import CoopDoor, State
from utils import pins, config

open_button = Button(pins["OPEN_BUTTON"])
close_button = Button(pins["CLOSE_BUTTON"])
open_led = LED(pins["OPEN_LED"])
close_led = LED(pins["CLOSE_LED"])
BUFFER_TIME = config["BUFFER_TIME"]  # minutes
MAX_TIME = config["MAX_TIME"]
CHICKENS = config["CHICKENS"]


main_door = CoopDoor(pins["MOTOR_MAIN_1"], pins["MOTOR_MAIN_2"],
                     pins["OPEN_SENSOR"], pins["CLOSE_SENSOR"],
                     max_time=MAX_TIME)

city = LocationInfo(name='Cleveland', region='USA', timezone='US/Eastern',
                    latitude=41.4667, longitude=-81.6667)

print(main_door.open_sensor.value)
print(main_door.close_sensor.value)
print(main_door.state)

if main_door.state == State.OPEN:
    open_led.on()
    close_led.off()
elif main_door.state == State.CLOSE:
    open_led.off()
    close_led.on()
else:
    open_led.blink()
    close_led.blink()

# TODO: open and close log method of open and close


def open():
    # TODO: reset counter of chickens
    open_led.blink()
    close_led.off()
    if main_door.open() == State.OPEN:
        print("door control: state opened")
        open_led.on()
    else:
        open_led.blink()
        close_led.blink()


def close():
    # TODO: if all chickens not in, send message
    close_led.blink()
    open_led.off()
    if main_door.close() == State.CLOSE:
        print("door control: state closed")
        close_led.on()
    else:
        open_led.blink()
        close_led.blink()


######## MANUAL CONTROL ##########
open_button.when_pressed = open
close_button.when_pressed = close


while True:
    ######## SCHEDULE ############
    s = sun(city.observer, date=date.today())
    open_start_time = (s['sunrise'] + timedelta(hours=1)).replace(tzinfo=utc)
    open_end_time = (s['sunrise'] + timedelta(hours=1, minutes=BUFFER_TIME)).replace(tzinfo=utc)
    close_start_time = (s['sunset']).replace(tzinfo=utc)
    close_end_time = (s['sunset'] + timedelta(minutes=BUFFER_TIME)).replace(tzinfo=utc)
    now = datetime.now().replace(tzinfo=utc)

    # try reading for 60 seconds
    # read card --> chicken name
    # if name not none, counter.checkin()
    # if counter.all_inside: close()

    if open_end_time > now > open_start_time:
        open()
        # counter.reset()
        print("in period")

    if close_end_time > now > close_start_time:
        close()
        # alert that door closed with schedule
        print('in end time')

    sleep(60)
    print('test of buttons')


# cleanup segment display display.cleanup(), cleanup all pins


print("done")
pause()
