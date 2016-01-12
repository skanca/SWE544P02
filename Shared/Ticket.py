import random
class Ticket:
    def __init__(self,rowNumber,columnNumber,minNumber,maxNumber):
        self.rowNumber = rowNumber
        self.columnNumber = columnNumber
        self.minNumber = minNumber
        self.maxNumber = maxNumber
        self.TicketValue = [[0 for x in range (self.columnNumber)] for x in range(self.rowNumber)]
        self.TicketState = [[0 for x in range (self.columnNumber)] for x in range(self.rowNumber)]

    def generateTicket(self):
        randRange = range(self.minNumber,self.maxNumber)
        ticket = []
        ticket = random.sample(randRange,self.rowNumber * self.columnNumber)
        for index1 in range (self.rowNumber):
            for index2 in range (self.columnNumber):
                self.TicketValue[index1][index2] = ticket[(index1 - 1) * self.columnNumber + index2]
                self.TicketState[index1][index2] = ticket[(index1 - 1) * self.columnNumber + index2]

    def getTicketValueStream(self):
        ticketValueStream = ""
        for index1 in range(self.rowNumber):
            for index2 in range (self.columnNumber):
                ticketValueStream += str(self.TicketValue[index1][index2]).zfill(2) + str(" ")
        print ticketValueStream
        return ticketValueStream

    def getTicketStateStream(self):
        ticketStateStream = ""
        for index1 in range(self.rowNumber):
            for index2 in range (self.columnNumber):
                ticketStateStream += str(self.TicketState[index1][index2]).zfill(2) + str(" ")
        print ticketStateStream
        return ticketStateStream

    def checkSetNumber(self,number):
        for index1 in range (self.rowNumber):
            for index2 in range (self.columnNumber):
                if self.TicketValue[index1][index2] == number:
                    self.TicketState[index1][index2] = "*"

    def checkCinko(self,cinkoNumber):
        cinkoMu = True
        for index1 in range(self.columnNumber):
            if self.TicketState[cinkoNumber][index1] <> "*":
                cinkoMu = False
                break
        return cinkoMu

    def checkTombala(self):
        tombalaMi = True
        for index1 in range(self.rowNumber):
            for index2 in range(self.columnNumber):
                if self.TicketState[index1][index2] <> "*":
                    tombalaMi = False
                    break
        return tombalaMi

#ticketa = Ticket(3,9,1,90)
#ticketa.generateTicket()
#ticketastream = ticketa.getTicketStateStream()
