from flask import make_response, jsonify, request, Response
from flask_accept import accept
from app import app
import Database
import json

db = Database.Database()

@app.route('/users/<id>')
def getUser(id):
    result = db.getUser(id, True)[0]
    return json.loads(result)

@app.route('/transactions/<id>')
def getTransactions(id):
    result = db.getTransactions(id, True)
    r = str(result[0][0])
    #r = make_response(jsonify(result[0][0]), 200)
    return r

@app.route('/delete/<id>')
def deleteUser(id):
    try:
        db.deleteUser(id)
        return make_response(jsonify({f"user {id}":"deleted"}), 200)
    except:
        return make_response(jsonify({"error": "Not found"}), 404)

@app.route('/add', methods=['GET','POST'])
def addToBudget():
    if request.args:
        jsonAdd = json.loads("{" + ", ".join((f"\"{k}\": \"{v}\"") for k,v in request.args.items()) + "}")
        db.addTransaction(jsonAdd["id"], jsonAdd["amount"])
        budget = json.loads(db.getUser(jsonAdd["id"], True)[0])["budget"]
        #db.update(jsonAdd["id"], budget+float(jsonAdd["amount"]))
        return make_response(jsonify(json.loads(db.getUser(jsonAdd["id"], True)[0])), 200)
    return make_response(jsonify({"error": "Not found"}), 404)

if __name__=='__main__':
    app.run(debug=True)