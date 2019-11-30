#!/usr/bin/python3
import os
import json
import jsonschema
import settings


class JsonControl():
    """JsonControl Can:
    * Import a known (controlled) schema "template"
    * Validate a JSON Schema with reference to the known schema.
    * Serialize json dict obj to json str
    * De-serialize json str to json dict obj 

    :return: JSON Schema
    :rtype: dict object
    """

    def __init__(self):
        """__init__ Known JSON templates/schemas 
        is stored in self.templatesdir, 
        and known templates will append to self.templates
        """
        self.templatesdir = settings.jsonTemplatesDir
        self.templates = []
        self.msgTemplateNotFound = \
            "Unknown file! Only known Templates placed in " + \
            str(self.templatesdir) + " is accepted!"
        for root, dirs, files in os.walk(self.templatesdir):
            root = root
            dirs = dirs
            for file in files:
                if file.endswith('.json'):
                    self.templates.append(file)

    def getTemplate(self, filename):
        """getTemplate loads the JSON Schema that matches the passed
        filename if it exists in the folder with known templates

        :return: JSON Schema from template
        :rtype: dict obj
        """
        if filename == "default":
            settings.sel_defaultJsonTemplate = 1
            self.filename = settings.defaultJsonTemplate
        elif filename == settings.defaultJsonTemplate:
            settings.sel_defaultJsonTemplate = 1
            self.filename = settings.defaultJsonTemplate
        else:
            settings.sel_defaultJsonTemplate = 0
            self.filename = filename
        if any(self.filename in s for s in self.templates):
            self.filename = self.templatesdir+self.filename
        else:
            print(self.msgTemplateNotFound)
            print("Known Templates:")
            print(str(self.templates))
            return "failed"
        with open(self.filename, 'r') as f:
            self.jsonTemplateFromFile = json.load(f)
        return self.jsonTemplateFromFile

    def validateTemplate(self, schemaForValidation):
        """validateTemplate will validate the passed schema
        against the original schema and will report if schema is invalid JSON,
        or if typeErrors is found in the schema

        :param schemaForValidation: JSON schema
        :type schemaForValidation: dict object
        """
        jsonschema.validate(schemaForValidation, self.jsonTemplateFromFile)

    def setDefaultValues(self, schema):
        """setDefaultValues 
        Sets default values for respective keys in the json schema,
        set defualt values in settings.py. 
        """
        if settings.sel_defaultJsonTemplate == 1:
            schema["protocolVersion"] = settings.df_protocolVersion
            schema["sentBy"] = settings.df_sentBy
            schema["msgType"] = settings.df_msgType
            schema["commandList"] = settings.df_commandList
            schema["statusCode"] = settings.df_statusCode
            schema["embeddedFileFormat"] = settings.df_embeddedFileFormat
            schema["embeddedFile"] = settings.df_embeddedFile
            settings.protocolVersion = settings.df_protocolVersion
            settings.sentBy = settings.df_sentBy
            settings.msgType = settings.df_msgType
            settings.commandList = settings.df_commandList
            settings.statusCode = settings.df_statusCode
            settings.embeddedFileFormat = settings.df_embeddedFileFormat
            settings.embeddedFile = settings.df_embeddedFile
        else:
            print("No Default values to set")

    def setValues(self, schema):
        schema["protocolVersion"] = settings.protocolVersion
        schema["sentBy"] = settings.sentBy
        schema["msgType"] = settings.msgType
        schema["commandList"] = settings.commandList
        schema["statusCode"] = settings.statusCode
        schema["embeddedFileFormat"] = settings.embeddedFileFormat
        schema["embeddedFile"] = settings.embeddedFile

    def getValues(self, schema):
        settings.protocolVersion = schema["protocolVersion"]
        settings.sentBy = schema["sentBy"]
        settings.msgType = schema["msgType"]
        settings.commandList = schema["commandList"]
        settings.statusCode = schema["statusCode"]
        settings.embeddedFileFormat = schema["embeddedFileFormat"]
        settings.embeddedFile = schema["embeddedFile"]

    def serialize(self, schema):
        """serialize converts passed schema to json-string 

        :param schema: json obj to convert to string
        :type schema: dict
        :return: data as string
        :rtype: str
        """
        self.serializedData = json.dumps(schema, indent=4)
        return self.serializedData

    def deSerialize(self, jsonString):
        """deSerialize converts passed json string to a json dict

        :param jsonString: json string
        :type jsonString: str
        :return: data as json obj
        :rtype: dict
        """
        self.deSerializedData = json.loads(jsonString)
        return self.deSerializedData
