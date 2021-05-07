import mysql.connector

class Database(object):
    def __init__(self, dbUser='user', dbPassword='password', dbHost='host', dbDatabase='database'):
        self.db = mysql.connector.connect(user=dbUser, password=dbPassword,
                                    host=dbHost,
                                    database=dbDatabase, port=3306, ssl_verify_cert=True, ssl_ca='BaltimoreCyberTrustRoot.crt.pem')

    def getAllUsers(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT id, name, budget, email FROM USERS")
        #print (cursor.fetchall())
        return cursor.fetchall()

    def insert(self, name, budget, email):
        cursor = self.db.cursor()
        sqlInsertUser = f"INSERT INTO USERS (name, budget, email) VALUES ('{name}', {budget}, '{email}');"
        cursor.execute(sqlInsertUser)
        self.db.commit()
        #print(cursor.rowcount, "record(s) affected")
    
    def update(self, id, newBudget):
        cursor = self.db.cursor()
        sqlUpdate = f"UPDATE USERS SET budget = {newBudget} WHERE id = {id};"
        cursor.execute(sqlUpdate)
        self.db.commit()

    def addTransaction(self, id, amount):
        cursor = self.db.cursor()
        sqlAddTransaction = f"INSERT INTO TRANSACTIONS (uid, amount) VALUES({id}, {amount});"
        cursor.execute(sqlAddTransaction)
        sqlUpdateBudget = f"UPDATE USERS SET budget = budget + {amount} WHERE  id = {id};"
        cursor.execute(sqlUpdateBudget)
        self.db.commit()

    def getUserFromEmail(self, email):
        cursor = self.db.cursor()
        cursor.execute(f"SELECT id FROM USERS WHERE email = '{email}'")
        return int(cursor.fetchone()[0])

    def getUser(self, id, isJSON = False):
        cursor = self.db.cursor()
        if isJSON:
            sqlGet = f"SELECT (JSON_OBJECT('id', id, 'name', name, 'budget', budget, 'email', email)) FROM users WHERE id = {id}"
        else:
            sqlGet = f"SELECT * FROM USERS WHERE id = {id};"
        cursor.execute(sqlGet)
        return cursor.fetchone()

    def getTransactions(self, id, isJSON = False):
        cursor = self.db.cursor()
        if isJSON:
            sqlGet = f"SELECT JSON_ARRAYAGG(JSON_OBJECT('user_id', uid, 'transaction_id', tid, 'amount', amount, 'time', dateAndTime)) FROM TRANSACTIONS WHERE uid = {id}"
        else:
            sqlGet = f"SELECT * FROM TRANSACTIONS WHERE uid = {id};"
        cursor.execute(sqlGet)
        return cursor.fetchall()

    def deleteUser (self, id):
        cursor = self.db.cursor()
        sqlDelete = f"DELETE FROM USERS WHERE id = {id};"
        cursor.execute(sqlDelete)
        self.db.commit()
        
if __name__ == "__main__":
    db = Database()