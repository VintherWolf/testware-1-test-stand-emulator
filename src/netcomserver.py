#!/usr/bin/python3
import settings
import socket
import sys
from time import sleep

global netcomserverStatus
netcomserverStatus = "down"
global rxData, txData, count
rxData = ""
txData = ""

packages = 0


def getNetData():
    global netcomserverStatus, rxData, txData
    netcomserverStatus = "up"
    print("netcomserverStatus = %s" % netcomserverStatus)
    datapackages = []
    #tempData = ""
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    server_address = (settings.serverIP, settings.serverPort)
    print(sys.stderr, 'starting up on %s port %s' % server_address)
    sock.bind(server_address)

    # Listen for incoming connections
    sock.listen(1)
    while True:
        # Wait for a connection
        print(sys.stderr, 'waiting for a connection')
        connection, client_address = sock.accept()
        # sock.settimeout(3)
        try:
            print(sys.stderr, 'connection from', client_address)

            # Receive the data in small packages
            while True:
                package = connection.recv(4048)
                # print(datapackages)
                if package == b'KillServer':
                    return "Server killed"
                if package == b'NoMorePackages':
                    break
                if not package:
                    break
                datapackages.append(package)
            settings.rxData_ser = b''.join(datapackages)
            settings.testRun = "Running"
            print(sys.stderr, 'Received "%s"' % settings.rxData_ser.decode())
            if settings.testRun == "Running":
                sleep(2)
                print("TEST RUNNING")
                message = "GPIO"
                message = message.encode(settings.ENCODING)
                print(sys.stderr, 'sending "%s"' % message)
                connection.sendall(message)
                settings.testRun = "Ready"
                datapackages = []

        finally:
            # Clean up the connection
            netcomserverStatus = "down"
            connection.close()


if __name__ == '__main__':
    getNetData()
