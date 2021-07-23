# for local communication
from socket import AF_INET, socket, SOCK_STREAM,gethostbyname,gethostname

# for threading chats
from threading import Thread

# for encryption
from cryptography.fernet import Fernet



class GlobalData:
    clients = {}
    addresses = {}

    #To find ip of my lan network. CLI command : ifconfig
    host = None
    
    port = 5000
    bufferSize = 1024
    serverAddress = (host, port)

    # initialising socket model
    serverObj = socket(AF_INET, SOCK_STREAM)

    # encryption key in string
    stringKey = "UEaypM0hsHuxt3iQ0g23OgQS3L_pUGT_luFuF4mcuCg="
    
    # An initialization vector (IV) is an arbitrary number that can be used along with a secret key for data encryption.
    key = bytes(stringKey , "utf-8")
    cipherSuite = Fernet(key)

    welcomeMessage = "Welcome to local-secure-chat"

    quitStatement = "okquit"

    maxConnectionLimit = 7