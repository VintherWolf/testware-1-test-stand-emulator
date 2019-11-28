#!/usr/bin/python3
import sys
from jsoncontroller import JsonControl
from netcomclient import sendNetData

platform = sys.platform
if platform == "linux":
    import bbbsettings
    print("Running on BeagleBone Black")
else:
    import settings


class DataControl():
    def __init__(self):
        self.cjsonSchema = JsonControl()
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

    def bbbsetTemplate(self, schema):
        try:
            jsonSchema = self.cjsonSchema.getTemplate(
                schema)
            self.jsonSchema = jsonSchema
        except:
            print(schema)
        self.cjsonSchema.validateTemplate(jsonSchema)

    def bbbstartTest(self, testStandID):
        if testStandID == "TS1":
            print("Test Stand 1 Starts Testing!")
            settings.msgType = "command"
            settings.commandList = "starttest"
            JsonControl.setValues(self, self.jsonSchema)
            settings.volatileData = JsonControl.serialize(
                self, self.jsonSchema)
            sendNetData()
            print("Received = %s" % bbbsettings.rxData)

        else:
            print("Unkown Test Stand ID!")
            print("Provide TS1 for Test Stand 1, TS2, TS3 etc..")
