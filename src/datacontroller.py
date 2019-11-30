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
            self.cjsonSchema.setValues(schema)
            settings.txData_cl = JsonControl.serialize(
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
    argvcommands = ['-bbbtest']
    argvcommandlist = ' '.join(argvcommands)
    if len(argv) > 2:
        teststandID = argv[2]
        if argvcommands[0] in argv:
            settings.msgType = argv[3]
            settings.commandList = argv[4]
            settings.statusCode = argv[5]
            bbbtest = DataControl()
            bbbtemplate = bbbtest.bbbsetTemplate(settings.defaultJsonTemplate)
            bbbtest.startTest(bbbtemplate, teststandID)
        else:
            print("Available Commands is:")
            for command in range(0, len(argvcommands)):
                print(argvcommands[command])
    else:
        print(("Invalid input!"
               "If default template is choosen:"
               "Usage: -command -teststandid -msgtype -commandlist -statuscode"
               "Where command can be: %s" % argvcommandlist))
        print(("teststandid shall be TS1, TS2, TS3 etc."
               "msgtype: <command|status|data>"
               "commandlist: <comma separated list of commands>"
               "statuscode: statusCodeIdForTeststand"))
