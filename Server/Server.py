import Queue
import socket
import threading
import time
#import User from Shared
from Shared.User import User



class ClientGetThread(threading.Thread):
    def __init__(self,ip,port,clientSocket):
        threading.Thread.__init__(self)
        userName = ""
        self.user = User(userName,ip,port)
       # self.ActiveBingoSessionUser.append(self.user)
       # self.RequestedBingoSessionUser.append(self.user)
        self.ip = ip
        self.port = port
        self.csocket = clientSocket
        print ("[+] New Get Thread started for "+ip + ":"+str(port))

    def parseInput(self,data):
        response = ""
        if data[0:4] == 'TICI':
            response = "TOCO"
            print 'Check Connection'
        if data[0:4] == 'USRS':
            response = "UAPR"
            print 'User Sign Up'
        if data[0:4] == 'LOGI':
            response = "UAPR"
            print 'User Login'
        if data[0:4] == 'LOGO':
            response = "SESE"
            print 'User Log out'
        if data[0:4] == 'LSTS':
            response = "LTSA"
            print 'List Tombala Sessions'
        if data[0:4] == 'JNTS':
            response = "JNAP"
            print 'Join a Tombala Session'
        if data[0:4] == 'CRTS':
            response = "CSAP"
            print 'Create a Tombala Session'
        if data[0:4] == 'SYCN':
            response = "CNKA"
            print 'Say Cinko'
        if data[0:4] == 'SYTM':
            response = "TMBA"
            print 'Say Tombala'
        print response
        self.csocket.sendall(response)

    def run(self):
        while True:
            data = self.csocket.recv(1024)
            print data
            if not data:
                break
            self.parseInput(data)

""""
            data = "someinfo"
            self.csocket.sendall(data)
            data = self.csocket.recv(56)
            time.sleep(8)
"""""


class ClientSendThread(threading.Thread):
    def __init__(self,ip,port,clientSocket):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.csocket = clientSocket
        print ("[+] New Send Thread started for " + ip + ":" + str(port))

    def run(self):
        print "Welcome to the server. Type something and hit enter"
        while True:
            a= 15
            #print "111"
            #if qsize

            #

#ActiveBingoSessionUsers = Queue()
#RequestedBingoSessionUsers = Queue()
ActiveBingoSessionNumber = [0 for x in range (90)]

s = socket.socket()
host = socket.gethostname()
port = 12345
s.bind((host,port))
s.listen(5)

while True:
    (clientSocket,(ip,port)) = s.accept()
    newGetThread = ClientGetThread(ip,port,clientSocket)
    newGetThread.start()

    newSendThread = ClientSendThread(ip,port,clientSocket)
    newSendThread.start()


#def cardGenerator(self):

def numberGenerator(self):
    print "number Generator"
#

def setNumberInCards(self):
    print "set number in cards"
#

def checkCinko(self,userName, cinkoID):
    print "check Cinko"
#   cinkoUserCard[][] = getUserCard()

def broadCastCinko(self,userName,cinkoID):
    print "broadcast Cinko"

def broadCastTombala(self,userName):
    print "broadcast Tombala"

def checkTombala(self,userName):
    print "check Tombala"







