#!/usr/bin/python3
import unittest
import settings
from jsoncontroller import JsonControl


refSchema = settings.refJsonTemplate
webSchema = settings.defaultJsonTemplate
testSchema = \
    {"id": 1,
     "name": "A green door",
             "price": 12.5,
             "tags": [
                 "home",
                 "green"
             ]
     }


class Test_Import_Template(unittest.TestCase):

    def test_Can_Import_Known_Template(self):
        """test_Can_Import_Known_Template 
        TC1-A Kan importere template
        """
        knownTemplate = settings.defaultJsonTemplate
        self.known_Template = JsonControl()
        self.known_Template.getTemplate(knownTemplate)
        self.assertTrue(self.known_Template, True)

    def test_Will_Fail_unKnown_Template(self):
        """test_Will_Fail_unKnown_Template 
        TC2-A Accepterer kun kendte templates
        """
        unknownTemplate = "unknown.json"
        self.unknown_Template = JsonControl()
        Template = self.unknown_Template.getTemplate(unknownTemplate)
        self.assertIs(Template, "failed")


class Test_Can_Validate_Ref_Template(unittest.TestCase):
    def setUp(self):
        self.refschema = JsonControl()
        self.refschema.getTemplate(refSchema)

    def test_Reference_template_with_valid_input(self):
        """test_Reference_template_with_valid_input 
        TC3-A Den Importerede template valideres 
        mod indholdet i den lagrede
        """
        TestJsonString = {"name": "eggs", "price": 21.47, "sku": 7}
        self.refschema.validateTemplate(TestJsonString)

    def test_Reference_template_with_invalid_input(self):
        """test_Reference_template_with_valid_input 
        TC4-A Hvis en type int sættes til type string fejler validering
        """
        TestJsonString = {"name": "eggs", "price": 21.47, "sku": "o"}
        with self.assertRaises(Exception):
            self.refschema.validateTemplate(TestJsonString)


class Test_Can_Validate_Webinterface_template(unittest.TestCase):
    def setUp(self):
        self.webschema = JsonControl()
        self.webschema.getTemplate(webSchema)

    def test_Webinterface_template_with_valid_input(self):
        """test_Webinterface_template_with_valid_input 
        TC5-A Kan validere WebinterfaceTeststandPayload_v1.json
        """
        jsonSchema = dict(statuscode="2", testcode="Write")
        self.webschema.validateTemplate(jsonSchema)

    def test_Webinterface_template_with_default(self):
        """test_Webinterface_template_with_default 
        TC6-A Kan importere default template med argument "default"
        """
        self.webschema2 = JsonControl()
        jsonSchema = self.webschema2.getTemplate("default")
        self.webschema2.validateTemplate(jsonSchema)


class Test_Serialize_deSerialize(unittest.TestCase):
    def setUp(self):
        self.webschema = JsonControl()
        self.webschema.getTemplate(webSchema)

    def test_serialize_dict_to_string(self):
        """test_serialize_dict_to_string 
        TC7-A Kan serialize dict til string
        """
        jsonString = self.webschema.serialize(testSchema)
        self.assertTrue(isinstance(jsonString, str))

    def test_deSerializes_string_to_dict(self):
        """test_deSerializes_string_to_dict 
        TC8-A Kan De-serialize en string til dict
        """
        jsonString = self.webschema.serialize(testSchema)
        data = self.webschema.deSerialize(jsonString)
        self.assertTrue(isinstance(data, dict))


class Test_Setvalues(unittest.TestCase):
    def setUp(self):
        self.webschema = JsonControl()
        self.jsonSchema = self.webschema.getTemplate("default")

    def test_Can_SetValues_to_Default(self):
        """test_SetValues_to_default 
        TC9-A Kan sætte værdierne i et JSON schema til default værdier
        """
        self.assertEqual(self.jsonSchema["sentBy"], "<machineProcessId>")
        self.webschema.setDefaultValues(self.jsonSchema)
        self.assertEqual(self.jsonSchema["sentBy"], settings.df_sentBy)
        self.assertEqual(self.jsonSchema["statusCode"], None)

    def test_Can_SetValues_to_RealValues(self):
        """test_SetValues_to_RealValues 
        TC10-A Kan sætte værdierne i et JSON schema til "rigtige" værdier
        """
        settings.protocolVersion = 0.3
        settings.sentBy = "tester"
        settings.msgType = "command"
        settings.commandList = "starttest"
        settings.statusCode = "busy"
        settings.embeddedFileFormat = "tbd"
        settings.embeddedFile = "small"
        self.webschema.setValues(self.jsonSchema)
        self.assertEqual(self.jsonSchema["protocolVersion"], 0.3)
        self.assertEqual(self.jsonSchema["sentBy"], "tester")
        self.assertEqual(self.jsonSchema["msgType"], "command")
        self.assertEqual(self.jsonSchema["commandList"], "starttest")
        self.assertEqual(self.jsonSchema["statusCode"], "busy")
        self.assertEqual(self.jsonSchema["embeddedFileFormat"], "tbd")
        self.assertEqual(self.jsonSchema["embeddedFile"], "small")


if __name__ == '__main__':
    unittest.main()
