#!/usr/bin/python3
import socket
import sys
import settings
from time import sleep
from teststandgpio import getTestResult
print("Running on host %s " % settings.Hostname)  # Remove after debug


def getNetData():
    """getNetData Starts webserver (TCP IP Socket), and listens for host
    retrieves data from host, and saves it in settings.rxData_ser
    Sends response from settings.txData_ser

    :return: settings.rxData_ser
    :rtype: JSON Dict
    """
    str_rxData_ser = []
    settings.sel_defaultJsonTemplate = 1
    # tempData = ""
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

            # Receive the data in small
            while True:
                rxData_temp = connection.recv(settings.NETBUFSIZE)
                if rxData_temp == b'KillServer':
                    return "Server killed"
                if rxData_temp == b'NoMorePackages':
                    break
                if not rxData_temp:
                    break
                str_rxData_ser.append(rxData_temp)
            settings.str_rxData_ser = b''.join(str_rxData_ser)
            settings.str_rxData_ser = settings.str_rxData_ser.decode(
                settings.ENCODING)
            settings.rxData_ser = settings.rxData_ser.replace(
                "\n", "")  # Remove newlines
            settings.statusCode = "Busy"
            # print(sys.stderr, 'Received "%s"' % settings.str_rxData_ser)
            if settings.statusCode == "Busy":

                try:
                    getTestResult()
                except:
                    print("Failed handling JSON schema")
                    pass
                settings.txData_ser = settings.txData_ser
                settings.txData_ser = settings.txData_ser.encode(
                    settings.ENCODING)
                print(sys.stderr, 'sending "%s"' % settings.txData_ser)
                if settings.statusCode == "Ready":
                    connection.sendall(settings.txData_ser)
                str_rxData_ser = []

        finally:
            # Clean up the connection
            connection.close()


if __name__ == '__main__':
    getNetData()
