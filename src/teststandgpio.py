#!/usr/bin/python3
import settings
from time import sleep
import Adafruit_BBIO.GPIO as GPIO
from sys import stderr


def setGPIOpin(pin, state):
    spin = str(pin)
    sstate = str(state)
    if state == "HIGH":
        settings.msgType = "status"
        settings.commandList = "GPIO Pin "+spin+" set HIGH"
    else:
        settings.msgType = "status"
        settings.commandList = "GPIO Pin "+spin+" set LOW"
    GPIO.setup(spin, GPIO.OUT)    # eg. GPIO.setup("P8_10",GPIO.OUT)
    settings.msgType = "status"
    settings.commandList = "GPIO Pin "+spin+" is HIGH"
    GPIO.setup(spin, sstate)
    GPIO.cleanup()


def readGPIOpin(pin):  # pin format = P8_XX
    spin = str(pin)
    GPIO.setup(spin, GPIO.IN)
    if GPIO.input(spin):
        settings.msgType = "status"
        settings.commandList = "GPIO Pin "+spin+" is HIGH"
    else:
        settings.msgType = "status"
        settings.commandList = "GPIO Pin "+spin+" is LOW"


while settings.invokeJsonParser == True:
    if settings.msgType == "command":
        if settings.commandList == "readGPIO30":
            readGPIOpin("P8_30")
        if settings.commandList == "setGPIO30H":
            setGPIOpin("P8_30", "HIGH")
        if settings.commandList == "setGPIO30L":
            setGPIOpin("P8_30", "LOW")
            print("")
    if settings.msgType == "shutdown":
        print(stderr, 'Shutting teststandgpio down')
        break
    sleep(1)