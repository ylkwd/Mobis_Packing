from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QStandardItemModel, QStandardItem
import sys
import Dataset as ds
from PyQt5.QtWidgets import (QDialog)
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
import main as Pack
# import py3dbp as py3d
from py3dbp import visualize
from py3dbp import test as test

conn = ds.connect_database()
container = []
boxes = []


class AddBox(QtWidgets.QDialog):
    def __init__(self, model):
        super(AddBox, self).__init__()
        self.w = uic.loadUi('UI/add.ui', self)
        print('add.ui')
        self.model = model
        self.w.show()
        self.w.buttonBox.accepted.connect(self.addBox)

    def addBox(self):
        SerialNumber = 0
        Quantity = 0
        print('add')
        SerialNumber = self.w.LineSerialNum.text()
        Quantity = self.w.LineQuantity.text()
        # email = self.w.lineEditEmail.text()
        i = 0
        # print(SerialNumber,Quantity)
        # exit(0)
        # result = dataset.select_data_serial(conn,SerialNumber)
        result = ds.select_Box_serial(conn, SerialNumber)
        # print(result)
        # exit(0)
        for row in result:
            id = '{}'.format(row['Id'])
            TableRow = (
                QStandardItem('{}'.format(row['Id'])), QStandardItem(row['SerialNumber']), QStandardItem(row['Length']),
                QStandardItem(row['Width']), QStandardItem(row['Height']), QStandardItem(Quantity))

            self.model.appendRow(TableRow)
        # print(Quantity)
        for i in range(0, int(Quantity)):
            boxes.append([row['Id']])
            print(i)
            i += 1


class AddCrate(QtWidgets.QDialog):
    def __init__(self, model):
        super(AddCrate, self).__init__()
        self.w = uic.loadUi('UI/addCrate.ui', self)
        print('add.ui')
        self.model = model
        self.w.show()
        self.w.buttonBox.accepted.connect(self.addBox)

    def addBox(self):
        SerialNumber = 0
        Quantity = 1
        print('add')
        SerialNumber = self.w.LineSerialNum.text()
        # Quantity = self.w.LineQuantity.text()
        # email = self.w.lineEditEmail.text()

        # print(SerialNumber,Quantity)
        # exit(0)
        # result = dataset.select_data_serial(conn,SerialNumber)
        result = ds.select_Crate_serial(conn, SerialNumber)
        # print(result)
        # exit(0)
        for row in result:
            id = '{}'.format(row['Id'])
            TableRow = (
                QStandardItem('{}'.format(row['Id'])), QStandardItem(row['SerialNumber']), QStandardItem(row['Length']),
                QStandardItem(row['Width']), QStandardItem(row['Height']), QStandardItem('1'))
            self.model.appendRow(TableRow)
        container.append(row['Id'])


def RunPacking():
    print("Run packing")
    # add = RunPacking()
    dataset = {}
    print(container, boxes)
    print(len(container), len(boxes))
    if len(container) == 0 or len(boxes) <= 5:
        alert = CrateAlert1()

    else:
        dataset = ds.Packing_Prepare(conn, container, boxes)
        print(dataset)
        Pack.start()

    # Pack.start(dataset)


def RunMulPacking():
    print("Run Mul packing")
    # add = RunPacking()
    dataset = {}
    # print(container, boxes)
    print(len(container), len(boxes))
    if len(container) == 0 or len(boxes) <= 5:
        alert = CrateAlert1()

    else:
        dataset = ds.Packing_Prepare(conn, container, boxes)
        # print(dataset)
        # Pack.start()
        test.Mul_packing()
    # Pack.start(dataset)


def BoxesList():
    print("Run Boxes List")


class CrateAlert1(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Crate Alert'

        self.left = 10
        self.top = 10
        self.width = 320
        self.height = 200
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        buttonReply = QMessageBox.question(self, 'Alert ', "Please add more boxes",
                                           QMessageBox.Yes | QMessageBox.Cancel,
                                           QMessageBox.Cancel)
        print(int(buttonReply))
        if buttonReply == QMessageBox.Yes:
            print('Yes clicked.')
        if buttonReply == QMessageBox.No:
            print('No clicked.')
        if buttonReply == QMessageBox.Cancel:
            print('Cancel')

        self.show()


class CrateAlert(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Crate Alert'

        self.left = 10
        self.top = 10
        self.width = 320
        self.height = 200
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        buttonReply = QMessageBox.question(self, 'Alert ', "Only one carte per time",
                                           QMessageBox.YesToAll | QMessageBox.Cancel,
                                           QMessageBox.Cancel)
        print(int(buttonReply))
        if buttonReply == QMessageBox.Yes:
            print('Yes clicked.')
        if buttonReply == QMessageBox.No:
            print('No clicked.')
        if buttonReply == QMessageBox.Cancel:
            print('Cancel')

        self.show()


class Example(QtWidgets.QMainWindow):
    def __init__(self):
        super(Example, self).__init__()
        uic.loadUi('UI/window.ui', self)
        # result = Database.select_data(conn)
        # for row in result:
        #     print("{SerialNumber}, {Length}, {Width}, {Height}, {Weight}".format(**row))
        self.model1 = QStandardItemModel()
        self.model1.setHorizontalHeaderLabels(['Id', 'Serial Number', 'Length', 'Width', 'Height', 'Quantity'])
        self.tableView2.setModel(self.model1)
        self.tableView2.horizontalHeader().setSectionResizeMode(1)

        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['Id', 'Serial Number', 'Length', 'Width', 'Height', 'Quantity'])
        self.tableView.setModel(self.model)
        self.tableView.horizontalHeader().setSectionResizeMode(1)

        # row = (QStandardItem('Alice'), QStandardItem('Alison'), QStandardItem('alice@alison.com'))
        # self.model.appendRow(row)

        self.actionNewCrate.triggered.connect(self.addCrate)
        self.actionNewBox.triggered.connect(self.addBox)
        self.actionExit.triggered.connect(self.Close)
        self.actionRun.triggered.connect(RunPacking)
        self.actionRunMul.triggered.connect(RunMulPacking)
        self.actionShow.triggered.connect(BoxesList)

    def Close(self):
        self.close()

    def addBox(self):
        print('add box')
        add = AddBox(self.model)

    def addCrate(self):
        print('Add crate')
        if self.model1.rowCount() < 1:
            print(self.model1.rowCount())
            add = AddCrate(self.model1)
        else:
            print("have container already")
            ex = CrateAlert()


def start():
    app = QtWidgets.QApplication([])
    win = Example()
    win.setFixedSize(1280, 720)
    win.show()
    sys.exit(app.exec())
    conn.close()


if __name__ == "__main__":
    start()
    conn.close()
