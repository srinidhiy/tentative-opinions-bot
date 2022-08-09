from doctest import debug_script
from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

mydb = mysql.connector.connect(host="localhost", user="root", passwd="root", database="tentative_opinions")



@app.route('/', methods = ["POST", "GET"])
def home():
    if request.method == "POST":
        # get the emails they provided and turn into a list
        emails = request.form["emails"]
        email_list = emails.split(" ")
        courthouses = request.form.getlist("courthouses")
        # set up query
        mycursor = mydb.cursor()
        email_query = ("SELECT * FROM Email WHERE email_address=%s")
        email_insert = "INSERT INTO Email (email_address) VALUES (%s)"
        courthouse_query = ("SELECT * FROM Courthouse WHERE courthouse_name=%s")
        courthouse_insert = "INSERT INTO Courthouse (courthouse_name) VALUES (%s)"
        bridge_query = ("SELECT * FROM Email_courthouse WHERE email_id=%s AND courthouse_id=%s")
        bridge_insert = "INSERT INTO Email_courthouse (email_id, courthouse_id) VALUES (%s, %s)"
        bridge_delete = ("DELETE FROM Email_courthouse WHERE email_id=%s AND courthouse_id=%s")
        # for every email, check if it's in the database
        for email in email_list:
            em = (email, )
            mycursor.execute(email_query, em)
            myresult = mycursor.fetchone()
            # if it's not in the database, add it
            if not myresult:
                mycursor.execute(email_insert, em)
                mydb.commit()
        # for every courthouse, check if it's in the database
        for courthouse in courthouses:
            c = (courthouse, )
            mycursor.execute(courthouse_query, c)
            myresult = mycursor.fetchone()
            # if not in database, add it
            if not myresult:
                mycursor.execute(courthouse_insert, c)
                mydb.commit()

        if request.form['submit'] == 'Submit to table':
            # for every email-courthouse pair, add to bridge table
            for email in email_list:
                # get the email_id
                em = (email, )
                mycursor.execute(email_query, em)
                myresult = mycursor.fetchone()
                email_id = myresult[0]
                for courthouse in courthouses:
                    # get courhouse_id
                    c = (courthouse, )
                    mycursor.execute(courthouse_query, c)
                    myresult = mycursor.fetchone()
                    courthouse_id = myresult[0]
                    # check if pair is in bridge table
                    mycursor.execute(bridge_query, (email_id, courthouse_id))
                    myresult = mycursor.fetchone()
                    # if not in table, add it
                    if not myresult:
                        mycursor.execute(bridge_insert, (email_id, courthouse_id))
                        mydb.commit()
            return redirect(url_for("confirm"))
        elif request.form['submit'] == 'Delete from table':
            # for every email-courthouse pair, delete from bridge table
            for email in email_list:
                # get the email_id
                em = (email, )
                mycursor.execute(email_query, em)
                myresult = mycursor.fetchone()
                email_id = myresult[0]
                for courthouse in courthouses:
                    # get courhouse_id
                    c = (courthouse, )
                    mycursor.execute(courthouse_query, c)
                    myresult = mycursor.fetchone()
                    courthouse_id = myresult[0]
                    # check if pair is in bridge table
                    mycursor.execute(bridge_query, (email_id, courthouse_id))
                    myresult = mycursor.fetchone()
                    # if not in table, add it
                    if myresult:
                        mycursor.execute(bridge_delete, (email_id, courthouse_id))
                        mydb.commit()
            return redirect(url_for("confirm"))
                
    else:
        return render_template("index.html")

@app.route("/confirm")
def confirm():
    return "<h1>Thank you for submitting!</h1>"


if __name__ == "__main__":
    app.run(debug=True)