import db, os, sqlite3
from flask import Flask, render_template, request, session, redirect, url_for, flash

image = "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/apple/237/revolving-hearts_1f49e.png"

app = Flask(__name__)
app.secret_key = os.urandom(32)

@app.route('/')
def index():
    list = db.genDates()
    list = db.remDates(list)
    return render_template("landing.html", happy = list, error = "", error2 = "")

@app.route("/date")
def addDate():
    some = str(request.args["dat"])
    id = str(request.args["ID"])
    email = str(request.args["email"])
    list = db.genDates()
    list = db.remDates(list)
    if db.wrongEmail(email):
        return render_template("landing.html", error = "You must input a valid, senior, email address", happy = list)
    if db.wrongOSIS(id):
        return render_template("landing.html", error = "Your OSIS must be", happy = list, italics = " your", notitalics = " valid 9-digit number!")
    if (len(some) == 0) or (len(str(request.args["ID"])) == 0) or (len(str(request.args["email"])) == 0):
        return render_template("landing.html", error = "All fields must be filled!", happy = list)
    if db.authenticate(some):
        command = "INSERT INTO dates (id, date) VALUES (" + request.args["ID"] + ", '" + request.args["dat"] + "');"
        db.exec(command)
        return render_template("out.html", selectedDate = str(request.args["dat"]), osis = id)
    else:
        return render_template("landing.html", error = "Unfortunately, your date is already chosen :(", error2 = "Please choose a different date.", happy = list)

@app.route("/redo")
def redo():
    date = str(request.args["input"])
    command = "DELETE FROM dates WHERE date = " + str(date) + ";"
    db.exec(command)
    list = db.genDates()
    list = db.remDates(list)
    return render_template("landing.html", happy = list, error = "", error2 = "")

@app.route("/checking")
def renderDate():
    return render_template("checker.html")

@app.route("/checked")
def checkDate():
    osis = int(request.args["ID"])
    registered = db.check(osis)
    if len(registered) == 0:
        return render_template("checker.html", all = registered, error = "Unfortunately, you", bold = " (OSIS: " + str(osis) + ") ", notbold = "have not signed up for a prom date yet")
    else:
        return render_template("checker.html", all = registered, id = osis)

@app.route("/faq")
def renderFAQ():
    return render_template("faq.html")

if __name__ == "__main__":
    db.setup()
    app.debug = True
    app.run()
