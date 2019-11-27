#!/usr/bin/python3
import settings
from jsoncontroller import JsonControl
from netcomclient import sendNetData


class DataControl():
    def __init__(self):
        return

    def getKeys(self, schema):
        return schema.keys()

    def getValues(self, schema):
        return schema.values()

    def startTest(self, schema, testStandID):
        if testStandID == "TS1":
            print("Test Stand 1 Starts Testing!")
            JsonControl.setDefaultValues(self, schema)
            settings.msgType = "command"
            settings.commandList = "starttest"
            JsonControl.setValues(self, schema)
            settings.volatileData = JsonControl.serialize(
                self, schema)
            sendNetData()
        else:
            print("Unkown Test Stand ID!")
            print("Provide TS1 for Test Stand 1, TS2, TS3 etc..")
