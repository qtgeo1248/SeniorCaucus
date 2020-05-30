import os, sqlite3, calendar
from datetime import datetime
from flask import Flask, render_template, request, session, redirect, url_for, flash

DB_FILE = "dates.db"
noschool = [3190, 3191, 3200, 3201, 5210, 5211, 5250, 5251, 6040, 6041,
            4090, 4091, 4100, 4101, 4130, 4131, 4140, 4141, 4150, 4151, 4160, 4161, 4170, 4171]

def setup():
    command = "CREATE TABLE IF NOT EXISTS dates (id INT, date INT);"
    exec(command)

def exec(cmd):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    output = c.execute(cmd)
    db.commit()
    return output

def authenticate(date):
    command = "SELECT date FROM dates WHERE '" + date + "' = date;"
    out = exec(command)
    thingy = out.fetchone()
    if thingy is None:
        return True
    return False

def genDates():
    list = []
    month = 3
    day = 15
    for i in range(13):
        for j in range(5):
            day += 1
            if month % 2 == 1:
                if day > 31:
                    day -= 31
                    month += 1
            if month % 2 == 0:
                if day > 30:
                    day -= 30
                    month += 1
            for k in range(2):
                cur = ""
                cur += str(month)
                if (day // 10 == 0):
                    cur += "0"
                cur += str(day)
                cur += str(k)
                if int(cur) not in noschool:
                    list.append(int(cur))
        day += 2
    return list


def remDates(list):
    command = "SELECT date FROM dates;"
    out = exec(command)
    thingy = out.fetchall()
    allChosen = convertTupToList(thingy)
    for item in allChosen:
        if (int(item) in list):
            list.remove(int(item))
    return list

def convertTupToList(datesTuple):
    list = []
    for item in datesTuple:
        if str(item) not in list:
            list.append(str(item)[1:-2])
    return list

def check(osis):
    command = "SELECT date FROM dates WHERE '" + str(osis) + "' = id;"
    out = exec(command)
    thingy = out.fetchall()
    allDates = convertTupToList(thingy)
    for i in range(len(allDates)):
        allDates[i] = int(allDates[i])
    return allDates

def convertDbToStr(dbdate):
    days = ["Sun", "Mon", "Tue", "Wed", "Thur", "Fri", "Sat"]
    month = dbdate // 1000
    day = (dbdate // 10) % 100
    time = dbdate % 10
    eyes = ""
    eyes += " " + str(month) + "/" + str(day) + "/2020 "
    eyes += days[calendar.weekday(2020, month, day)]
    if time == 0:
        eyes += " 4:00 PM"
    else:
        eyes += " 4:30 PM"
    return eyes

def wrongEmail(email):
    cur = ""
    num = 0
    for i in email:
        if i.isdigit():
            cur += i
    try:
        num = int(cur)
    except ValueError:
        return True
    try:
        num = int(email[-2:])
    except ValueError:
        return True
    if num // 10 >= 1:
        return True
    return False

def wrongOSIS(osis):
    try:
        num = int(osis)
    except ValueError:
        return True
    if (num // (10 ** 9) >= 1) or (num % (10 ** 9) < 10 ** 8):
        return True
    return False
