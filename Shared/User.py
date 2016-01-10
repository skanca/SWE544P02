import random
class User:
    def __init__(self,nickName, ip, port):
        self.userName = nickName
        self.userIP = ip
        self.userPort = port
        self.userTicketColumnSize = 9
        self.userTicketRowSize = 3
        self.userTicketMinNumber = 1
        self.userTicketMaxNumber = 90
        self.userTicket = [[0 for x in range (9)] for x in range(3)]
        self.userTicketState = [[0 for x in range (9)] for x in range(3)]

#    74	87	82	16	89	70	66	65	8
#    26	62	11	86	25	23	17	4	24
#    29	71	13	5	22	52	88	55	53

    def generateCard(self):
        randRange = range(self.userTicketMinNumber,self.userTicketMaxNumber)
        card = []
        card = random.sample(randRange,self.userTicketRowSize * self.userTicketColumnSize)

        for index1 in range (self.userTicketRowSize):
            for index2 in range (self.userTicketColumnSize):
                self.userTicket[index1][index2] = card[(index1 - 1) * self.userTicketColumnSize + index2]
                self.userTicketState[index1][index2] = card[(index1 - 1) * self.userTicketColumnSize + index2]
                print "index1 = ", index1
                print "index2 = ", index2
                print "value  = ", self.userTicket[index1][index2]

    def checkSetNumber(self,number):
        rowSize = 3
        columnSize = 9
        find = False
        for index1 in range (rowSize):
            for index2 in range (columnSize):
                if self.userTicket[index1][index2] == number:
                    find = True
                    #self.userTicket[index1][index2] = "*"
                    self.userTicketState[index1][index2] = "*"
        return find

user = User("senol","ip","port")
user.generateCard()
""""
        print "card Generator"
        for h in range(self.cards):
            card = []
            randRange = range(self.minNumber,self.maxNumber)
            card = random.sample(randRange,self.rowSize * self.columnSize )

            columnRange = range(self.minColumnNumber,self.maxColumnNumber)
            selectedColumns = random.sample(columnRange,9)
            for i in range(self.rowSize):
                string = ""
                for j in range (self.columnSize):
                    string += str(card[i+j*self.rowSize]) + "\t"
                print string
            print "n"
"""""







