try:
    self.ticket = QtGui.QTextDocument(tx)
    printer = QPrinter()
    dialog = QPrintDialog(printer)
    if dialog.exec_():
        #return self.ticket.print(printer)
        pass
except Exception as er:
    print(er)