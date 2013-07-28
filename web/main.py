from bottle import Bottle, run, static_file, request
import json
import datetime
import os
import sqlite3 as lite

app = Bottle()

@app.get('/')
def hello():
    return static_file('index.html', 'static')

@app.get('/door')
def GetDoor():
    con = lite.connect("../runtime/catdoor.db")

    with con:
        cur = con.cursor()
        cur.execute("select value from settings where key = 'doorstate'")

        data = cur.fetchone()
    ret = {"door_state": data[0]}
    return ret


@app.put('/door')
def PutDoor():
    con = lite.connect("../runtime/catdoor.db")

    with con:
        cur = con.cursor()
        cur.execute("update settings set value=? where key =?", (request.forms.door_state, "doorstate"))
        con.commit()
    return 0

@app.get('/log')
def GetLog():
    con = lite.connect("../runtime/catdoor.db")

    with con:
        cur = con.cursor()
        cur.execute("select * from logs order by time desc limit 20")

        rows = cur.fetchall()

        # column_names = [d[0] for d in cur.description]
        #
        # for row in cur:
        #     info = dict(zip(column_names, row))
        #     reply = json.dumps(info)


def unix_time(dt):
    epoch = datetime.datetime.utcfromtimestamp(0)
    delta = dt - epoch
    return delta.total_seconds()


def unix_time_millis(dt):
    return unix_time(dt) * 1000.0


run(app, host='0.0.0.0', port=8080, debug=True)
