from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets, QtGui, QtCore
import sqlite3
from join import *
from main_window import *
import sys
import pkg_resources.py2_warn


class Join(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_Join()
        self.ui.setupUi(self)

        self.ui.label_error.hide()

        self.ui.btn_join.clicked.connect(self.go_join)

    def go_join(self):
        Login = None
        Password = None

        if len(self.ui.edit_login.text()) > 0:
            Login = self.ui.edit_login.text()
        else:
            self.ui.label_error.setText("Введите логин и пароль")
            self.ui.label_error.show()
            return

        if len(self.ui.edit_password.text()) > 0:
            Password = self.ui.edit_password.text()
        else:
            self.ui.label_error.setText("Введите логин и пароль")
            self.ui.label_error.show()
            return

        con = sqlite3.connect("DATABASE.db")
        curs = con.cursor()
        ex = curs.execute(
            """SELECT * FROM Decanat WHERE name = "{}" and password = "{}" """.format(Login, Password)).fetchall()
        con.commit()
        con.close()
        if not ex:
            self.ui.label_error.setText("Неверный логин или пароль")
            self.ui.label_error.show()
            return
        else:

                self.win = Main("DATABASE.db")
                self.close()
                self.win.show()


class Main(QMainWindow, UI_Main):
    def __init__(self, path):
        self.path = path
        super(Main, self).__init__()
        self.setupUi(self)
        self.con = sqlite3.connect(self.path)
        self.curs = self.con.cursor()
        self.update_data()
        self.comboBox.currentTextChanged.connect(self.update_data)

    def update_data(self):
        self.brch = self.curs.execute(
                """Select id From Branches WHERE name = "{}" """.format(self.comboBox.currentText())).fetchall()[0][0]
        #print(self.brch)
        self.dt = self.curs.execute("""Select id, FIO from Students Where Branch = {} """.format(self.brch)).fetchall()
        print(self.dt)
        if self.dt:
            for j in self.dt:
                data = []

                k = self.curs.execute("""Select FIO from UserForm Where id = {} """.format(j[1])).fetchall()[0][0]
                print(j[0], k)

                data.append((j[0], k))
                print(data)
                self.update_table(data)
        else:
            self.update_table(self.dt)

    def update_table(self, data):
        print(data)
        self.tableWidget.setRowCount(0)
        n = len(data)
        try:
            self.tableWidget.setRowCount(n)
            for i in range(n):
                self.tableWidget.setItem(i, 0, QTableWidgetItem())
                self.tableWidget.setItem(i, 1, QTableWidgetItem())

                self.tableWidget.item(i, 0).setText(str(data[i][0]))
                self.tableWidget.item(i, 1).setText(str(data[i][1]))
        except Exception as er:
            print(er)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = Join()
    mainWindow.show()
    sys.exit(app.exec())
