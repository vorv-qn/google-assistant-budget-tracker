from datetime import datetime
from Database import *

class Transaction(object):
    def __init__(self, amount, transTime):
        self.amount = amount
        self.transTime = transTime

class UserObj(object):
    def __init__(self, name, id=0, budget=0, email="", existing=False, transactions=[]):
        self.name = name
        self.budget = budget
        self.email = email
        self.transactions = transactions
        self.db = Database()
        if existing:
            id = self.db.getUserFromEmail(self.email)
        self.id = id

    def getTransactions(self):
        transHist = self.db.getTransactions(self.id)
        result=''
        for row in transHist:
                result += f"{str(row[1]).replace('datetime.datetime','')} \t {str(row[2]).replace('Decimal','')}\n"
        return result
        
    def setBudget(self, _budget):
        now = datetime.now()
        self.budget = _budget
        spending = Transaction(_budget, now)
        self.transactions.append(spending)
        self.db.update(self.id, self.budget)

    def insertToDB(self):
        self.db.insert(self.name, self.budget, self.email)
        self.id = self.db.getUserFromEmail(self.email)

    def modifyBudget(self, money):
        now = datetime.now()
        spending = Transaction(money,now)
        self.budget += money
        self.transactions.append(spending)
        self.db.addTransaction(self.id, money)

    def add(self, money):
        self.modifyBudget(money)

    def sub(self, money):
        self.modifyBudget(-money)

    def getAllUsers(withTransaction = False, toStr = False):
        l = UserObj(0,"").db.getAllUsers()
        result = []
        finalStr = ""
        for e in l:
            result+=[UserObj(e[1],e[0],str(e[2]).replace('Decimal',''),e[3])]
        if toStr:
            if withTransaction:
                for e in result:
                    finalStr+=(e.toString(True))
            else:
                for e in result:
                    finalStr += e.toString()
            return finalStr
        else:
            return result

    def toString(self, withTransaction=False):
        result = f"{self.name}, {self.id}, {self.email} has a budget of ${self.budget} \n"
        if withTransaction:
            transactions = self.db.getTransactions(self.id)
            for row in transactions:
                result += f"{str(row[1]).replace('datetime.datetime','')} \t {str(row[2]).replace('Decimal','')}\n"
        return result+"\n"