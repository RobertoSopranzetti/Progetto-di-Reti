# -*- coding: utf-8 -*-
"""
@author: roberto.sopranzetti@studio.unibo.it
matricola: 0000993972
"""

import socket as sk
import os
import sys


buffer = 4096
encoded = 'utf-8'

UPLOAD_PATH = os.getcwd()+"/client/upload/"
DOWNLOAD_PATH = os.getcwd()+"/client/download/"


try:
    sock = sk.socket(sk.AF_INET,sk.SOCK_DGRAM)
    print("Socket initialized")
    sock.setblocking(0)
    sock.settimeout(15)
except sk.error:
    print("Failed to create Socket")
    sys.exit()

server_address=('localhost', 10000)
print('\n\r starting up on %s port %s' % server_address)

while True:
    command = input(
        "Choose one of the options \n1. get <file>\n2. put <file>\n3. list\n4. exit\n")
    CommandClient=command.encode(encoded)

    CL = command.split(' ')
    print("Processing... check server for messages")
    
    if command.startswith('get'):
        
        print("Checking for acknowledgement")
        sock.sendto(CommandClient, server_address)
        try:
            ClientData, client_address = sock.recvfrom(buffer)
        except:
            print("Timeout or some unknown error")
            sys.exit()
        args = CL[1]
        if ClientData.startswith('ERROR'.encode()):
            print(ClientData.decode(encoded))
        else:
            with open(DOWNLOAD_PATH+args, 'wb') as file:
                file.write(ClientData)
                while True:
                    data, server_addr = sock.recvfrom(buffer)
                    if data == 'END'.encode():
                        break
                    file.write(data)
            file.close()
            print("File ", args, " downloaded successfully")       
                
    elif command.startswith('put'):
        args = CL[1]
        print("Checking for acknowledgement") 

        if not os.listdir(UPLOAD_PATH).__contains__(args):
            print("ERROR File not found !!!")
        else:
            sock.sendto(CommandClient, server_address)
            try:
                ClientData, client_address = sock.recvfrom(buffer)
            except:
                print("Timeout or some unknown error")
                sys.exit()
            text = ClientData.decode(encoded)
            if ClientData.startswith('ERROR'.encode()):
                print(text)
            else:
                with open(UPLOAD_PATH+args, 'rb') as file:
                    while True:
                        data = file.read(buffer)
                        if not data:
                            send = sock.sendto('END'.encode(), server_address)
                            file.close()
                            break
                        else:
                            send = sock.sendto(data,server_address)
                print("File ", args, " uploaded successfully")  


        
                
    elif command.startswith('list'):
        print("Checking for acknowledgement")
        sock.sendto(CommandClient, server_address)

        try:
            ClientData, client_address = sock.recvfrom(buffer)
        except:
            print("Timeout or some unknown error")
            sys.exit()
        text = ClientData.decode(encoded)
        print(text)
        
            
    elif command.startswith('exit'):
        print("Server will exit")
        sock.sendto(CommandClient, server_address)

        sock.close()
        sys.exit()
                 
    else:
        sock.sendto(CommandClient, server_address)

        try:
            ClientData, client_address = sock.recvfrom(buffer)
        except:
            print("Timeout or some unknown error")
            sys.exit()
        text = ClientData.decode(encoded)
        print(text)