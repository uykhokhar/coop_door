#!/usr/bin/env python3
#############################################################################
# Filename    : SevenSegmentDisplay.py
# Description : Control SevenSegmentDisplay with 74HC595
# Author      : www.freenove.com
# modification: 2019/12/27
########################################################################
import RPi.GPIO as GPIO
import time

LSBFIRST = 1
MSBFIRST = 2
# define the pins for 74HC595
dataPin   = 7   #GPIO4   # DS Pin of 74HC595(Pin14)
latchPin  = 13  #GPIO27    # ST_CP Pin of 74HC595(Pin12)
clockPin = 15   #GPIO22    # CH_CP Pin of 74HC595(Pin11)
# SevenSegmentDisplay display the character "0"- "F" successively
num = [0xc0,0xf9,0xa4,0xb0,0x99,0x92,0x82,0xf8,0x80,0x90,0x88,0x83,0xc6,0xa1,0x86,0x8e]
#0,1,2,3,4,5,6,7,8,9

{0: 0xc0,
1: 0xf9,
2: 0xa4,
3: 0xb0,
4: 0x99,
5: 0x92,
6: 0x82,
7: 0xf8,
8: 0x80,
9: 0x90}

def setup():
    GPIO.setmode(GPIO.BOARD)   # use PHYSICAL GPIO Numbering
    GPIO.setup(dataPin, GPIO.OUT)
    GPIO.setup(latchPin, GPIO.OUT)
    GPIO.setup(clockPin, GPIO.OUT)

def shiftOut(dPin,cPin,order,val):
    for i in range(0,8):
        GPIO.output(cPin,GPIO.LOW);
        if(order == LSBFIRST):
            GPIO.output(dPin,(0x01&(val>>i)==0x01) and GPIO.HIGH or GPIO.LOW)
        elif(order == MSBFIRST):
            GPIO.output(dPin,(0x80&(val<<i)==0x80) and GPIO.HIGH or GPIO.LOW)
            print(f"{i}: {num[i]}")
            print(0x80&(val<<i)==0x80)
            print((0x80&(val<<i)==0x80) and GPIO.HIGH or GPIO.LOW)
        GPIO.output(cPin,GPIO.HIGH);

def loop():
    while True:
        for i in range(0,len(num)):
            GPIO.output(latchPin,GPIO.LOW)
            shiftOut(dataPin,clockPin,MSBFIRST,num[i])  # Send serial data to 74HC595
            GPIO.output(latchPin,GPIO.HIGH)
            time.sleep(2)
        # for i in range(0,len(num)):
        #     GPIO.output(latchPin,GPIO.LOW)
        #     shiftOut(dataPin,clockPin,MSBFIRST,num[i]&0x7f) # Use "&0x7f" to display the decimal point.
        #     GPIO.output(latchPin,GPIO.HIGH)
        #     time.sleep(0.5)

def destroy():
    GPIO.cleanup()

if __name__ == '__main__': # Program entrance
    print ('Program is starting...' )
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        destroy()
