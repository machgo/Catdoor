import sqlite3 as lite
import datetime

conn = lite.connect('../runtime/catdoor.db')

with conn:
    c = conn.cursor()

    c.execute('drop table if exists settings')
    c.execute('drop table if exists logs')

    c.execute('create table settings (key text, value text)')
    c.execute('insert into settings values ("doorstate", "locked")')

    c.execute('create table logs (time timestamp, name text, description text)')
    c.execute('insert into logs values (?, ?, ?)', (datetime.datetime.now(), "Database created", "no errors"))

