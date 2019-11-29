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
        txData_cl = settings.txData_cl
        # txData_cl = 'test txData_cl'
        print(sys.stderr, 'sending "%s"' % txData_cl)
        txData_cl = txData_cl.encode(settings.ENCODING)
        sock.sendall(txData_cl)
        txData_cl = None
        sleep(1)
        if txData_cl == None:
            txData_cl = 'NoMorePackages'
        #    print(sys.stderr, 'sending "%s"' % txData_cl)
            txData_cl = txData_cl.encode(settings.ENCODING)
            sock.sendall(txData_cl)
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
            settings.rxData_cl = b''.join(datapackages)
            settings.rxData_cl = settings.rxData_cl.decode()
            print("Received = ", settings.rxData_cl)
            datapackages = []
    finally:
        print(sys.stderr, 'clent closing socket')
       # print("Test Result %s" % testResult)
        sock.close()


# if __name__ == '__main__':
    # sendNetData()
