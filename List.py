from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox, QDialog
from PyQt5 import QtCore
from PyQt5.QtGui import QStandardItemModel, QStandardItem
import sys
from PyQt5.uic import loadUiType
# import interface.Dataset as ds
import Database as DS

# conn = ds.connect_database()
# Con = DS.connect_database()


class AddContact(QtWidgets.QDialog):
    def __init__(self, model):
        super(AddContact, self).__init__()
        self.w = uic.loadUi('add.ui', self)
        print('add.ui')
        self.model = model
        self.w.show()
        self.w.buttonBox.accepted.connect(self.addContact)

    def addContact(self):
        print('add')
        firstname = self.w.lineEditFirstName.text()
        lastname = self.w.lineEditLastName.text()
        email = self.w.lineEditEmail.text()

        row = (QStandardItem(firstname), QStandardItem(lastname), QStandardItem(email))
        self.model.appendRow(row)


class Example(QtWidgets.QMainWindow):
    def __init__(self):
        super(Example, self).__init__()
        uic.loadUi('UI/List_window.ui', self)

        self.model1 = QStandardItemModel()
        self.model1.setHorizontalHeaderLabels(['Id', 'Serial Number', 'Length', 'Width', 'Height', 'Quantity'])
        self.tableView2.setModel(self.model1)
        self.tableView2.horizontalHeader().setSectionResizeMode(1)

        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['Id', 'Serial Number', 'Length', 'Width', 'Height', 'Quantity'])
        self.tableView.setModel(self.model)
        self.tableView.horizontalHeader().setSectionResizeMode(1)

        result = DS.select_all_crate(Con)
        for row in result:
            id = '{}'.format(row['Id'])
            TableRow = (
                QStandardItem('{}'.format(row['Id'])), QStandardItem(row['SerialNumber']), QStandardItem(row['Length']),
                QStandardItem(row['Width']), QStandardItem(row['Height']), QStandardItem('1'))
            self.model1.appendRow(TableRow)

        # BoxResult = ds.select_all_box(conn)
        BoxResult = DS.select_data(Con)
        for row in BoxResult:
            id = '{}'.format(row['Id'])
            TableRow = (
                QStandardItem('{}'.format(row['Id'])), QStandardItem(row['SerialNumber']), QStandardItem(row['Length']),
                QStandardItem(row['Width']), QStandardItem(row['Height']), QStandardItem('1'))
            self.model.appendRow(TableRow)
        # self.actionNew.triggered.connect(self.addContact)

    def addContact(self):
        print('add item')
        add = AddContact(self.model)


def start():
    app = QtWidgets.QApplication([])
    win = Example()
    win.setFixedSize(1280, 720)
    win.show()
    sys.exit(app.exec())
    # Con.close()


# if __name__ == "__main__":
#     start()
