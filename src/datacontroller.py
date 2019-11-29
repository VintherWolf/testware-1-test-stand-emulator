#!/usr/bin/python3
import sys
from jsoncontroller import JsonControl
from netcomclient import sendNetData
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
            self.cjsonSchema.setDefaultValues(schema)
            settings.msgType = "command"
            settings.commandList = "starttest"
            self.cjsonSchema.setValues(schema)
            settings.volatileData = JsonControl.serialize(
                self, schema)
            sendNetData()
        else:
            print("Unkown Test Stand ID!")
            print("Provide TS1 for Test Stand 1, TS2, TS3 etc..")

    def bbbsetTemplate(self, schema):
        try:
            self.jsonSchema = self.cjsonSchema.getTemplate(
                schema)
        except:
            print("Failed loading JSON Schema!")
        self.cjsonSchema.validateTemplate(self.jsonSchema)
        return self.jsonSchema


if __name__ == '__main__':
    argv = sys.argv
    commands = ['-bbbtest']

    if len(argv) == 3:
        teststandID = argv[2]
        if commands[0] in argv:
            settings.sel_defaultJsonTemplate = 1
            bbbtest = DataControl()
            bbbtemplate = bbbtest.bbbsetTemplate(settings.defaultJsonTemplate)
            bbbtest.startTest(bbbtemplate, teststandID)
            print("Argv 2 = ", teststandID)
            print(bbbtemplate)
        else:
            print("Available Commands is:")
            for command in range(0, len(commands)):
                print(commands[command])
    else:
        print("Invalid input!")
        print("Usage is -command -teststandid")
        print("Where command can be:")
        print(' '.join(commands))
        print("and teststandid shall be TS1, TS2, TS3 etc.")
