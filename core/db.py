import datetime
import logging


class catdoorDB:
    # def openConnection(self):
        # connection = MongoClient('catdoor', 27017)
        # db = connection.catdoor
        # return db

    def getDoorLockState(self):
        f = open("/opt/catdoor/runtime/doorlock.state")
        state = f.read()
        f.close()
        if state == "unlocked":
            return True
        else:
            return False
        # return True
        # scon = lite.connect("../db/catdoor.db")

        # with con:
        #     cur = con.cursor()
        #     cur.execute("select value from settings where key = 'doorstate'")

        #     data = cur.fetchone()
            
        #     if data[0] == "unlocked":
        #         return True
        #     else:
        #         return False

    def writeLog(self, action, details='no details'):
        # con = lite.connect("../db/catdoor.db")

        # with con:
        #     cur = con.cursor()
        #     timeNow = datetime.datetime.now()
        #     cur.execute("insert into logs values(?, ?, ?)", (action, details, timeNow))

        logging.basicConfig(filename='/opt/catdoor/runtime/run.log', level=logging.DEBUG, format='%(asctime)s %(message)s')
        logging.info("Logentry, action: {}, details: {}".format(action, details))
