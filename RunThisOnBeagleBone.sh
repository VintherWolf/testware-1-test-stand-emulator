#!/usr/bin/env bash
# This is the prgram that shall be run on the BeagleBone 
# Start HostPC_CLI on the host, which is the main program for the client.

# Websockets = Server side 
echo "Starts Server"
(/usr/bin/env python ./src/netcomserver.py)

