from bottle import Bottle, run, static_file, request
import json
import datetime
import os

app = Bottle()


@app.get('/')
def hello():
    return static_file('index.html', 'static')

@app.get('/door')
def GetDoor():
    f = open("/opt/catdoor/runtime/doorlock.state")
    state = f.read()
    f.close()

    ret = {"door_state": state}
    return ret


@app.put('/door')
def PutDoor():
    if request.forms.door_state == "locked":
        os.system("python2 /opt/catdoor/tools/lockdoor.py")
    else:
        os.system("python2 /opt/catdoor/tools/unlockdoor.py")

    return 0


def unix_time(dt):
    epoch = datetime.datetime.utcfromtimestamp(0)
    delta = dt - epoch
    return delta.total_seconds()


def unix_time_millis(dt):
    return unix_time(dt) * 1000.0


run(app, host='0.0.0.0', port=8080, debug=True)
