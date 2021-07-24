# for local communication
from socket import AF_INET, socket, SOCK_STREAM

# for threading chats
from threading import Thread

# for GUI
import tkinter as tk
from tkinter import *

# for encryption
from globalData import GlobalData

import sys
import time


count = 0




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


# class containing tkinter objects
class TkObjects:
    tkObj = tk.Tk()
    messagesFrame = tk.Frame(tkObj)
    myMessage = tk.StringVar()
    scrollBar = tk.Scrollbar(messagesFrame)
    messageList = tk.Listbox(messagesFrame , height=25 , width=70 , font=('Times', 20) , yscrollcommand=scrollBar.set)
    entryField = tk.Entry(tkObj , textvariable=myMessage , background = "#D3D3D3" , font = "Helvetica 20",width=50)
    sendButton = tk.Button(tkObj , text="Send")



# class to handle the client connection
class HandleConnection:

    # function to receive a message from server and print it to message frame
    @classmethod
    def receive(cls):
        while(True):                                             
            try:
                message = GlobalData.serverObj.recv(GlobalData.bufferSize)

                # decrypting message
                message = str(message , "utf-8")
                message = HandleEncryption.decryptor(message)


                TkObjects.messageList.insert(tk.END , message)
                TkObjects.messageList.see(tk.END)


                if(message == "You are not allowed to join , ending connection"):
                    time.sleep(2)
                    TkObjects.tkObj.quit()
                    sys.exit()

                if(message == "invalid key , ending connection"):
                    time.sleep(2)
                    TkObjects.tkObj.quit()
                    sys.exit()

            except OSError:
                break
            except RuntimeError:
                break

    
    # function to send a message to the server
    @classmethod
    def send(cls , event=None):

        global count 

        message = TkObjects.myMessage.get()

                

        # encrypting the message
        tempMessage = message
        message = HandleEncryption.encryptor(message)

        TkObjects.myMessage.set("")

        # sending the message
        GlobalData.serverObj.sendto(bytes(message , "utf-8") , GlobalData.serverAddress)

        # if messgae was to quit
        if(tempMessage == GlobalData.quitStatement):
            GlobalData.serverObj.close()
            TkObjects.tkObj.quit()


    # function to quit the application
    @classmethod
    def onClose(cls , event=None):
        TkObjects.myMessage.set(GlobalData.quitStatement)
        cls.send()
        TkObjects.tkObj.quit()

    








if __name__ == "__main__":

    # making up the gui
    TkObjects.tkObj.title("local-secure-chat")

    # hiding the gui window
    TkObjects.tkObj.withdraw()

    TkObjects.myMessage.set("Type Here")

    TkObjects.scrollBar.pack(side=tk.RIGHT , fill=tk.Y)

    TkObjects.messageList.pack(side = tk.LEFT , fill=tk.BOTH)
    TkObjects.messageList.pack()
    TkObjects.messageList.see(tk.END)

    TkObjects.messagesFrame.pack()

    TkObjects.entryField.bind("<Return>" , HandleConnection.send)
    TkObjects.entryField.pack(padx=20, pady=20)
    TkObjects.entryField.focus()


    TkObjects.sendButton = tk.Button(TkObjects.tkObj , text="Send" , command=HandleConnection.send , font = "Helvetica 20 bold" , height = 2, width = 20 , bg='green')
    TkObjects.sendButton.pack()

    TkObjects.tkObj.protocol("WM_DELETE_WINDOW", HandleConnection.onClose)


    # getting the host and port to connect
    GlobalData.host = input("Enter HOST ip address : ")
    GlobalData.port = input("Enter HOST port address : ")

    GlobalData.port = int(GlobalData.port)

    GlobalData.serverAddress = (GlobalData.host , GlobalData.port)

    # init server
    GlobalData.serverObj.connect(GlobalData.serverAddress)

    # init receiving thread
    receivingThread = Thread(target=HandleConnection.receive)
    receivingThread.start()

    # showing the window
    TkObjects.tkObj.deiconify()
    tk.mainloop()

    




