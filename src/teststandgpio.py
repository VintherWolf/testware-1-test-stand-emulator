#!/usr/bin/python3
import settings
from time import sleep
from sys import stderr
from jsoncontroller import JsonControl


if settings.Hostname == "TestStand":
    try:
        import Adafruit_BBIO.GPIO as GPIO
    except:
        # May not work on windows without tweaking visual studio
        Warning("Failed importing Adafruit BBIO for GPIO")


def setGPIOpin(pin, state):
    """setGPIOpin Set a GPIO pin HIGH or LOW

    :param pin: header#_pinnumber eg. P8_11
    :type pin: str
    :param state: HIGH / LOW
    :type state: str
    """
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
    GPIO.setup(spin, GPIO.OUT)    # eg. GPIO.setup("P8_11",GPIO.OUT)
    settings.msgType = "status"
    GPIO.output(spin, output)
    GPIO.cleanup()


def readGPIOpin(pin):  # pin format = P8_XX
    """readGPIOpin retrieves current state of a GPIO pin per request
    """
    spin = str(pin)
    GPIO.setup(spin, GPIO.IN)
    if GPIO.input(spin):
        settings.msgType = "status"
        settings.commandList = "GPIO Pin "+spin+" is HIGH"
    else:
        settings.msgType = "status"
        settings.commandList = "GPIO Pin "+spin+" is LOW"


# We must instantiate a JSON template object to be able to start test etc.
JsonWorker = JsonControl()
JsonWorker.getTemplate("default")


def getTestResult():
    """getTestResult will handle request for test actions. 
    Meaning it will initiate a given test action eg. setGPIOpin "P8_11" "HIGH"
    """
    if settings.statusCode == "Busy":
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
        settings.statusCode = "Ready"
    else:
        print("Failed! Test is Not Running!")
