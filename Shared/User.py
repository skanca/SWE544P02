import random
class User:
    def __init__(self,nickName, ip, port):
        userName = nickName
        userIP = ip
        userPort = port
        userTicket = [[0 for x in range (9)] for x in range(3)]
        userTicketState = [[0 for x in range (9)] for x in range(3)]

#    74	87	82	16	89	70	66	65	8
#    26	62	11	86	25	23	17	4	24
#    29	71	13	5	22	52	88	55	53

    def generateCard(self):
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



    minColumnNumber = 1
    maxColumnNumber = 5
    columnSize = 9
    rowSize = 3
    minNumber = 1
    maxNumber = 90
    cards = 2

user = User("UserName","IP","Port")
#user.generateCard()
#    userTicket[0][1] = 1
#    userTicket[0][8] = 7
 #   print userTicket[0][8]


