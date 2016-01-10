import socket
import threading
import Queue
import time
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#ReadThread class
class ReadThread (threading.Thread):
#ReadThread Initialization
    def __init__(self, name,csoc,screenQueue,app):
        threading.Thread.__init__(self)
        self.name = name
        self.csoc = csoc
        self.nickname = ""
        self.screenQueue = screenQueue #...
        self.app = app

    def incoming_parser(self,data):
        if data[0:4] == "TOCO":
            print "Connection Request"
        if data[0:4] == "UREJ":
            print "User Login is Rejected"
        if data[0:4] == "SESE":
            print "Session is Ended"
        if data[0:4] == "LTSA":
            print "List Game Session Answer"
        if data[0:4] == "JSAP":
            print "Join a Game Session is Approved"
        if data[0:4] == "JSDC":
            print "Join a Game Session is Declined"
        if data[0:4] == "CSAP":
            print "Create a new Game Session is Approved"
        if data[0:4] == "CSDC":
            print "Create a new Game Session is Declined"
        if data[0:4] == "GWST":
            print "Game Will Start"
        #if data[0:4] = "ATI":
        #User is getting the ticket
        if data[0:4] == "SYNM":
            #5:3 = Number
            print "Random Tombala Number is "
        if data[0:4] == "ICNK":
            #5:8 = UserName
            #13:3= Cinko Number
            print "A User Cinko information - Announced"
        if data[0:4] == "ITMB":
            #5:8 = UserName
            print "A User Tombala information - Announced"
        if data[0:4] == "CNKA":
            print "Cinko Request is Approved"
        if data[0:4] == "CNKD":
            print "Cinko Request is Declined"
        if data[0:4] == "TMBA":
            print "Tombala Request is Approved"
        if data[0:4] == "TMBD":
            print "Tombala Request is Declined"
        if data[0:4] == "INFW":
            print "Too many invlaid request, User session is ended"
        if data[0:4] == "LUCA":
            #5:8 = User Name
            #13:X= Card Information
            print "Learn Other User Card Information Answer"
        if data[0:4] == "GFNS":
            #5:8 = Winner Name
            print "Game ower Winner is ..."
        if data[0:4] == "ERRR":
            print "Command Error"

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
    def __init__(self,sendQueue,screenQueue):

        self.qt_app = QApplication(sys.argv)
        QDialog.__init__(self,None)

        self.sendQueue =sendQueue
        self.screenQueue = screenQueue

        self.setWindowTitle("Tombala Client")
        self.setMinimumSize(500,200)
        self.resize(640,480)

        self.vbox = QVBoxLayout()
        self.vbox.setGeometry(QRect(10,10,621,461))

        self.hbox = QHBoxLayout()

#Output Message 'll be shown/edited in sendMessage
        self.sendMessage = QLineEdit("",self)

        self.messageArea = QTextBrowser()

        self.send_button = QPushButton("&Send")
        #self.send_button.connect(self.send_button,SIGNAL('Clicked'),self.outgoing_parser)
        self.send_button.connect(self.send_button,SIGNAL('clicked()'),self.outgoing_parser)
        self.vbox.addLayout(self.hbox)
        self.vbox.addWidget(self.sendMessage)
        self.vbox.addWidget(self.send_button)

#Input / Output Message 'll be shown in self.messageArea
        self.hbox.addWidget(self.messageArea)
        self.setLayout(self.vbox)


        self.timer = QTimer()
        self.timer.timeout.connect(self.updateChannelWindow)
        self.timer.start(100)

    def updateChannelWindow(self):
        if self.screenQueue.qsize() > 0:
            queue_message = self.screenQueue.get()
            print('queue_message: ',queue_message)
            self.messageArea.append(queue_message)

    def run(self):
        self.show()
        self.qt_app.exec_()

    def outgoing_parser(self):
        #print "outgoing parser"
        data = self.sendMessage.text()
        self.sendQueue.put(str(data))
        self.sendMessage.clear()
        print data
        if data[0:4] == "USRS":
            #5:8 = User Name
            print "User Sign Up Request"
        if data[0:4] == "LOGI":
            #5:8 = User Name
            print "User Login"
        if data[0:4] == "LOGO":
            #5:8 = User Name
            print "User Log out"
        if data[0:4] == "LSTS":
            print "List Tombala Session"
        if data[0:4] == "JSTS":
            #5:3 = Tombala Session ID
            print "Join a Tombala Session"
        if data[0:4] == "CRTS":
            print "Create a Tombala Session"
        if data[0:4] == "SYCN":
            #5:3 = Cinko Number
            print "Announced Cinko"
        if data[0:4] == "SYTM":
            print "Announced Tombala"
        if data[0:4] == "LUCI":
            print "Request Tombala Session Card Status"


sendQueue = Queue.Queue()
screenQueue = Queue.Queue()

s=socket.socket()
host = socket.gethostname()
print host
port=12345
userName = "senol"
s.connect((host,port))

app = ClientDialog(sendQueue,screenQueue)

rt = ReadThread("ReadThread",s,screenQueue,app)
wt = WriteThread("WriteThread",s,sendQueue,screenQueue)
rt.start()
wt.start()



app.run()

rt.join()
wt.join()
s.close()
