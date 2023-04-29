from requiredLibraries import *
from mainWindow import  Ui_Dialog
class Database():
    def __init__(self):
        self.conn = sqlite3.connect('logs.db')
        self.c = self.conn.cursor()
        self.c.execute("CREATE TABLE IF NOT EXISTS main (tarih TEXT, miktar INT, aciklama LONGTEXT, kategori varchar(400))")
        self.conn.commit()
    def insert(self, tarih, miktar,description='',kategori="Belirtilmemis"):
        self.c.execute("INSERT INTO main(tarih, miktar, aciklama, kategori ) VALUES (?, ?, ?, ?)", (tarih, miktar,description,kategori))
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
        self.view.setHorizontalHeaderLabels(["Tarih", "Miktar","Aciklama","Kategori"])
        self.view.setEditTriggers(QTableWidget.NoEditTriggers)
        self.view.setSelectionBehavior(QTableWidget.SelectRows)
        self.view.setSelectionMode(QTableWidget.SingleSelection)
        self.view.setShowGrid(False)
        self.view.verticalHeader().setVisible(False)
        self.view.horizontalHeader().setStretchLastSection(True)
        self.view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.setCentralWidget(self.view)
        self.db = Database()
        self.db.c.execute("SELECT * FROM main ORDER BY tarih DESC,kategori;")
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
        self.setFixedWidth(713)
        self.setFixedHeight(277)
        self.setWindowTitle('codedby:github/linuxkerem')
        self.ui.dateLabel.setText(str(datetime.datetime.now()).split()[0])
        self.ui.gelirButton.clicked.connect(self.bakiyeEkle)
        self.ui.clearButton.clicked.connect(self.veritabininiTemizle)
        self.ui.showDBButton.clicked.connect(self.showDB)
        self.hesapla()

    def veritabininiTemizle(self):
        reply = QMessageBox.warning(self, 'Dikkat', 'Tum verilerinizi silmek istediginizden emin misiniz ?',QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.db.clear()
            self.ui.resultLabel.setText("Bu ay ki geliriniz: 0" )
    def bakiyeEkle(self):
        kategori = self.ui.kategoriBox.currentText()
        if kategori == "Belirtilmemis" and len(self.ui.ozelKategori.text()) != 0:
            kategori = self.ui.ozelKategori.text()
        self.db.insert(self.ui.dateLabel.text(),self.ui.gelirBox.text(),self.ui.aciklama.text(),kategori)
        self.ui.gelirBox.clear()
        self.ui.aciklama.clear()
        self.ui.ozelKategori.clear()
        self.ui.kategoriBox.setCurrentIndex(0)
        self.hesapla()
    def hesapla(self):
        tarih = self.ui.dateLabel.text().split('-')
        tarih = tarih[0] + '-' + tarih[1]
        gelir, gider = 0,0
        giderler = self.db.c.execute("SELECT miktar FROM main WHERE miktar < 0 AND tarih LIKE '%{}%'".format(tarih))
        for i in giderler:
            try:
                gider += i[0]
            except: pass
        gelirler = self.db.c.execute("SELECT miktar FROM main WHERE miktar > 0 AND tarih LIKE '%{}%'".format(tarih))
        for i in gelirler:
            try:
                gelir += i[0]
            except: pass
        self.ui.resultLabel.setText("Bu ay ki geliriniz: " + str(int(gelir-gider)))

    def showDB(self):
        self.dbWindow = dbWindow()
        self.dbWindow.show()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())