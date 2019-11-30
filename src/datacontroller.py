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
        """startTest Initiates a testrun by setting up the values in
        the JSON schema and pushing them to the teststand via netsockets
        (sendNetData)

        :param schema: Json schema
        :type schema: dict
        :param testStandID: "TS1" "TS2" etc.
        :type testStandID: str
        """
        if testStandID == "TS1":
            print("Test Stand 1 Starts Testing!")
            self.cjsonSchema.setValues(schema)
            settings.txData_cl = JsonControl.serialize(
                self, schema)
            sendNetData()
        else:
            print("Unkown Test Stand ID!")
            print("Provide TS1 for Test Stand 1, TS2, TS3 etc..")

    def trySetTemplate(self, schema):
        """trySetTemplate Will attempt to create a default template,
        that the teststand ID and commands can be stored in, 
        before initiating a test.

        :param schema: json schema
        :type schema: dict
        :return: schema
        :rtype: dict
        """
        try:
            self.jsonSchema = self.cjsonSchema.getTemplate(
                schema)
            self.cjsonSchema.setDefaultValues(self.jsonSchema)
        except:
            print("Failed loading JSON Schema!")
        self.cjsonSchema.validateTemplate(self.jsonSchema)
        return self.jsonSchema


if __name__ == '__main__':
    argv = sys.argv
    JsonWorkerClass = DataControl()
    jsonWorkerSchema = JsonWorkerClass.trySetTemplate(
        settings.defaultJsonTemplate)
    settings.msgType = "command"
    settings.statusCode = "Ready"
    if len(argv) == 4:
        teststandID = argv[1]
        settings.msgType = argv[2]
        settings.commandList = argv[3]
    elif len(argv) > 1 and len(argv) < 4:
        print("Invalid input!")
    # Start Main Sequence, takes user input to set GPIO pin high or low:
    while True:
        choice = input("Set GPIO P8_11 HIGH (h) or LOW (l), Q for Quit\n")
        if choice == 'HIGH' or choice == 'h':
            settings.commandList = "setGPIO_P8_11H"
        elif choice == 'Q' or choice == 'q':
            print("Farewell")
            break
        else:
            settings.commandList = "setGPIO_P8_11L"
        JsonWorkerClass.startTest(jsonWorkerSchema, "TS1")
