import Queue
import socket
import threading
import time
#import User from Shared
from Shared.User import User
from PyQt4.QtCore import *
from PyQt4.QtGui import *

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
#        if data[0:4] == 'SIGNUP':
#            response = "TOCO"
#            print 'Check Connection'
        if data[0:5] == 'ISNUP':
            response = "SNUPA"
            #response = "SNUPR"
            print 'User Sign Up'
        if data[0:5] == 'ILGIN':
            response = "LGINA"
            #response = "LGINR"
            print 'User Login'
        if data[0:5] == 'ILGOT':
            response = "LGOTA"
            print 'User Log out'
        if data[0:5] == 'ILSTM':
            response = "LSTMI"
            print 'List Tombala Sessions'
        if data[0:5] == 'IJNTM':
            response = "JNTMA"
            #response = "JNTMR"
            print 'Join a Tombala Session'
        if data[0:5] == 'ICRTM':
            response = "CRTMA"
            #response = "CRTMR"
            print 'Create a Tombala Session'
        if data[0:5] == 'IANCN':
            response = "ANCNA"
            #response = "ANCNR"
            #+check Cinko
            #+2.response is IBRCN username cinkonumber
            print 'Announce Cinko'
        if data[0:5] == 'IANTM':
            response = "ANTMA"
            #response = "ANTMR"
            #+check Tombala
            #+2.response is IBRTM username
            #+3.response is IGMFN username
            print 'Say Tombala'
        if data[0:5] == 'ANNMA':
            print "generate new number"
            #response = "ANTMA"
        if data[0:5] == "IRQGM":
            print "Game Info request"
            response = "GMINF"
            #+User and User Info List

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
def checkToStartGame():
    if (RequestedBingoSessionUsers._qsize() >= 3) and (RequestedBingoSessionUsers.qsize() <= 6):
        print "hello new game"
        ActiveBingoSessionUsers.queue.clear()
        for user in RequestedBingoSessionUsers.get():
            user.generateCard()
            ActiveBingoSessionUsers.put(user)

ActiveBingoSessionUsers = Queue.Queue()
RequestedBingoSessionUsers = Queue.Queue()
ActiveBingoSessionNumber = [0 for x in range (90)]

timer = QTimer()
timer.timeout.connect(checkToStartGame)
# #update every 10 ms
timer.start(100)

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


def numberGenerator(self):
    print "number Generator"

#will be in User object
#def cardGenerator(self):
#    print "card Generator"

#will be in User object
#def setNumberInCards(self):
#    print "set number in cards"

#will be in User object
#def checkCinko(self,userName, cinkoID):
#    print "check Cinko"
#   cinkoUserCard[][] = getUserCard()

#will be in User object
#def checkTombala(self,userName):
#    print "check Tombala"

def broadCastCinko(self,userName,cinkoID):
    print "broadcast Cinko"

def broadCastTombala(self,userName):
    print "broadcast Tombala"








