from requiredLibraries import *
from mainWindow import  Ui_Dialog
class Database():
    def __init__(self):
        self.conn = sqlite3.connect('logs.db')
        self.c = self.conn.cursor()
        self.c.execute("CREATE TABLE IF NOT EXISTS main (id INTEGER PRIMARY KEY, date TEXT, type INTEGER, amount REAL)")
        self.conn.commit()
    def insert(self, date, type, amount):
        self.c.execute("INSERT INTO main (date, type, amount) VALUES (?, ?, ?)", (date, type, amount))
        self.conn.commit()
    def clear(self):
        self.c.execute("DELETE FROM main;")
        self.conn.commit()
        print("Veritabanı temizlendi.")
class dbWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Database Window")
        self.resize(450, 250)
        self.view = QTableWidget()
        self.view.setColumnCount(4)
        self.view.setHorizontalHeaderLabels(["ID", "Date", "Type", "Amount"])
        self.view.setEditTriggers(QTableWidget.NoEditTriggers)
        self.view.setSelectionBehavior(QTableWidget.SelectRows)
        self.view.setSelectionMode(QTableWidget.SingleSelection)
        self.view.setShowGrid(False)
        self.view.verticalHeader().setVisible(False)
        self.view.horizontalHeader().setStretchLastSection(True)
        self.view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.setCentralWidget(self.view)
        self.db = Database()
        self.db.c.execute("SELECT * FROM main")
        self.data = self.db.c.fetchall()
        self.view.setRowCount(len(self.data))
        for i in range(len(self.data)):
            for j in range(4):
                self.view.setItem(i, j, QTableWidgetItem(str(self.data[i][j])))
        self.show()
class App(QtWidgets.QMainWindow):
    def __init__(self):
        super(App, self).__init__()
        self.db = Database()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle('codedby:github/linuxkerem')
        self.ui.dateLabel.setText(str(datetime.datetime.now()).split()[0])
        self.ui.gelirButton.clicked.connect(self.gelir)
        self.ui.giderButton.clicked.connect(self.gider)
        self.ui.clearButton.clicked.connect(self.db.clear)
        self.ui.showDBButton.clicked.connect(self.showDB)
    def gelir(self):
        self.db.insert(self.ui.dateLabel.text(), 1, self.ui.gelirBox.text())
        self.ui.gelirBox.clear()
        self.hesapla()
    def gider(self):
        self.db.insert(self.ui.dateLabel.text(), 0, self.ui.giderBox.text())
        self.ui.giderBox.clear()
        self.hesapla()
    def hesapla(self):
        gider = 0
        gelir = 0
        giderler = self.db.c.execute("SELECT amount FROM main WHERE type=0 AND date LIKE '%{}%'".format(self.ui.dateLabel.text().split('-')[1]))
        for i in giderler:
            gider += i[0]
        gelirler = self.db.c.execute("SELECT amount FROM main WHERE type=1 AND date LIKE '%{}%'".format(self.ui.dateLabel.text().split('-')[1]))
        for i in gelirler:
            gelir += i[0]
        self.ui.resultLabel.setText("Bu ay ki geliriniz: " + str(int(gelir-gider)))

    def showDB(self):
        self.dbWindow = dbWindow()
        self.dbWindow.show()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())