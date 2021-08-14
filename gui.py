import sys
import random

import PySide6
from PySide6 import QtCore, QtWidgets, QtGui

import Ingest
import Sort
import palletize
from lib.Container import Container
from lib.Item import Item


def init(data) -> list:
    items = []
    for item in data.iterrows():
        obj = Item(item[1]["Length"], item[1]["Width"], item[1]["Height"], item[1]["Weight"],
                        item[1]["Code/Serial Number"])
        items.append(obj)
    return items


class Gui(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир"]
        self.button = QtWidgets.QPushButton("Click me!")
        self.update_table_button = QtWidgets.QPushButton("Update Table")
        self.clear_table_button = QtWidgets.QPushButton("Clear Table")
        self.text = QtWidgets.QLabel("Hello World", alignment=QtCore.Qt.AlignCenter)

        self.splitter = QtWidgets.QSplitter()
        self.tableWidget = QtWidgets.QTableWidget(10, 1, self)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.splitter.addWidget(self.tableWidget)

        self.layout = QtWidgets.QGridLayout(self)
        self.layout.setGeometry(QtCore.QRect(0, 0, 3, 3))
        self.layout.addWidget(self.text, 1, 0)
        self.layout.addWidget(self.button, 1, 1)
        self.layout.addWidget(self.splitter, 2, 1, 1, 2)
        self.layout.addWidget(self.update_table_button, 3, 1)
        self.layout.addWidget(self.clear_table_button, 3, 0)

        self.button.clicked.connect(self.magic)
        self.update_table_button.clicked.connect(self.update_table)
        self.clear_table_button.clicked.connect(self.clear_table)

    def showEvent(self, event:PySide6.QtGui.QShowEvent) -> None:
        self.load_list()
        self.update_table()

    def load_list(self):
        self.data = Ingest.ingest("../../", 'IngestTemplate.xlsx')
        self.items = init(self.data)
        self.items = Sort.item_sort(self.items)
        print(self.items[0])
        print(self.items[len(self.items) - 1])
        self.containerTemplate = Container(0, 0, 0, 2000, 3000, 2000)
        self.shipment = palletize.palletize(self.items, self.containerTemplate)
        print(self.shipment)

    @QtCore.Slot()
    def magic(self):
        self.text.setText(random.choice(self.hello))
        self.load_list()

    @QtCore.Slot()
    def update_table(self):
        for row in range(0, 10):
            temp = QtWidgets.QTableWidgetItem(f"{self.shipment[0][row]}")
            self.tableWidget.setItem(row, 0, temp)

    @QtCore.Slot()
    def clear_table(self):
        for row in range(0, 10):
            for column in range(0, 2):
                temp = QtWidgets.QTableWidgetItem("")
                self.tableWidget.setItem(row, column, temp)


def start():
    app = QtWidgets.QApplication([])

    widget = Gui()
    widget.resize(800, 400)
    widget.show()

    sys.exit(app.exec_())
