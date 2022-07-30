# -*- coding: utf-8 -*-
"""
@author: roberto.sopranzetti@studio.unibo.it
matricola: 0000993972
"""

from email import message
import socket as sk
import os
import sys
import time


SERVER_PATH = os.getcwd()+"/server/files/"
encoded = 'utf8'
buffer = 4096

    
   
def ServerList():
    list = os.listdir(SERVER_PATH)
    listC = str(list).encode()
    send = sock.sendto(listC,address)
    print("Error message sent to %s with %s bytes" % (address,send))
    

def serverExit():
    print("Server EXIT, will close the socket")
    sock.close()
    sys.exit()
    
    
def serverGet():
    args = text.split(' ')
    d = 1
    if len(args)==1:
        msg = "ERROR you have to put a file name as an argument"
        send = sock.sendto(msg.encode(),address)
        print("Error message sent to %s with %s bytes" % (address,send))

    elif not os.listdir(SERVER_PATH).__contains__(args[1]):
        msg = "ERROR file not existing!"
        send = sock.sendto(msg.encode(),address)
        print("Error message sent to %s with %s bytes" % (address,send))

    else:
        try:
            with open(SERVER_PATH+args[1], 'rb') as file:
                while True:
                    data = file.read(buffer)
                    if not data:
                        send = sock.sendto('END'.encode(),address)
                        print("Done")
                        file.close()
                        break
                    else:
                        print("Sending packet number ", d)
                        send = sock.sendto(data, address)
                        d += 1
        except IOError as info:
            print(info)
            msg = "Error during download"
            send = sock.sendto(msg.encode(),address)
            print("Error message sent to %s with %s bytes" % (address,send))

        
def serverPut():
    args = text.split(' ')
    d = 1
    print("Function Put in use...")
    if len(args)==1:
        msg = "ERROR you have to put a file name as an argument"
        send = sock.sendto(msg.encode(),address)
        print("Error message sent to %s with %s bytes" % (address,send))

    elif os.listdir(SERVER_PATH).__contains__(args[1]):
        msg = "ERROR file already exists"
        send = sock.sendto(msg.encode(),address)
        print("Error message sent to %s with %s bytes" % (address,send))

    else:
        try:
            status = "READY"
            receive = sock.sendto(status.encode(), address) 
            with open(SERVER_PATH+args[1], 'wb') as file:
                while True:
                    data, server_addr = sock.recvfrom(buffer)
                    print("Received packet number ",d)
                    if data == "END".encode():
                        print("Done")
                        file.close()
                        break
                    else:
                        file.write(data)
                        d += 1
        except IOError as info:
            print(info)
            msg = "Error during upload"
            send = sock.sendto(msg.encode(),address)
            print("Error message sent to %s with %s bytes" % (address,send))
            


def serverElse():
    msg = "ERROR " + text + " is not recognized by server"
    msgEn = msg.encode(encoded)
    sock.sendto(msgEn, address)
    print("message sent")


try:
    sock = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
    server_address = ('localhost', 10000)
    print('\n\r starting up on %s port %s' % server_address)
    sock.bind(server_address)
    print("binding was a success")
except sk.error:
    print("failed to create socket")
    sys.exit()

while True:
    print('\n\r Waiting for a response...')  
    data, address = sock.recvfrom(buffer)            
    print('recieved %s bytes from %s' % (len(data), address))

    text = data.decode(encoded)
    print("text")       
    if text.startswith('get'):
        print("Reading request recieved from: ", address)
        serverGet()
    elif text.startswith('put'):
        print("Writing request received from: ", address)
        serverPut()
    elif text.startswith('list'):
        print("List request received from: ", address)
        ServerList()
    elif text.startswith('exit'):
        print("Server exiting...")
        serverExit()
    else:
        serverElse() 