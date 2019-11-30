#!/usr/bin/env bash
echo "Starts Test Run"


(/usr/bin/env python ./src/datacontroller.py -bbbtest TS1 command readGPIO30 test)

