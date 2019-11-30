#!/usr/bin/python3
import settings
from time import sleep
import Adafruit_BBIO.GPIO as GPIO
from sys import stderr
from jsoncontroller import JsonControl


def setGPIOpin(pin, state):
    spin = str(pin)
    output = None
    if state == "HIGH":
        settings.msgType = "status"
        settings.commandList = "GPIO Pin "+spin+" set HIGH"
        output = GPIO.HIGH

    else:
        settings.msgType = "status"
        settings.commandList = "GPIO Pin "+spin+" set LOW"
        output = GPIO.LOW
    GPIO.setup(spin, GPIO.OUT)    # eg. GPIO.setup("P8_10",GPIO.OUT)
    settings.msgType = "status"
    settings.commandList = "GPIO Pin "+spin+" is HIGH"
    GPIO.setup(spin, output)
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


JsonWorker = JsonControl()
JsonWorker.getTemplate("default")


def getTestResult():
    if settings.testRun == "Running":
        print("Schema for deserialize = %s" % settings.str_rxData_ser)
        JsonSchema = JsonWorker.deSerialize(settings.str_rxData_ser)
        JsonWorker.getValues(JsonSchema)
        if settings.msgType == "command":
            if settings.commandList == "readGPIO_P8_11":
                readGPIOpin("P8_11")
            if settings.commandList == "setGPIO_P8_11H":
                setGPIOpin("P8_11", "HIGH")
            if settings.commandList == "setGPIO_P8_11L":
                setGPIOpin("P8_11", "LOW")
        if settings.msgType == "shutdown":
            print(stderr, 'Shutting teststandgpio down')
        JsonWorker.setValues(JsonSchema)
        settings.txData_ser = JsonWorker.serialize(JsonSchema)
        settings.testRun = "Ready"
    else:
        print("Failed! Test is Not Running!")
