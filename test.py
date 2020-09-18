#from door.rfid import write_tag
from time import sleep

from gpiozero import Button, DigitalInputDevice, LED, Motor
from door import log
from door.coop_door import CoopDoor, State
from door.counter import Counter, SevenSegmentDisplay
from door.rfid import read_tag
from door.utils import pins, config




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
display = SevenSegmentDisplay(pins['SEG_DATA'], pins['SEG_LATCH'], pins['SEG_CLOCK'])

log.debug(f"initial door open sensor value: {main_door.open_sensor.value}")
log.debug(f"initial door close sensor value: {main_door.close_sensor.value}")
log.debug(f"initial door state: {main_door.state}")


current_state = main_door.determine_state()
i = 0

display.display(i)

log.debug("checking state")
# while i < 10:
#     state = main_door.determine_state()
#
#     if state == State.OPEN:
#         log.debug('state open')
#         open_led.on()
#         close_led.off()
#     elif state == State.CLOSE:
#         log.debug('state closed')
#         open_led.off()
#         close_led.on()
#     else:
#         log.debug('state indeterminate')
#         open_led.blink()
#         close_led.blink()
#
#     if state != current_state:
#         current_state = state
#         log.debug(f"state changed to {current_state}")
#
#     display.display(i)
#     i += 1
#     sleep(1)

display.loop()
display.cleanup()
