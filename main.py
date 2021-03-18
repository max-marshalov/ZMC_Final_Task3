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
# import pkg_resources.py2_warn


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
    def __init__(self, path, user, main_user):
        self.user = user
        self.main_user = main_user
        self.path = path
        super().__init__()
        self.setupUi(self)
        self.con = sqlite3.connect(self.path)
        self.curs = self.con.cursor()

        self.btn_go_to_menu.clicked.connect(self.go_to_menu)
        self.btn_photo.clicked.connect(self.shw_photo)

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
        print(self.fio)
        dt = self.fio.split(" ")

        self.surname = dt[0]
        self.name = dt[1]
        self.otch = dt[2]
        self.data = \
            self.curs.execute(
                f"""Select study_ticket_number, facultet, Groups from Students where id = {self.user}""").fetchall()[
                0]
        self.tk_number = self.user
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
        self.btn_study_ticket.clicked.connect(self.study_ticket)

        self.phone_number = self.curs.execute(
            f"""SELECT phone_number FROM UserForm WHERE id = {self.id}""").fetchone()[0]

        self.mail = self.curs.execute(
            f"""SELECT email FROM UserForm WHERE id = {self.id}""").fetchone()[0]

        self.reg_adress = self.curs.execute(
            f"""SELECT reg_address FROM Students WHERE id = {self.user}""").fetchone()[0]

        self.reg_adress = self.curs.execute(
            f"""SELECT address_index, city, street, house, flat FROM Address WHERE id = {self.reg_adress}""").fetchone()

        self.live_adress = self.curs.execute(
            f"""SELECT live_address FROM Students WHERE id = {self.user}""").fetchone()[0]

        self.live_adress = self.curs.execute(
            f"""SELECT address_index, city, street, house, flat FROM Address WHERE id = {self.live_adress}""").fetchone()

        self.edit_adress_1.setText(
            f"{self.reg_adress[0]}, {self.reg_adress[1]}, {self.reg_adress[2]}, {self.reg_adress[3]}, {self.reg_adress[4]}")
        self.edit_adress_2.setText(
            f"{self.live_adress[0]}, {self.live_adress[1]}, {self.live_adress[2]}, {self.live_adress[3]}, {self.live_adress[4]}")
        self.edit_phone_number.setText(str(self.phone_number))
        self.edit_email.setText(str(self.mail))

        self.branch = self.curs.execute(
            f"""SELECT Branch FROM Students WHERE id = {self.user}""").fetchone()[0]

        self.facultet_name = self.curs.execute(
            f"""SELECT name FROM Facultets WHERE id = {self.facultet}""").fetchone()[0]

        self.branch_name = self.curs.execute(
            f"""SELECT name FROM Branches WHERE id = {self.branch}""").fetchone()[0]

        self.join_date = self.curs.execute(
            f"""SELECT join_date FROM Students WHERE id = {self.user}""").fetchone()[0]

        self.leave_date = self.curs.execute(
            f"""SELECT leave_date FROM Students WHERE id = {self.user}""").fetchone()[0]

        self.label_facultet.setText(str(self.facultet_name))
        self.label_branch.setText(str(self.branch_name))

        self.comboBox_group_number.setCurrentIndex(self.group - 1)
        self.label_stud_number.setText(str(self.user))
        self.label_zach_number.setText(str(self.user))
        self.edit_chit_bilet.setText(str(self.user))

        self.label_date_zach.setText(str(self.join_date))
        self.label_date_otch.setText(str(self.leave_date))

    def question(self):
        pass

    def study_ticket(self):
        self.doc = DocxTemplate(os.path.abspath("Формат студенческого билета (1).docx"))
        context = {'study_number': "{}".format(self.tk_number), 'surname': "{}".format(self.surname),
                   'name': "{}".format(self.name),
                   'otch': "{}".format(self.otch), 'facultet': "{}".format(self.facultet),
                   'group': "{}".format(self.group),
                   'year1': "{}".format(self.year_join), 'year2': "{}".format(self.year_join + 1),
                   'year3': "{}".format(self.year_join + 2),
                   'year4': "{}".format(self.year_join + 3), 'year5': "{}".format(self.year_join + 4),
                   'year6': "{}".format(self.year_join + 5),
                   'level1': "{}".format(1), 'level2': "{}".format(2), 'level3': "{}".format(3),
                   'level4': "{}".format(4),
                   'level5': "{}".format(5), 'level6': "{}".format(6)}
        self.doc.render(context)
        self.doc.save("Билет.docx")
        self.printing()

    def printing(self):
        os.startfile(os.path.abspath("Билет.docx"), "print")
    def shw_photo(self):
        dt = self.curs.execute(f"""Select photo_path from UserForm where id = {self.id}""").fetchall()[0][0]
        self.ex = Example(dt)
        self.ex.show()

    def save_1(self):
        self.curs.execute(
            f"""UPDATE Paper set serial_number = '{self.edit_serial.text()}', number = '{self.edit_number.text()}', gave = '{self.edit_gave.text()}', code = '{self.edit_code.text()}', date = '{self.edit_date.text()}' WHERE id = {self.user}"""
        )
        self.con.commit()

    def save_2(self):
        try:
            self.curs.execute(
                f"""UPDATE UserForm set phone_number = '{self.edit_phone_number.text()}', email = '{str(self.edit_email.text())}' WHERE id = {self.id}"""
            )
            self.con.commit()
        except Exception as ex:
            print(ex)

        self.reg_adress = self.curs.execute(
            f"""SELECT reg_address FROM Students WHERE id = {self.user}""").fetchone()[0]

        self.live_adress = self.curs.execute(
            f"""SELECT live_address FROM Students WHERE id = {self.user}""").fetchone()[0]

        try:
            self.curs.execute(
                f"""UPDATE Address set smth WHERE id = {self.reg_adress}"""
            )

            self.curs.execute(
                f"""UPDATE Address set smth WHERE id = {self.live_adress}"""
            )

            self.con.commit()
        except Exception as ex:
            print(ex)

    def save_3(self):
        pass

    def go_to_menu(self):
        self.win = Main("DATABASE.db", self.main_user)
        self.win.show()
        self.close()


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
            self.win = Anketa("DATABASE.db", int(self.tableWidget.item(self.tableWidget.currentRow(), 0).text()), self.user)
            self.close()
            self.win.show()
        except Exception as error:
            print(error)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = Join()
    mainWindow.show()
    sys.exit(app.exec())
