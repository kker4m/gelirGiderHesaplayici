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

class App(QtWidgets.QMainWindow):
    def __init__(self):
        super(App, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle('codedby:fiverr/linuxkerem')
        self.ui.addAccount.clicked.connect(self.addAccount)
        self.ui.addMultipleAccount.clicked.connect(self.addMultipleAccount)
        self.ui.addAccountGmailTab.clicked.connect(self.addGmailAccount)
        self.ui.addProxysProxyTab.clicked.connect(self.addProxys)
        self.ui.addGmailsButton.clicked.connect(self.addGmails)
        self.ui.addAccountProxyTab.clicked.connect(self.addProxyAccount)
        self.ui.startButton.clicked.connect(self.start)

conn = sqlite3.connect('test.db')
print("Database opened successfully")
conn.close()
