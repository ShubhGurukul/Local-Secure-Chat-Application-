# Local-Secure-Chat-Application-
Using IP address and port number chat with anyone. This project is made by using SQLite, Cryptography, Tkinter etc.
# local-Secure-Chat
chat application to communicate with anyone on a local area network


# prerequisite

1. make sure you have python version greator than 3.6 installed
2. install packages listed in requirements.txt module
3. install tkinter

# How to use - 

### server side
1. generate new key by running python generateKey.py
2. copy thatkey and paste in globalData.py inside GlobalData class in string key
3. if you are regenerating the key , make sure to delete the previous chatDatabase.db
4. run the python serverApp.py
5. add allowed users and their key to user.csv file
example - john,mynameisjohn were john is user name and mynameisjohn is user key
6. start the serverApp.py using python
7. distribute clientApp.py and globalData.py
8. to see chat history run seeChatHistory.py


### client side
1. run the clientApp.py
2. enter ip and port to connect
3. enter your username 
4. enter your user key
5. start chatting



# license
this project is licensed under GNU GENERAL PUBLIC LICENSE VERSION 3

Visit www.letscodeofficial.com/gnuV3 for license terms

