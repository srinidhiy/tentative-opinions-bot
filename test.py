import mysql.connector
mydb = mysql.connector.connect(host="localhost", user="root", passwd="root", database="tentative_opinions")
mycursor = mydb.cursor()
print("EMAIL TABLE*****")
query = ("SELECT * FROM Email")
mycursor.execute(query)
for emailid, email in mycursor:
    print(emailid, email)

print("COURTHOUSE TABLE*****")
query2 = ("SELECT * FROM Courthouse")
mycursor.execute(query2)
for courthouseid, court in mycursor:
    print(courthouseid, court)

print("BRIDGE TABLE*****")
query3 = ("SELECT * FROM Email_courthouse")
mycursor.execute(query3)
for emailid, courthouseid in mycursor:
    print(emailid, courthouseid)

query4 = ("SELECT email_address FROM Email WHERE email_id=1")
mycursor.execute(query4)
for res in mycursor:
    print(res)
