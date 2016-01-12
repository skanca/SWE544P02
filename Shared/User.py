import string
from Shared import Ticket
class User:
    def __init__(self,userName, ip, port):
        self.userName = string.ljust(userName,10,' ')
        self.userIP = ip
        self.userPort = port
        self.ticket = Ticket.Ticket(3,9,1,90)
        self.lastNumberApproved = True

    def setUserName(self,userName):
        self.userName = userName

    def setLastNumberApproved(self,value):
        self.lastNumberApproved = value








