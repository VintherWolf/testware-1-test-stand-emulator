#!/usr/bin/python3
import sys
from jsoncontroller import JsonControl
from netcomclient import sendNetData


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
            self.jsonSchema = self.cjsonSchema.getTemplate(
                schema)
        except:
            print(schema)
        self.cjsonSchema.validateTemplate(self.jsonSchema)

    def bbbstartTest(self, testStandID):
        if testStandID == "TS1":
            print("Test Stand 1 Starts Testing!")
            bbbsettings.msgType = "command"
            bbbsettings.commandList = "starttest"
            JsonControl.setValues(self, self.jsonSchema)
            bbbsettings.volatileData = JsonControl.serialize(
                self, self.jsonSchema)
            sendNetData()
            print("Received = %s" % bbbsettings.rxData)

        else:
            print("Unkown Test Stand ID!")
            print("Provide TS1 for Test Stand 1, TS2, TS3 etc..")


if __name__ == '__main__':
    argv = sys.argv

    commands = ['-bbbtest']
    platform = sys.platform

    if platform == "linux2":
        import bbbsettings
        print("Running on BeagleBone Black")
    else:
        print("Running on Host PC or an unknown system")
        import settings

    if len(argv) == 3:
        if commands[0] in argv:
            bbbtest = DataControl()
            bbbtest.bbbsetTemplate(bbbsettings.defaultJsonTemplate)
            bbbtest.bbbstartTest(argv[2])
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
