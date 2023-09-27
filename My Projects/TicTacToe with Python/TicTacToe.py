class game():
    def __init__(self):
        self.board=[]
        for i in range(4):
            temp = []
            for j in range(4):
                temp.append('-')
            self.board.append(temp) 

    def printb(self):
        print("    0  1  2  3 \n")
        for i in range(4):
            print(f"{i} : ",end= " ")
            for j in range(4):
                print(f"{self.board[i][j]} ",end=" ")
            print("\n")

    def setx(self,row,col):
        if(self.board[row][col]=='-'):
            self.board[row][col] = 'X'
            return 1
        else:
            return 0
            
    def setO(self,row,col):
        if(self.board[row][col]=='-'):
            self.board[row][col] = 'O'
            return 1
        else:
            return 0
    
    def checkO(self):
        for i in range(4):
            ccount = 0
            for j in range(4):
                if(self.board[i][j] == 'O'):
                    ccount += 1
                else:
                    break
            if(ccount == 4):
                return 1
        
        for i in range(4):
            rcount = 0
            for j in range(4):
                if(self.board[j][i] == 'O'):
                    rcount += 1
                else:
                    break
            if(rcount == 4):
                return 1
        d1count = 0
        d2count = 0
        k = 3
        for i in range(4):
            if(self.board[i][i]=='O'):
                d1count += 1
        if(d1count == 4):
            return 1
        for i in range(4):
            if self.board[i][k] == 'O':
                d2count += 1
            else:
                break
            k -= 1
        if d2count == 4:
            return 1
        return 0
    
    def checkX(self):
        for i in range(4):
            ccount = 0
            for j in range(4):
                if(self.board[i][j] == 'X'):
                    ccount += 1
                else:
                    break
            if(ccount == 4):
                return 1
        
        for i in range(4):
            rcount = 0
            for j in range(4):
                if(self.board[j][i] == 'X'):
                    rcount += 1
                else:
                    break
            if(rcount == 4):
                return 1
        d1count = 0
        d2count = 0
        k = 3
        for i in range(4):
            if(self.board[i][i]=='X'):
                d1count += 1
        if(d1count == 4):
            return 1
        for i in range(4):
            if self.board[i][k] == 'X':
                d2count += 1
            else:
                break
            k -= 1
        if d2count == 4:
            return 1
        return 0


xox = game()
n1 = str(input("Enter X user's name: "))
n2 = str(input("Enter O user's name: "))
t = 0
for i in range(8):
    xox.printb()
    xpr = int(input("Enter row for 'X'    :"))
    xpc = int(input("Enter column for 'X' :"))
    while(not(xox.setx(xpr,xpc))):
        print("Please enter the row and column where there is no 'X' and 'O'")
        xpr = int(input("Enter row for 'X'    :"))
        xpc = int(input("Enter column for 'X' :"))
    if xox.checkX():
        t = 1
        print("\n'X' user is the winner. Congrats " + n1 + " !\n")
        xox.printb()
        break
    xox.printb()
    opr = int(input("Enter row for 'O'    :"))
    opc = int(input("Enter column for 'O' :"))
    while(not(xox.setO(opr,opc))):
        print("Please enter the row and column where there is no 'X' and 'O'")
        opr = int(input("Enter row for 'O'    :"))
        opc = int(input("Enter column for 'O' :"))
    if xox.checkO():
        t = 1
        print("\n'O' user is the winner. Congrats " + n2 + " !\n")
        xox.printb()
        break
if t==0:
    print("OOPS! the game is a tie. Well Played.")
