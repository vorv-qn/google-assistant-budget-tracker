from app import app
from flask_assistant import Assistant, tell, ask, event
import User
import Database
import json

user_id = 0
email = ''
name = ''
userInfo = [user_id, name, email]
db = Database.Database()
assist = Assistant(app,project_id='budget-tracker-v1-fa53b')
usersList = User.UserObj.getAllUsers()
def checkExistant():
    if userInfo[0] == 0:
        return False
    return True

def askForEmail():
    return ask("You haven't provided your email. Please enter it.")

@assist.action('Default_Welcome_Intent')
def welcome():
    #print(assist.client_id)
    return ask("Welcome to your personalized Budget Tracker! Please enter your email.")

@assist.action('getEmail', mapping={'userEmail' : 'sys.email'})
def checkIfExistant(userEmail):
    flag = False
    userInfo[2] = userEmail
    for e in usersList:
        print(e.toString())
        if (e.email == userEmail):
            u = e
            userInfo[0] = e.id
            userInfo[1] = e.name
            flag = True
            break
    print(tell(f"Hello {u.name}, your budget is ${u.budget}"))
    if flag:
        return tell(f"Hello {u.name}, your budget is ${u.budget}")
    return ask("Hello, it looks like this is your first time using this skill. Please enter your name.")

@assist.action('getName', mapping={'userName' : 'sys.person'})
def getName(userName):
    name = userName["name"]
    userInfo[1] = name
    #if (userInfo[0] == 0):
    #    return checkIfExistant(userInfo[2])
    u = User.UserObj(name, email = userInfo[2])
    #try: 
    u.insertToDB()
    #finally:
    userInfo[0] = u.id
    return tell(f"Hello, {u.name}, your budget was set to ${u.budget}")

@assist.action('getInfo')
def getInfo():
    return tell(f"{userInfo[0]}, {userInfo[1]}, {userInfo[2]}")

@assist.action('getBudget')
def getBudget():
    budget = 0
    userInfo[1] = "Elie"
    '''  
    if (checkExistant()==False):
        return askForEmail()
    userJson = json.loads(db.getUser(userInfo[0], True)[0])
    budget = userJson["budget"]
    print(budget)'''
    return tell(f"Hello {userInfo[1]}, your budget is ${budget}")

@assist.action('setBudget', mapping={'num': 'sys.unit-currency'})
def setBudget(num):
    #print(f"{userInfo[0]} {num}")
    db.update(userInfo[0], num["amount"])
    return tell("Your budget was updated successfully")

@assist.action('addBudget', mapping={'num': 'sys.unit-currency'})
def addToBudget(num):
    amount = num["amount"]
    db.addTransaction(userInfo[0], amount)
    budget = json.loads(db.getUser(userInfo[0], True)[0])["budget"]
    return tell(f"Okay, your budget is now ${budget}")

@assist.action('addExpenditure', mapping={'num':'sys.unit-currency'})
def removeFromBudget(num):
    amount = - num["amount"]
    db.addTransaction(userInfo[0], amount)
    budget = json.loads(db.getUser(userInfo[0], True)[0])["budget"]
    return tell(f"Okay, your budget is now ${budget}")

if __name__=='__main__':
    app.run(debug=True)