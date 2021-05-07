import User
from flask import make_response, jsonify, request
from app import app
import json
from google.auth import jwt


@app.route('/', methods=['GET','POST'])
def responseJson():
    usersList = User.UserObj.getAllUsers()
    assistantRequest = (request.json)
    userInfo = jwt.decode(request.headers['Authorization'], verify=False)
    if (userInfo['iss']!='https://accounts.google.com'):
        raise Exception
    email = userInfo['email']
    name = userInfo['given_name']
    new = True
    user = User.UserObj(name, email = email)
    for e in usersList:
        if (e.email == email):
            new = False 
    if new:
        user.db.insert(name, 0, email)
    u_id = user.db.getUserFromEmail(email)
    budget = json.loads(user.db.getUser(u_id, True)[0])['budget']
    user.budget = budget
    user.id = u_id
    print(user.toString())
    sceneName = assistantRequest['scene']['name']
    if sceneName == 'Set_Budget':
        user.setBudget(float(assistantRequest['intent']['params']['amount']['resolved']))
        b = user.budget
        response = makeGAResponse(name, b)
    elif sceneName == 'Add_Budget':
        user.add(float(assistantRequest['intent']['params']['amount']['resolved']))
        b = user.budget
        response = makeGAResponse(name, b)
    elif sceneName == 'Add_Expenditure':
        user.sub(float(assistantRequest['intent']['params']['amount']['resolved']))
        b = user.budget
        response = makeGAResponse(name, b)
    elif sceneName == 'Transaction':
        res = user.getTransactions()
        response = displayTransactions(str(res))
    elif assistantRequest['handler']['name']=='fromLinkedAcct':
        res = f'Welcome to your personalized budget Tracker {name}! Your budget is ${budget}. How can I help you today?'
        response = GAResponseFromSpeech(sceneName, res)
    elif sceneName == 'Budget':
        response = GAResponseFromSpeech('Budget', f'Your budget is ${user.budget}. Anything else I can help you with?')
    r = make_response(response)
    r.headers['Content-Type']='application/json'
    return r

def displayTransactions(s):
    return jsonify({
            "prompt": {
                "override": False,
                "firstSimple": {
                "speech": "Here's your transaction history.",
                "text": s
                }
            },
            "scene": {
                "name": "Transaction",
                "slots": {},
            }
            })

def GAResponseFromSpeech(name, s):
    return jsonify({
            "prompt": {
                "override": False,
                "firstSimple": {
                "speech" : s,
                "text": ""
                }
            },
            "scene": {
                "name": name,
                "slots": {},
            }
            })

def makeGAResponse(userName, userBudget):
    return jsonify({
            "prompt": {
                "override": False,
                "firstSimple": {
                "speech": f"Okay {userName}, your budget is now ${userBudget}. Is there anything else?",
                "text": ""
                }
            },
            "scene": {
                "name": "Budget",
                "slots": {},
            }
            })

if __name__ == '__main__':
    app.run(debug=True)