#!/usr/bin/python3
from tkinter import Tk, Frame, Button, Label, Entry, E, W, N, S, END
from jsoncontroller import JsonControl
from datacontroller import DataControl
from netcomclient import sendNetData
from netcomserver import getNetData
import os
import settings

# Fonts
f_header1 = ("Arial", 10, "bold")
f_normal = ("Arial", 8)

# Texts
txt_programTitle = settings.programTitle


class Gui:
    # , padding=(3, 3, 12, 12)
    def __init__(self, master):
        self.cjsonSchema = JsonControl()
        self.datactrl = DataControl()
        content = Frame(root)
        content.grid()
        # Program "Main" Header
        self.lb_prgHeader = Label(
            content, text=txt_programTitle, font=f_header1, )
        self.lb_prgHeader.grid(row=0, column=0, columnspan=4, sticky=(N, E, W))

        # Button: Start Test
        self.bt_startTest = Button(
            content, text="Start Test", font=f_normal, command=self.startTest)
        self.bt_startTest.grid(row=5, column=0)

        # Button: Initialize Template
        self.bt_usetemplate = Button(
            content, text="Use Template", font=f_normal, command=self.setTemplate)
        self.bt_usetemplate.grid(row=1, column=0)

        # Entry: Template
        self.entry_template = Entry(
            content, width=16)
        self.entry_template.grid(row=1, column=1, columnspan=3)
        self.entry_template.insert(0, settings.defaultJsonTemplate)
        # Button: Quit Program
        self.bt_quitProgram = Button(
            content, text="Quit", font=f_normal, command=content.quit)
        self.bt_quitProgram.grid(row=6, column=3, sticky=(S, E))

        # Label: Receive Data
        self.lb_rxData = Label(content, text="Received Data", font=f_normal)
        self.lb_rxData.grid(row=4, column=1)

        # Entry: Receive Data
        self.entry_rxData = Entry(
            content, width=12)
        self.entry_rxData.grid(row=5, column=1)

    def setTemplate(self):
        actualTemplate = self.entry_template.get()
        self.entry_template.delete(0, END)
        try:
            jsonSchema = self.cjsonSchema.getTemplate(
                actualTemplate)
            self.jsonSchema = jsonSchema

            self.entry_template.insert(0, "JSON Schema OK")
        except:
            print(actualTemplate)
            self.entry_template.insert(0, "FAILED! Try again")
        self.entry_template.update()
        self.cjsonSchema.validateTemplate(jsonSchema)

    def startTest(self, testStandID="TS1"):
        self.entry_rxData.delete(first=0, last=END)
        if testStandID == "TS1":
            self.entry_rxData.delete(0, END)
            self.entry_rxData.update()
            print("Test Stand 1 Starts Testing!")
            settings.msgType = "command"
            settings.commandList = "starttest"
            JsonControl.setValues(self, self.jsonSchema)
            settings.txData = JsonControl.serialize(
                self, self.jsonSchema)
            sendNetData()
            self.entry_rxData.insert(0, settings.rxData_cl)

        else:
            print("Unkown Test Stand ID!")
            print("Provide TS1 for Test Stand 1, TS2, TS3 etc..")


root = Tk()
root.title(txt_programTitle)
gui = Gui(root)
root.mainloop()
