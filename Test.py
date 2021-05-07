from User import *
import time
s1="set my budget to 200$"
s2="add 50$ to my account"
s3="I spent 20$"
testUser = User(1,"Elie","Z","Rizk")
testUser.add(100)
time.sleep(3)
testUser.sub(25)
testUser.sub(50)
print(testUser)
