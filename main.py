from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets, QtGui, QtCore
from docxtpl import DocxTemplate
import sqlite3
from join import *
from main_window import *
import sys
from anketa import *
import os


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
            """SELECT Facultet FROM Decanat WHERE name = "{}" and password = "{}" """.format(Login,
                                                                                             Password)).fetchall()[0][0]
        con.commit()
        con.close()
        if not ex:
            self.ui.label_error.setText("Неверный логин или пароль")
            self.ui.label_error.show()
            return
        else:

            self.win = Main("DATABASE.db", ex)
            self.close()
            self.win.show()


class Anketa(QMainWindow, Ui_Anketa):
    def __init__(self, path, user):
        self.user = user
        self.path = path
        super().__init__()
        self.setupUi(self)
        self.con = sqlite3.connect(self.path)
        self.curs = self.con.cursor()
        self.btn_photo.clicked.connect(self.shw_photo)

        self.btn_go_to_menu.clicked.connect(self.go_to_menu)

        self.btn_save.clicked.connect(self.save_1)
        self.btn_save_2.clicked.connect(self.save_2)
        self.btn_save_3.clicked.connect(self.save_3)

        self.paper = self.curs.execute(
            f"""SELECT serial_number, number, gave, code, date FROM Paper WHERE id = {self.user}""").fetchone()

        self.id = self.curs.execute(
            f"""SELECT FIO FROM Students WHERE id = {self.user}""").fetchone()[0]

        self.fio = self.curs.execute(
            f"""SELECT FIO FROM UserForm WHERE id = {self.id}""").fetchone()[0]

        self.sex = self.curs.execute(
            f"""SELECT sex FROM UserForm WHERE id = {self.id}""").fetchone()[0]

        self.birthday = self.curs.execute(
            f"""SELECT birthday FROM Anket WHERE id = {self.id}""").fetchone()[0]

        self.year_join = int(self.curs.execute(
            f"""SELECT year FROM Students WHERE id = {self.user}""").fetchone()[0])

        self.surname = self.fio[0]
        self.name = self.fio[1]
        self.otch = self.fio[2]
        self.data = \
            self.curs.execute(
                f"""Select study_ticket_number, facultet, Groups from Students where id ={self.user}  """).fetchall()[
                0]
        self.tk_number = self.data[0]
        self.facultet = self.data[1]
        self.group = self.data[2]
        self.label_fio.setText(self.fio)
        self.label_sex.setText(self.sex)
        self.label_birthday.setText(str(self.birthday))

        self.edit_serial.setText(str(self.paper[0]))
        self.edit_number.setText(str(self.paper[1]))
        self.edit_gave.setText(str(self.paper[2]))
        self.edit_code.setText(str(self.paper[3]))
        self.edit_date.setText(str(self.paper[4]))
        #self.study_ticket()

    def study_ticket(self):
        self.doc = DocxTemplate(os.path.abspath("Формат студенческого билета (1).docx"))
        context = {'study_number': "{}".format(self.tk_number), 'surname': "{}".format(self.surname),
                   'name': "{}".format(self.name),
                   'otch': "{}".format(self.otch), 'facultet': "{}".format(self.facultet), 'group': "{}".format(self.group),
                   'year1': "{}".format(self.year_join), 'year2': "{}".format(self.year_join + 1),
                   'year3': "{}".format(self.year_join + 2),
                   'year4': "{}".format(self.year_join + 3), 'year5': "{}".format(self.year_join + 4),
                   'year6': "{}".format(self.year_join + 5),
                   'level1': "{}".format(1), 'level2': "{}".format(2), 'level3': "{}".format(3),
                   'level4': "{}".format(4),
                   'level5': "{}".format(5), 'level6': "{}".format(6)}
        self.doc.render(context)
        self.doc.save("Билет.docx")
        os.startfile(os.path.abspath("Билет.docx"), "print")

    def shw_photo(self):
        dt = self.curs.execute(f"""Select photo_path from UserForm where id = {self.id}""").fetchall()[0][0]
        self.ex = Example(dt)
        self.ex.show()



    def save_1(self):
        pass

    def save_2(self):
        pass

    def save_3(self):
        pass

    def go_to_menu(self):
        self.win = Main("DATABASE.db")
        self.close()
        self.win.show()

class Example(QWidget):

    def __init__(self, path):
        self.path = path
        super().__init__()

        self.initUI()

    def initUI(self):
        hbox = QHBoxLayout(self)
        pixmap = QtGui.QPixmap(self.path)

        lbl = QLabel(self)
        lbl.setPixmap(pixmap)

        hbox.addWidget(lbl)
        self.setLayout(hbox)

        self.move(300, 200)
        self.setWindowTitle('Photo')
        self.show()

class Main(QMainWindow, Ui_MainWindow):
    def __init__(self, path, user):
        self.path = path
        self.user = user
        super(Main, self).__init__()
        self.setupUi(self)
        self.con = sqlite3.connect(self.path)
        self.curs = self.con.cursor()
        if self.user == 1:
            self.comboBox.removeItem(3)
            self.comboBox.removeItem(3)
        elif self.user == 2:
            self.comboBox.removeItem(0)
            self.comboBox.removeItem(0)
            self.comboBox.removeItem(0)
        self.update_data()
        self.comboBox.currentTextChanged.connect(self.update_data)
        self.tableWidget.cellClicked.connect(self.student)

    def update_data(self):
        self.brch = self.curs.execute(
            """Select id From Branches WHERE name = "{}" """.format(self.comboBox.currentText())).fetchall()[0][0]
        # print(self.brch)
        self.dt = self.curs.execute("""Select id, FIO from Students Where Branch = {} """.format(self.brch)).fetchall()
        # print(self.dt)
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
        # print(data)
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

    def student(self):
        try:
            self.win = Anketa("DATABASE.db", int(self.tableWidget.item(self.tableWidget.currentRow(), 0).text()))
            self.close()
            self.win.show()
        except Exception as error:
            print(error)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = Join()
    mainWindow.show()
    sys.exit(app.exec())
