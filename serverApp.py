# for local communication
import socket
from socket import error, setdefaulttimeout
import errno

# for threading chats
from threading import Thread

# for encryption
from cryptography.fernet import Fernet

# Global Data
from globalData import GlobalData


from contextlib import closing

# for data base
import eSqlite as ES

import csv

from datetime import datetime
import sys
# import user

class GlobalData_server:

    # setting up db module
    sObj = ES.SQLiteConnect()
    sObj.setDatabase("chatDatabase.db")

    result = sObj.setPassword(GlobalData.stringKey , pin = 123456)

    if(result == None):
        pass
    elif(result == False):              
        print("chat data base was created with diff key , delete previous chatDatabase.db to continue")
        sys.exit()

    sObj.setSecurityStatus(True)

    contentList = [["name" , "TEXT" , 1] , ["message" , "TEXT" , 1] , ["timeStamp" , "TEXT" , 1]]

    sObj.createTable("chatData" , contentList , raiseException = False)


    # setting up key verfication dictionary
    usersDict = {}

    with open('user.csv') as csvFile:
        csvReader = csv.reader(csvFile, delimiter=',')

        for row in csvReader:
            usersDict[str(row[0])] = str(row[1])









# class contain methods to handle encryption and decrption using AES module
class HandleEncryption:

    @classmethod
    def encryptor(self , string):
        stringToPass = bytes(string , "utf-8")
        encodedText = GlobalData.cipherSuite.encrypt(stringToPass)
        return encodedText.decode("utf-8")

        

    
    # function to decrypt the passed string
    @classmethod
    def decryptor(self , string):
        stringToPass = bytes(string , "utf-8")
        decodedText = GlobalData.cipherSuite.decrypt(stringToPass)
        return decodedText.decode("utf-8")



class HandleChat:


    # function to set up the new connection request and intialise the thread
    @classmethod
    def acceptIncomingConnection(cls):

        # virtually can handle unlimited connections
        while(True):

            client , clientAddress = GlobalData.serverObj.accept()

            # printing the connection details
            print("{} has connected".format(clientAddress))

            # send a welcome message and ask for name
            toSend = HandleEncryption.encryptor(GlobalData.welcomeMessage + " , Send you name please! ")
            client.send(bytes(toSend , "utf-8"))

            # storing the new connection details in dictionary
            GlobalData.addresses[client] = clientAddress

            # init thread
            Thread(target=cls.handleClient , args=(client , )).start()


    # function to handle the initiated client connection
    @classmethod
    def handleClient(cls , client):

        # first thing we receive is the clients name
        nameReceived = client.recv(GlobalData.bufferSize)

        nameReceived = str(nameReceived , "utf-8")

        name = HandleEncryption.decryptor(nameReceived)

        if(None == GlobalData_server.usersDict.get(name , None)):
            toSend = HandleEncryption.encryptor("You are not allowed to join , ending connection")
            client.send(bytes(toSend , "utf-8"))
            return


        toSend = HandleEncryption.encryptor("Please Send your Key")
        client.send(bytes(toSend , "utf-8"))

        keyReceived = client.recv(GlobalData.bufferSize)
        keyReceived = str(keyReceived , "utf-8")
        keyReceived = HandleEncryption.decryptor(keyReceived)

        if(keyReceived != GlobalData_server.usersDict.get(name , None)):
            toSend = HandleEncryption.encryptor("invalid key , ending connection")
            client.send(bytes(toSend , "utf-8"))
            return


        # sending greetings to user
        welcomeMessage = "Welcome {} , To quit chat type and send : {}".format(name , GlobalData.quitStatement)
        toSend = HandleEncryption.encryptor(welcomeMessage)
        client.send(bytes(toSend , "utf-8"))

        # broadcast message to all the connected user that name as connected
        toSend = "{} has joined the local-secure-chat".format(name)
        cls.broadcast(toSend)

        # adding client to storage
        GlobalData.clients[client] = name

        while(True):

            # decryting the message
            try:
                messageReceived = client.recv(GlobalData.bufferSize)
            
            # bad file descriptor
            except OSError:
                break

            # decrypting the message
            messageReceived = str(messageReceived , "utf-8")
            messageReceived = HandleEncryption.decryptor(messageReceived)

            # if user does not want to quit
            if(messageReceived != GlobalData.quitStatement):
                
                # broadcast the message to every one
                # here we don't need to worry about space as we are not working with string
                cls.broadcast(messageReceived , name)

            else:

                # init the closing sequence

                # send the client also to close the connection
                toSend = HandleEncryption.encryptor(GlobalData.quitStatement)
                client.send(bytes(toSend , "utf-8"))
                client.close()

                # delete the client data
                del GlobalData.clients[client]


                # broad cast to let others know that name as left the chat room
                toSend = HandleEncryption.encryptor("{} has left the chat room".format(name))
                cls.broadcast(toSend)

                break


    # function to broadcast a message to all the clients
    @classmethod
    def broadcast(cls , message , name = ""):

        # if the name contains space then it cannot be used with utf-8
        name = name + " : "

        toSend = HandleEncryption.encryptor(name + message)

        tempGlobalClients = GlobalData.clients.copy()

        # sending message to each client
        for sock in tempGlobalClients:
            try:
                GlobalData_server.sObj.insertIntoTable([name[:-2] , message , str(datetime.now())] , keyPass = None , tableName = None , forPass = False , commit = True)
                print(name + message)
                sock.send(bytes(toSend , "utf-8"))
            except BrokenPipeError:
                print("failed to broadcast to {} because of broken pipe , deleting client".format(sock))
                sock.close()

                # delete the client data
                del GlobalData.clients[sock]






if __name__ == "__main__":


    # getting the ip address
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))


    GlobalData.host = s.getsockname()[0]

    GlobalData.serverAddress = (GlobalData.host , GlobalData.port)

    try:
        GlobalData.serverObj.bind(GlobalData.serverAddress)
    except error as e:
            # if the port number is unavailable
            if(e.errno == errno.EADDRINUSE):

                # getting the port number
                with closing(s) as s:
                    s.close()
                    # AF_INET refers to the address family ipv4. 
                    # The SOCK_STREAM means connection oriented TCP protocol.
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                    s.bind(('', 0))
                    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                        
                    # assign the port to object
                    GlobalData.port = s.getsockname()[1]

            # initialising serve object
            s.close()
            GlobalData.serverAddress = (GlobalData.host , GlobalData.port)
            GlobalData.serverObj.bind(GlobalData.serverAddress)


    # printing ip address and port number to connect
    print("IP serverAddress of the server : {}".format(GlobalData.host))
    print("port used by the server is : {}".format(GlobalData.port))
    
    GlobalData.serverObj.listen(GlobalData.maxConnectionLimit)

    print("Waiting for connection...")

    # each new connection will get a sepearte thread
    try:
        startThreading = Thread(target=HandleChat.acceptIncomingConnection)
        
        startThreading.start()
        startThreading.join()
        GlobalData.serverObj.close()
    except KeyboardInterrupt:
        GlobalData.serverObj.close()

    
