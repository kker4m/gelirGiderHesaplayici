from requiredLibraries import *

class Database():
    def __init__(self):
        self.conn = sqlite3.connect('logs.db')
        self.c = self.conn.cursor()
        self.c.execute("CREATE TABLE IF NOT EXISTS main (id INTEGER PRIMARY KEY, date TEXT, type INTEGER, amount REAL)")
        self.conn.commit()
        #self.conn.close()

class Main():
    def __init__(self):
        self.db = Database()



conn = sqlite3.connect('test.db')
print("Database opened successfully")
conn.close()
