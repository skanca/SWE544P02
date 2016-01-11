import socket
import threading
import Queue
import time
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from Shared.User import User

#ReadThread class
class ReadThread (threading.Thread):
#ReadThread Initialization
    def __init__(self, name,csoc,screenQueue,app):
        threading.Thread.__init__(self)
        self.name = name
        self.csoc = csoc
        self.screenQueue = screenQueue #...
        self.app = app

    def incoming_parser(self,data):
        response = ""
        if data[0:5] == "ICHCN":
            print "Check Connection"
            response = "CHCNA"
        if data[0:5] == "SNUPA":
            print "SignUp Request is Approved"
        if data[0:5] == "SNUPR":
            print "SignUp Request is Rejected"
        if data[0:5] == "LGINA":
            print "Login Request is Approved"
        if data[0:5] == "LGINR":
            print "Login Request is Rejected"
        if data[0:5] == "LGOTA":
            print "Log out Request is Approved"
        if data[0:5] == "LGOTR":
            print "Log out Request is Rejected"
        if data[0:5] == "LSTMI":
            print "List Tombala Request Result"
            #6-5: Session Number
            #11-: User List (10 chracter for each user)
        if data[0:5] == "JNTMA":
            print "Join to Active Tombala Session (not started yet) Approved"
        if data[0:5] == "JNTMR":
            print "Join to Active Tombala Session (not started yet) Rejected"
        if data[0:5] == "CRTMA":
            print "Create a Tombala Session is Approved"
        if data[0:5] == "CRTMR":
            print "Create a Tombala Session is Rejected"
        if data[0:5] == "ANCNA":
            print "Announce Cinko Request is Approved"
        if data[0:5] == "ANCNR":
            print "Announce Cinko Request is Invalid"
        if data[0:5] == "ANTMA":
            print "Announce Tombala Request is Approved"
        if data[0:5] == "ANTMA":
            print "Announce Tombala Request is Approved"
        if data[0:5] == "IANNM":
            print "Announce Number"
            number = data[6:3]
            user.checkSetNumber(number)
            cinkoMu = user.checkForCinko()
            tombalaMi = user.checkForResult()
            if user.tombalaMi:
                response = "IANTM" + user.userName
                self.csoc.sendall(response)
            elif user.cinkoMu:
                response = "IANCN" + user.userName
                self.csoc.sendall(response)
            else:
                response = "ANNMA"
                self.csoc.sendall(response)
        if data[0:5] == "IBRCN":
            print "Broad Cast Cinko"
            #6-10: UserName
            #16-3: Cinko Number
        if data[0:5] == "IBRTM":
            print "Broad Cast Tombala"
            #6-10: UserName
        if data[0:5] == "GMINF":
            print "Game Info"
            #6-: User List and User Info

#ReadThread run
    def run(self):
        while True:
            try:
                data = self.csoc.recv(1024)
                if data <> '':
                    outtext = time.strftime("[%H:%M:%S] - Server - : ", time.gmtime())+data
                    print(outtext)
                    self.screenQueue.put(outtext)
                    self.incoming_parser(data)
            except:
                pass
            if data[0:3] == "BYE":
                self.csoc.close()


class WriteThread (threading.Thread):
#WriteThread initialization
    def __init__(self,name,csoc, sendQueue,screenQueue):
        threading.Thread.__init__(self)
        self.name = name
        self.csoc = csoc
        self.sendQueue = sendQueue
        self.screenQueue = screenQueue
#WriteThread run
    def run(self):
        while True:
            if self.sendQueue.qsize() > 0:
                queue_message = self.sendQueue.get()
                try:
                    outtext = time.strftime("[%H:%M:%S] - Local - : ", time.gmtime())+queue_message
                    self.screenQueue.put(outtext)
                    self.csoc.send(queue_message)
                except socket.error:
                    self.csoc.close()
#                    break

