import sys
import random
import pandas as pd
from PyQt5.QtCore import QCoreApplication
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import QFileDialog, QLabel
# import data
# from interface import interactive
from PySide6.QtGui import QFileOpenEvent, QPixmap
import Database
import Dataset as ds
# from interface import gui
# from PyQt5 import QtWidgets, uic
# from PyQt5.QtWidgets import QMessageBox
# from interface import test
import Add
import List

logo = 'Mobis.png'
conn = Database.connect_database()
# conn = Database.connect_database()


class Menu(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # self.w = gui.Gui()
        # self.table = test.TableView(data)
        label1 = QLabel(self)
        pixmap = QPixmap("Mobis.png")
        label1.setPixmap(pixmap)

        self.pack_button = QtWidgets.QPushButton("Pack!")
        self.config_button = QtWidgets.QPushButton("Config")
        self.list_button = QtWidgets.QPushButton("Packing list")
        self.import_button = QtWidgets.QPushButton("Import File")
        self.interactive_button = QtWidgets.QPushButton("Exit")

        self.layout = QtWidgets.QGridLayout(self)
        self.layout.setGeometry(QtCore.QRect(0, 0, 10, 10))
        self.layout.addWidget(label1, 0, 0, 0, 0)

        self.layout.addWidget(self.pack_button, 2, 0)
        self.layout.addWidget(self.interactive_button, 2, 1)
        self.layout.addWidget(self.list_button, 1, 1)
        self.layout.addWidget(self.config_button, 2, 1)
        self.layout.addWidget(self.import_button, 1, 0)

        self.pack_button.clicked.connect(self.pack)
        self.config_button.clicked.connect(self.config)
        self.list_button.clicked.connect(self.list)
        self.import_button.clicked.connect(self.import_file)
        self.interactive_button.clicked.connect(self.interactive_run)

    @QtCore.Slot()
    def pack(self):
        print("pack")
        Add.start()
        print("Add")
        # if self.w.isVisible():
        conn.close()
        pass
        # else:
        #     self.w.show()

    @QtCore.Slot()
    def list(self):
        # if self.table.isVisible():
        #     pass
        # else:
        #     # self.table(data).show()
        #     print("list")

        result = Database.select_data(conn)
        # for row in result:
        #     print("{SerialNumber}, {Length}, {Width}, {Height}, {Weight}".format(**row))
        List.start()
        conn.close()
        start()

    @QtCore.Slot()
    def config(self):
        print("config")
        container = [1]
        boxes = []
        Multiboxes = []
        fileName = str(QFileDialog.getOpenFileName(self, "open file", '..', "Excel files (*.xlsx)")[0])
        print(fileName)

        # print(fileName.partition(".xlsx"))
        # Database.create_table_cur(conn,"box")
        if fileName != 0:
            df = pd.read_excel(fileName)
            # print(df.columns[0])

            for index, row in df.iterrows():
                Quantity =0
                # print(df.columns)
                # print(type(df.loc[:'Length']))
                list = [row[0]]
                SerialNumber=row['PART NO.']
                Quantity= row['BOX QTY']
                # append_data(list, row['Height'])
                # append_data(list, row['Weight'])
                result = ds.select_Box_serial(conn, SerialNumber)
                for row1 in result:
                    id = '{}'.format(row1['Id'])
                Multiboxes.append([row1['Id'], row['BOX QTY']])
                # print(Multiboxes[0])
                for i in range(0, int(Quantity)):
                    boxes.append([row1['Id']])
                    # print(i)
                    i += 1

                # Database.insert_data(conn, list)

            print(Multiboxes,len(Multiboxes))

            print("Data Imported!")
            print(container, Multiboxes)
            print(len(boxes), boxes)
            dataset = ds.Multi_Packing_Prepare(conn, container, Multiboxes)
            # dataset = ds.Packing_Prepare(conn, container, boxes)
            print(dataset)
        else:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText("Please select an input file")

    @QtCore.Slot()
    def import_file(self):
        fileName = str(QFileDialog.getOpenFileName(self, "open file", '..', "Excel files (*.xlsx)")[0])
        print(fileName)

        # print(fileName.partition(".xlsx"))
        # Database.create_table_cur(conn,"box")
        if fileName != 0:
            df = pd.read_excel(fileName)
            # print(df.columns[0])

            for index, row in df.iterrows():
                # print(df.columns)
                # print(type(df.loc[:'Length']))
                list = [row[0]]
                append_data(list, row['Length'])
                append_data(list, row['Width'])
                append_data(list, row['Height'])
                append_data(list, row['Weight'])
                # print(list[0])
                Database.insert_data(conn, list)

            # print(list)
            print("Data Imported!")
        else:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText("Please select an input file")

        pass

    @QtCore.Slot()
    def interactive_run(self):
        # interactive.start()
        # main
        print("Exit")
        sys.exit()
        pass


def start():
    app = QtWidgets.QApplication([])

    widget = Menu()
    widget.resize(800, 400)
    widget.setWindowTitle("Welcome to Mobis Packing!")
    print("Welcome to Mobis Packing!")

    widget.show()

    sys.exit(app.exec())
    conn.close()


def append_data(sensorlist, sensor_data):
    sensorlist.append(sensor_data)
    # print(sensorlist)


if __name__ == "__main__":
    start()
    conn.close()
