#!/usr/bin/python3
""" Contains all shared variables
"""
import os
import sys

# Set serverloopback = True for testing only
serverloopback = False
invokeJsonParser = False
# Host Specifics
if sys.platform == "linux2":
    try:
        host = os.uname()
        if host[1] == "beaglebone":
            Hostname = "TestStand"
            print("Running on BeagleBone Black")
            invokeJsonParser = True
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

# JSON Controller and Test

defaultJsonTemplate = "WebinterfaceTeststandPayload_v1.json"
refJsonTemplate = "goldentemplate.json"
actualTemplate = ""
sel_defaultJsonTemplate = ""

# Default values for default template
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

# Data Transactions
# Client side

rxData_cl = ""
str_rxData_cl = ""
txData_cl = ""

# Server Side
rxData_ser = ""
str_rxData_ser = ""
txData_ser = "TEST"

# Inet Settings
if serverloopback == False:
    serverIP = '192.168.7.2'
    serverPort = 10000
else:
    serverIP = 'localhost'
    serverPort = 10000
NETBUFSIZE = 1024
ENCODING = 'utf-8'

# GUI Settings
programTitle = " Test Stand Emulator Control "
