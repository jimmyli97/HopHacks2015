#!/usr/bin/python

import sqlite3 as lite
import sys

con = None
con = lite.connect('test.db')

with con:
    cur = con.cursor()
    cur.execute("CREATE TABLE Cars(Id INT, Name TEXT, Price INT)")
    cur.execute("INSERT INTO Cars VALUES(1, 'Audi', 52234)")
    cur.execute("INSERT INTO Cars VALUES(2, 'Mercedes', 23423)")

