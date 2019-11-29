#!/usr/bin/python3
""" Contains all shared variables
"""
import os
import sys
jsonTemplatesDir = ""

# Set to True for testing only
serverloopback = False

# Host Specifics
if sys.platform == "linux2":
    try:
        host = os.uname()
        if host[1] == "beaglebone":
            Hostname = "TestStand"
            print("Running on BeagleBone Black")
    except:
        Hostname = "WebServer"
        pass
else:
    Hostname = "WebServer"


try:
    os.listdir("src")
    jsonTemplatesDir = "./src/json-templates/"
except:
    jsonTemplatesDir = "./json-templates/"


global netcomserverStatus


# JSON Controller and Test

defaultJsonTemplate = "WebinterfaceTeststandPayload_v1.json"
refJsonTemplate = "goldentemplate.json"
actualTemplate = ""
sel_defaultJsonTemplate = ""

# Default values for defualt template
df_protocolVersion = 1.0
df_sentBy = Hostname
df_msgType = None
df_commandList = None
df_statusCode = None
df_embeddedFileFormat = None
df_embeddedFile = None

# Keys for default template
protocolVersion = ""
sentBy = ""
msgType = ""
commandList = ""
statusCode = ""
embeddedFileFormat = ""
embeddedFile = ""

# JSON String to be send
global volatileData
volatileData = ""
global rxData
rxData = ""
global txData
txData = ""
global teststandstatus
teststandstatus = ""

global rxData_ser
rxData_ser = ""
global testRun
testRun = ""

# Inet Settings
if serverloopback == False:
    serverIP = '192.168.7.2'
    serverPort = 10000
else:
    serverIP = 'localhost'
    serverPort = 10000

ENCODING = 'utf-8'

netcomserverStatus = ''

# GUI
programTitle = " Test Stand Emulator Control "
