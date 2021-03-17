from docxtpl import DocxTemplate
import sqlite3
import os
import pkg_resources.py2_warn
con = sqlite3.connect("DATABASE.db")
curs = con.cursor()

data = \
    curs.execute("""Select study_ticket_number, FIO, facultet, Groups, year from Students where id = 1 """).fetchall()[
        0]
print(data)
fio = curs.execute("""Select FIO from UserForm where id = {}""".format(data[1])).fetchall()[0][0].split(" ")
surname = fio[0]
name = fio[1]
otch = fio[2]
number = data[0]
fuck = data[2]
group = data[3]
year = int(data[4])

doc = DocxTemplate(os.path.abspath("Формат студенческого билета (1).docx"))
context = {'study_number': "{}".format(number), 'surname': "{}".format(surname), 'name': "{}".format(name),
           'otch': "{}".format(otch), 'facultet': "{}".format(fuck), 'group': "{}".format(group),
           'year1': "{}".format(year), 'year2': "{}".format(year + 1), 'year3': "{}".format(year + 2),
           'year4': "{}".format(year + 3), 'year5': "{}".format(year + 4), 'year6': "{}".format(year + 5),
           'level1': "{}".format(1), 'level2': "{}".format(2), 'level3': "{}".format(3), 'level4': "{}".format(4),
           'level5': "{}".format(5), 'level6': "{}".format(6)}
doc.render(context)
doc.save("Билет.docx")