from gpiozero import Button, DigitalInputDevice, LED, Motor
from signal import pause
from time import sleep

from coop_door import CoopDoor, State
from utils import pins

open_button = Button(pins["OPEN_BUTTON"])
close_button = Button(pins["CLOSE_BUTTON"])
open_led = LED(pins["OPEN_LED"])
close_led = LED(pins["CLOSE_LED"])

main_door = CoopDoor(pins["MOTOR_MAIN_1"], pins["MOTOR_MAIN_2"],
                     pins["OPEN_SENSOR"], pins["CLOSE_SENSOR"],
                     max_time=5)

print(main_door.open_sensor.value)
print(main_door.close_sensor.value)
print(main_door.state)

def open():
    open_led.blink()
    close_led.off()
    res = main_door.open()
    if res == State.OPEN:
        print("door control: state opened")
        open_led.on()
    else:
        open_led.blink()
        close_led.blink()

def close():
    close_led.blink()
    open_led.off()
    res = main_door.close()
    if res == State.CLOSE:
        print("door control: state closed")
        close_led.on()
    else:
        open_led.blink()
        close_led.blink()

open_button.when_pressed = open
close_button.when_pressed = close

print("done")
open_led.off()
pause()
