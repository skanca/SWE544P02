import Queue
import socket
import threading
import time
#import User from Shared
from Shared.User import User
import random
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class ClientGetThread(threading.Thread):
    def __init__(self,ip,port,clientSocket):
        threading.Thread.__init__(self)
        self.user = User("",ip,port)
        self.ip = ip
        self.port = port
        self.clientSocket = clientSocket
        print ("[+] New Get Thread started for "+ip + ":"+str(port))

    def checkUser(self,userName):
        findUser = False
        for us in AllSignInUsers:
            if (us == self.user.userName):
                findUser = True
                break
        return findUser

    def parseInput(self,data):
        if (not data[0:5] <> 'ISNUP') and (self.checkUser()):
            response = "LGINR"
            self.clientSocket.sendall(response)
            return False

        response = ""
        if data[0:5] == 'ISNUP':
            userName = data[6:10]
            self.user.setUserName(userName)
            AllSignInUsers.append(userName)
            response = "SNUPA" + userName
            print 'User Sign Up'
        if data[0:5] == 'ILGIN':
            response = "LGINA"
            #response = "LGINR"
            print 'User Login'
        if data[0:5] == 'ILGOT':
            response = "LGOTA"
            userName = data[6:]
            AllSignInUsers.remove(userName)
            print 'User Log out'
        if data[0:5] == 'ILSTM':
            response = "LSTMI"
            print 'List Tombala Sessions'
        if data[0:5] == 'IJNTM':
            if (requestSessionUsers.count() > 6):
                response = "JNTMR"
            else:
                response = "JNTMA"
                requestSessionUsers.append(self.user)
            #response = "JNTMR"
            print 'Join a Tombala Session'
        if data[0:5] == 'ICRTM':
            if (requestSessionUsers.count() == 0):
                response = "CRTMA"
                requestSessionUsers.append(self.user)
            else:
                response = "CRTMR"
            #response = "CRTMR"
            print 'Create a Tombala Session'
        if data[0:5] == 'IANCN':
            response = "ANCNA"
            cinkoNumber = data[6:3]
            if cinkoNumber < 1 or cinkoNumber > 3:
                response = "ERRRR"
            else:
                if self.user.ticket.checkCinko(cinkoNumber):
                    #response = "ANCNA"
                    response = ""
                    broadCastCinko(self.user.userName,cinkoNumber)
                else:
                    response = "ANCNR"
            #response = "ANCNR"
            #+check Cinko
            #+2.response is IBRCN username cinkonumber
            print 'Announce Cinko'
        if data[0:5] == 'IANTM':
            tombalaMi = True
            if (self.user.ticket.checkTombala()):
                #response = "ANTMA"
                response = ""
                broadCastTombala(self.user.userName)
            else:
                response = "ANTMR"
            #response = "ANTMR"
            #+check Tombala
            #+2.response is IBRTM username
            #+3.response is IGMFN username
            print 'Say Tombala'
        if data[0:5] == 'ANNMA':
            self.user.setLastNumberApproved(True)
            response = ""
            #in a timer event every 5 miniute, if all user lastNumberApproved is True, then generate a new number
#            number = generateNumber()
#            broadCastNumber(number)
#            print "generate new number"
            print "Announced Number Approved"
        print response
        if (response <> ""):
            self.clientSocket.sendall(response)
            #+User and User Info List

    def run(self):
        while True:
            data = self.csocket.recv(1024)
            print data
            if not data:
                break
            self.parseInput(data)

""""
        if data[0:5] == "IRQGM":
            print "Game Info request"
            response = "GMINF"
"""""



class ClientSendThread(threading.Thread):
    def __init__(self,ip,port,clientSocket,sendQueue):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.clientSocket = clientSocket
        self.sendQueue = sendQueue
        print ("[+] New Send Thread started for " + ip + ":" + str(port))

    def sendtoAll(self,data):
        for thread in sendThreads.get():
            thread.clientSocket.sendall(data)
            print data
            #thread

    def send(self,data):
        self.clientSocket.sendall(data)

    def run(self):
        while True:
            #print "Welcome to the server. Type something and hit enter"
            if self.sendQueue.qsize() > 0:
                queue_message = self.sendQueue.get()
                try:
                    self.clientSocket.send(queue_message)
                except socket.error:
                    self.clientSocket.close()


""""
    if (RequestedBingoSessionUsers._qsize() >= 3) and (RequestedBingoSessionUsers.qsize() <= 6):
        print "hello new game"
        ActiveBingoSessionUsers.queue.clear()
        for user in RequestedBingoSessionUsers.get():
            user.generateCard()
            ActiveBingoSessionUsers.put(user)

"""""


def checkStartGame():
    for activeSendThread in sendThreads:
        activeSendThread.user.ticket.generateTicket()
        userTicket = activeSendThread.user.ticket.getTicketValueStream()
        message = "IGMST" + str(activeSendThread.user.ticket.getTicketValueStream())
        activeSendThread.send(message)
        print message

    print "checkToStartGame"

def checkSendNumber(self):
    print "number Generator"
    generateNumber = True
    for activeSendThread in sendThreads:
        if (not activeSendThread.user.lastNumberApproved):
            generateNumber= False
            break
    if (generateNumber):
        number = random.sample(range(1,90),89)
        for activeSendThread in sendThreads:
            message = "IANNM" + str(number).zfill(2)
            activeSendThread.send(message)

    print "generateNumber"

def broadCastCinko(self,userName,cinkoID):
    for uthread in sendThreads:
        message = "IBRCN" + userName + cinkoID
        uthread.csocket.sendAll(message)
    print "broadcast Cinko"

def broadCastTombala(self,userName):
    for uthread in sendThreads:
        message = "IBRTM" + userName
        uthread.csocket.sendAll(message)
    print "broadcast Tombala"

def broadCastNumber(self,number):
    for uthread in sendThreads:
        message = "IANNM" + str(number).zfill(2)
        uthread.csocket.sendAll(message)
    print "broadcast Number"

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

#ActiveBingoSessionUsers = Queue.Queue()
#RequestedBingoSessionUsers = Queue.Queue()

AllSignInUsers = []
getThreads = []
sendThreads = []
activeSessionUsers = []
requestSessionUsers = []

#ActiveBingoSessionNumber = [0 for x in range (90)]

timer = threading.Timer(30.0,checkStartGame)
timer.start()

#timer = threading.Timer(30.0,generateNumber)
#timer.start()

s = socket.socket()
host = socket.gethostname()
port = 12345
s.bind((host,port))
s.listen(5)

while True:
    (clientSocket,(ip,port)) = s.accept()
    newGetThread = ClientGetThread(ip,port,clientSocket)
    getThreads.append(newGetThread)
    newGetThread.start()

    sendQueue = Queue.Queue()
    newSendThread = ClientSendThread(ip,port,clientSocket,sendQueue)
    sendThreads.append(newSendThread)
    newSendThread.start()









