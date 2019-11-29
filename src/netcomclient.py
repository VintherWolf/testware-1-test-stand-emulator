#!/usr/bin/python3
import settings
import socket
import sys
from time import sleep


def sendNetData():
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    datapackages = []
    # tempData = ""
    # Connect the socket to the port where the server is listening
    server_address = (settings.serverIP, settings.serverPort)
    print(sys.stderr, 'connecting to %s port %s' % server_address)
    sock.connect(server_address)
    sock.settimeout(10)
    try:
        # Send data
        txData = settings.txData
        # txData = 'test txData'
        print(sys.stderr, 'sending "%s"' % txData)
        txData = txData.encode(settings.ENCODING)
        sock.sendall(txData)
        txData = None
        sleep(1)
        if txData == None:
            txData = 'NoMorePackages'
        #    print(sys.stderr, 'sending "%s"' % txData)
            txData = txData.encode(settings.ENCODING)
            sock.sendall(txData)
        # print("Test Result %s" % testResult)
        # Receive the data in small packages
        while True:
            package = sock.recv(settings.NETBUFSIZE)
            # print(datapackages)
            if package == b'NoMorePackages':
                break
            if not package:
                break
            datapackages.append(package)
            settings.rxData = b''.join(datapackages)
            settings.rxData = settings.rxData.decode()
            print("Received = ", settings.rxData)
            datapackages = []
    finally:
        print(sys.stderr, 'Client closing socket')
       # print("Test Result %s" % testResult)
        sock.close()


# if __name__ == '__main__':
    # sendNetData()
