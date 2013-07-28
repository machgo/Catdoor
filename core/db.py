import datetime
import logging
import sqlite3 as lite


class catdoorDB:
    def getDoorLockState(self):
        con = lite.connect("/opt/catdoor/runtime/catdoor.db")

        with con:
            cur = con.cursor()
            cur.execute("select value from settings where key = 'doorstate'")

            data = cur.fetchone()
            
            if data[0] == "unlocked":
                return True
            else:
                return False

    def writeLog(self, action, details='no details'):
        con = lite.connect("/opt/catdoor/runtime/catdoor.db")

        with con:
            cur = con.cursor()
            timeNow = datetime.datetime.now()
            cur.execute("insert into logs values(?, ?, ?)", (timeNow, action, details))
