from bottle import Bottle, run, static_file, request, response
import json
import datetime
import os
import sqlite3 as lite
import collections   
import pprint


app = Bottle()

@app.get('/')
def hello():
    return static_file('index.html', 'static')

@app.get('/favicon.ico')
def favicon():
    return static_file('favicon.ico', 'static')

@app.get('/apple-touch-icon-144x144.png')
def appletouchicon144x144():
    return static_file('apple-touch-icon-144x144.png', 'static')

@app.get('/apple-touch-icon-114x114.png')
def appletouchicon114x114():
    return static_file('apple-touch-icon-114x114.png', 'static')

@app.get('/apple-touch-icon-72x72.png')
def appletouchicon72x72():
    return static_file('apple-touch-icon-72x72.png', 'static')

@app.get('/apple-touch-icon.png')
def appletouchicon():
    return static_file('apple-touch-icon.png', 'static')

@app.get('/lastcampic.jpg')
def lastcampic():
    return static_file('lastcampic.jpg', 'static')

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

        objects_list = []
        for row in rows:
            # pprint.pprint(locals())
            d = collections.OrderedDict()
            d['time'] = row[0]
            d['name'] = row[1]
            d['description'] = row[2]
            objects_list.append(d)
 
        response.content_type = 'application/json'
        j = json.dumps(objects_list)
        return j

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


# run(app, host='0.0.0.0', port=8080, debug=True)
run(app, host='0.0.0.0', port=8080, server='tornado')