class ClientDialog(QDialog):
    def __init__(self,sendQueue,screenQueue,user):
        self.qt_app = QApplication(sys.argv)
        QDialog.__init__(self,None)
        self.sendQueue =sendQueue
        self.screenQueue = screenQueue
        self.user = user

        self.setWindowTitle("Tombala Client")
        self.setMinimumSize(500,200)
        self.resize(640,480)

        self.vbox = QVBoxLayout()
        self.vbox.setGeometry(QRect(10,10,621,461))

        self.hbox = QHBoxLayout()
#Output Message 'll be shown/edited in sendMessage
        self.sendMessageLabel = QLabel("Message: ")
        self.sendMessageEdit = QLineEdit("",self)

        self.userNameLabel = QLabel("User Name: ")
        self.userNameEdit = QLineEdit("",self)
        self.signOnbutton = QPushButton("&Save")
        self.signOnbutton.connect(self.signOnbutton,SIGNAL('clicked()'),self.setUserName)

        self.messageArea = QTextBrowser()

        self.send_button = QPushButton("&Send")
        #self.send_button.connect(self.send_button,SIGNAL('Clicked'),self.outgoing_parser)
#        self.send_button.connect(self.send_button,SIGNAL('clicked()'),self.outgoing_parser)
        self.send_button.connect(self.send_button,SIGNAL('clicked()'),self.putSendQueue)

        self.hbox.addWidget(self.userNameLabel)
        self.hbox.addWidget(self.userNameEdit)
        self.hbox.addWidget(self.signOnbutton)
        self.vbox.addLayout(self.hbox)

        self.hbox.addWidget(self.sendMessageLabel)
        self.hbox.addWidget(self.sendMessageEdit)
        self.hbox.addWidget(self.send_button)
        self.vbox.addLayout(self.hbox)

#Input / Output Message 'll be shown in self.messageArea
        self.vbox.addWidget(self.messageArea)
        self.setLayout(self.vbox)


        self.timer = QTimer()
        self.timer.timeout.connect(self.updateMessageWindow)
        self.timer.start(100)

    def updateMessageWindow(self):
        if self.screenQueue.qsize() > 0:
            queue_message = self.screenQueue.get()
            print('queue_message: ',queue_message)
            self.messageArea.append(queue_message)

    def run(self):
        self.show()
        self.qt_app.exec_()

    def setUserName(self):
        self.user.userName = self.userNameEdit.text()
        print self.user.userName

    def putSendQueue(self):
        out_message = ""
        #print "outgoing parser"
        data = self.sendMessageEdit.text()
        self.sendMessageEdit.clear()
        print data
        if data[0:5] == "ISNUP":
            out_message = "ISNUP" + self.user.userName
            #6:10 = User Name
            print "User Sign Up Request", out_message
        if data[0:5] == "ILGIN":
            out_message = "ILGIN" + self.user.userName
            #6:10 = User Name
            print "User Login Request"
        if data[0:5] == "ILGOT":
            out_message = "ILGOT" + self.user.userName
            #6:10 = User Name
            print "User Log out Request"
        if data[0:5] == "ILSTM":
            out_message = "ILSTM"
            print "List Tombala Session"
        if data[0:5] == "IJNTM":
            out_message = "IJNTM"
            #6:3 = Tombala Session ID
            print "Join a Tombala Session"
        if data[0:5] == "ICRTM":
            out_message = "ICRTM"
            print "Create a Tombala Session"
        if data[0:5] == "IANCN":
            out_message = "IANCN"
            #6:3 = Cinko Number
            print "Announced Cinko"
        if data[0:5] == "IANTM":
            out_message = "IANTM"
            print "Announced Tombala"
        if data[0:4] == "IRQGM":
            out_message = "IRQGM"
            print "Request Tombala Session Card Status"
        if out_message <> "":
            self.sendQueue.put(str(out_message))

sendQueue = Queue.Queue()
screenQueue = Queue.Queue()

s=socket.socket()
host = socket.gethostname()
#print host
port=12345

user = User("",host,port)

s.connect((host,port))

app = ClientDialog(sendQueue,screenQueue,user)

rt = ReadThread("ReadThread",s,screenQueue,app)
wt = WriteThread("WriteThread",s,sendQueue,screenQueue)

rt.start()
wt.start()

app.run()

rt.join()
wt.join()

s.close()
