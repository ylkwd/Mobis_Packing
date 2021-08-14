import logging
import sys

import PySide2
import numpy as np
from itertools import product, combinations

from PyQt5.QtWidgets import qApp
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import axes3d
from PySide2.QtCore import Qt, Slot
from PySide2.QtGui import QKeySequence, QColor
from PySide2.QtWidgets import (QAction, QApplication, QComboBox, QHBoxLayout,
                               QHeaderView, QLabel, QMainWindow, QSlider,
                               QTableWidget, QTableWidgetItem, QVBoxLayout,
                               QWidget)

import Ingest
import Sort
import palletize
from lib.Container import Container
from lib.Item import Item

import hashlib

"""This example implements the interaction between Qt Widgets and a 3D
matplotlib plot"""


def init(data) -> list:
    items = []
    for item in data.iterrows():
        obj = Item(item[1]["Length"], item[1]["Width"], item[1]["Height"], item[1]["Weight"],
                   str(item[1]["Code/Serial Number"]))
        items.append(obj)
    return items


class ApplicationWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        logi = [0, 0, 0]
        self.container = Container(0, 0, 0, logi, 100, 10, 5)

        self.column_names = ["Column A", "Column B", "Column C"]

        # Central widget
        self._main = QWidget()
        self.setCentralWidget(self._main)

        # Main menu bar
        self.menu = self.menuBar()
        self.menu_file = self.menu.addMenu("File")
        exit = QAction("Exit", self, triggered=qApp.quit)
        self.menu_file.addAction(exit)

        self.menu_about = self.menu.addMenu("&About")
        about = QAction("About Qt", self, shortcut=QKeySequence(QKeySequence.HelpContents),
                        triggered=qApp.aboutQt)
        self.menu_about.addAction(about)

        # Figure (Left)
        self.fig = Figure(figsize=(5, 3))
        self.canvas = FigureCanvas(self.fig)

        # Sliders (Left)
        self.slider_azim = QSlider(minimum=0, maximum=360, orientation=Qt.Horizontal)
        self.slider_elev = QSlider(minimum=0, maximum=360, orientation=Qt.Horizontal)

        self.slider_azim_layout = QHBoxLayout()
        self.slider_azim_layout.addWidget(QLabel("{}".format(self.slider_azim.minimum())))
        self.slider_azim_layout.addWidget(self.slider_azim)
        self.slider_azim_layout.addWidget(QLabel("{}".format(self.slider_azim.maximum())))

        self.slider_elev_layout = QHBoxLayout()
        self.slider_elev_layout.addWidget(QLabel("{}".format(self.slider_elev.minimum())))
        self.slider_elev_layout.addWidget(self.slider_elev)
        self.slider_elev_layout.addWidget(QLabel("{}".format(self.slider_elev.maximum())))

        # Table (Right)
        self.table = QTableWidget()
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        # ComboBox (Right)
        self.combo = QComboBox()
        self.load_list()
        # items = ["Wired", "Surface", "Triangular Surface", "Sphere", "Cube"]
        items = []
        for i in range(len(self.shipment)):
            items.append(f"Crate {1+i}")
        self.combo.addItems(items)

        # Right layout
        rlayout = QVBoxLayout()
        rlayout.setContentsMargins(1, 1, 1, 1)
        rlayout.addWidget(QLabel("Plot type:"))
        rlayout.addWidget(self.combo)
        rlayout.addWidget(self.table)

        # Left layout
        llayout = QVBoxLayout()
        rlayout.setContentsMargins(1, 1, 1, 1)
        llayout.addWidget(self.canvas, 88)
        llayout.addWidget(QLabel("Azimuth:"), 1)
        llayout.addLayout(self.slider_azim_layout, 5)
        llayout.addWidget(QLabel("Elevation:"), 1)
        llayout.addLayout(self.slider_elev_layout, 5)

        # Main layout
        layout = QHBoxLayout(self._main)
        layout.addLayout(llayout, 70)
        layout.addLayout(rlayout, 30)

        # Signal and Slots connections
        self.combo.currentTextChanged.connect(self.combo_option)
        self.slider_azim.valueChanged.connect(self.rotate_azim)
        self.slider_elev.valueChanged.connect(self.rotate_elev)

        # Initial setup
        self.plot_dyn_cube(self.shipment, 0)
        self._ax.view_init(30, 30)
        self.slider_azim.setValue(30)
        self.slider_elev.setValue(30)
        # self.fig.canvas.mpl_connect("button_release_event", self.on_click)

    # Matplotlib slot method
    def on_click(self, event):
        azim, elev = self._ax.azim, self._ax.elev
        self.slider_azim.setValue(azim + 180)
        self.slider_elev.setValue(elev + 180)

    # Utils methods

    def set_table_data(self, X, Y, Z):
        for i in range(len(X)):
            self.table.setItem(i, 0, QTableWidgetItem("{:.2f}".format(X[i])))
            self.table.setItem(i, 1, QTableWidgetItem("{:.2f}".format(Y[i])))
            self.table.setItem(i, 2, QTableWidgetItem("{:.2f}".format(Z[i])))

    def clear_table_data(self):
        for i in range(self.table.rowCount()):
            for j in range(self.table.colorCount()):
                self.table.setItem(i, j, QTableWidgetItem(""))

    def set_table_data_container(self, data):
        self.clear_table_data()
        table_row = 0
        seen = []
        for i in range(len(data)):
            if data[i].item is None or data[i].item.get_serial() in seen:
                continue

            color = QColor()
            hex_code = f'#{self.serial_hash(data[i].item.get_serial())}'
            color.setNamedColor(hex_code)
            print(hex_code)
            self.table.setItem(table_row, 0, QTableWidgetItem())
            self.table.item(table_row, 0).setBackground(color)
            self.table.setItem(table_row, 1, QTableWidgetItem(data[i].item.get_serial()))
            table_row += 1
            seen.append(data[i].item.get_serial())

    def set_canvas_table_configuration(self, row_count, data):
        self.fig.set_canvas(self.canvas)
        self._ax = self.canvas.figure.add_subplot(projection="3d")

        self._ax.set_xlabel(self.column_names[0])
        self._ax.set_ylabel(self.column_names[1])
        self._ax.set_zlabel(self.column_names[2])

        self.table.setRowCount(row_count)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(self.column_names)
        self.set_table_data(data[0], data[1], data[2])

    def set_canvas_table_configuration_containers(self, row_count, data):
        self.fig.set_canvas(self.canvas)
        self._ax = self.canvas.figure.add_subplot(projection="3d")

        self.table.setRowCount(row_count)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(self.column_names)
        self.set_table_data_container(data)

    def serial_hash(self, item_serial: str) -> str:
        sha = hashlib.sha256()
        sha.update(item_serial.encode())
        return sha.hexdigest()[:6]

    def load_list(self):
        self.data = Ingest.ingest("../../", 'Book1.xlsx')
        self.items = init(self.data)
        self.items = Sort.item_sort(self.items)
        print(self.items[0])
        print(self.items[len(self.items) - 1])
        logi = [0, 0, 0]
        self.containerTemplate = Container(0, 0, 0, logi, 1087, 1277, 980)
        self.shipment = palletize.palletize(self.items, self.containerTemplate)
        print(self.shipment)

    # Plot methods

    def plot_wire(self):
        # Data
        self.X, self.Y, self.Z = axes3d.get_test_data(0.03)

        self.set_canvas_table_configuration(len(self.X[0]), (self.X[0], self.Y[0], self.Z[0]))
        self._ax.plot_wireframe(self.X, self.Y, self.Z, rstride=10, cstride=10, cmap="viridis")
        self.canvas.draw()

    def plot_surface(self):
        # Data
        self.X, self.Y = np.meshgrid(np.linspace(-6, 6, 30), np.linspace(-6, 6, 30))
        self.Z = np.sin(np.sqrt(self.X ** 2 + self.Y ** 2))

        self.set_canvas_table_configuration(len(self.X[0]), (self.X[0], self.Y[0], self.Z[0]))
        self._ax.plot_surface(self.X, self.Y, self.Z,
                              rstride=1, cstride=1, cmap="viridis", edgecolor="none")
        self.canvas.draw()

    def plot_triangular_surface(self):
        # Data
        radii = np.linspace(0.125, 1.0, 8)
        angles = np.linspace(0, 2 * np.pi, 36, endpoint=False)[..., np.newaxis]
        self.X = np.append(0, (radii * np.cos(angles)).flatten())
        self.Y = np.append(0, (radii * np.sin(angles)).flatten())
        self.Z = np.sin(-self.X * self.Y)

        self.set_canvas_table_configuration(len(self.X), (self.X, self.Y, self.Z))
        self._ax.plot_trisurf(self.X, self.Y, self.Z, linewidth=0.2, antialiased=True)
        self.canvas.draw()

    def plot_sphere(self):
        # Data
        u = np.linspace(0, 2 * np.pi, 100)
        v = np.linspace(0, np.pi, 100)
        self.X = 10 * np.outer(np.cos(u), np.sin(v))
        self.Y = 10 * np.outer(np.sin(u), np.sin(v))
        self.Z = 9 * np.outer(np.ones(np.size(u)), np.cos(v))

        self.set_canvas_table_configuration(len(self.X), (self.X[0], self.Y[0], self.Z[0]))
        self._ax.plot_surface(self.X, self.Y, self.Z)
        self.canvas.draw()

    def plot_cube(self):
        self._ax.cla()
        r = [-10, 10]
        for s, e in combinations(np.array(list(product(r, r, r))), 2):
            if np.sum(np.abs(s - e)) == r[1] - r[0]:
                self._ax.plot3D(*zip(s, e), color="b")

        self.canvas.draw()

    def plot_dyn_cube(self, shipment: list, index: int):
        if hasattr(self, "_ax"):
            self._ax.cla()
        self.set_canvas_table_configuration_containers(len(self.shipment), self.shipment[index])

        for container in shipment[index]:
            print(container)
            if container.item is None:
                continue
            verts = np.array([
                [container.x, container.y, container.z],                                                                                         # 0
                [container.x+container.item.get_length(), container.y, container.z],                                                             # 1
                [container.x, container.y+container.item.get_width(), container.z],                                                              # 2
                [container.x+container.item.get_length(), container.y+container.item.get_width(), container.z],                                  # 3
                [container.x, container.y, container.z+container.item.get_height()],                                                             # 4
                [container.x + container.item.get_length(), container.y, container.z+container.item.get_height()],                               # 5
                [container.x, container.y + container.item.get_width(), container.z+container.item.get_height()],                                # 6
                [container.x + container.item.get_length(), container.y + container.item.get_width(), container.z+container.item.get_height()],  # 7
            ])
            faces = [
                [verts[0], verts[1], verts[3], verts[2]],  # Top
                [verts[4], verts[5], verts[7], verts[6]],  # Bottom
                [verts[2], verts[3], verts[7], verts[6]],  # North
                [verts[0], verts[1], verts[5], verts[4]],  # South
                [verts[0], verts[2], verts[6], verts[4]],  # East
                [verts[1], verts[3], verts[7], verts[5]]   # West
            ]

            self._ax.scatter3D(verts[:, 0], verts[:, 1], verts[:, 2], alpha=0)
            color = self.serial_hash(container.item.get_serial())
            self._ax.add_collection3d(Poly3DCollection(faces, facecolors=f'#{color}', linewidths=1, edgecolors='b', alpha=.5))

        verts = np.array([
            [self.containerTemplate.x, self.containerTemplate.y, self.containerTemplate.z],  # 0
            [self.containerTemplate.x + self.containerTemplate.length, self.containerTemplate.y, self.containerTemplate.z],  # 1
            [self.containerTemplate.x, self.containerTemplate.y + self.containerTemplate.width, self.containerTemplate.z],  # 2
            [self.containerTemplate.x + self.containerTemplate.length, self.containerTemplate.y + self.containerTemplate.width, self.containerTemplate.z],  # 3
            [self.containerTemplate.x, self.containerTemplate.y, self.containerTemplate.z + self.containerTemplate.height],  # 4
            [self.containerTemplate.x + self.containerTemplate.length, self.containerTemplate.y, self.containerTemplate.z + self.containerTemplate.height],  # 5
            [self.containerTemplate.x, self.containerTemplate.y + self.containerTemplate.width, self.containerTemplate.z + self.containerTemplate.height],  # 6
            [self.containerTemplate.x + self.containerTemplate.length, self.containerTemplate.y + self.containerTemplate.width, self.containerTemplate.z + self.containerTemplate.height],  # 7
        ])
        self._ax.scatter3D(verts[:, 0], verts[:, 1], verts[:, 2])

        self._ax.set_xlabel('X')
        self._ax.set_ylabel('Y')
        self._ax.set_zlabel('Z')
        self.canvas.draw()

    # Slots

    @Slot()
    def combo_option(self, text):
        if text == "Wired":
            self.plot_wire()
        elif text == "Surface":
            self.plot_surface()
        elif text == "Triangular Surface":
            self.plot_triangular_surface()
        elif text == "Sphere":
            self.plot_sphere()
        elif text == "Cube":
            self.plot_cube()
        for i in range(len(self.shipment)):
            if text == f"Crate {1 + i}":
                self.plot_dyn_cube(self.shipment, i)

    @Slot()
    def rotate_azim(self, value):
        self._ax.view_init(self._ax.elev, value)
        self.fig.set_canvas(self.canvas)
        self.canvas.draw()

    @Slot()
    def rotate_elev(self, value):
        self._ax.view_init(value, self._ax.azim)
        self.fig.set_canvas(self.canvas)
        self.canvas.draw()


def start():
    app = QApplication(sys.argv)
    w = ApplicationWindow()
    w.setFixedSize(1280, 720)
    w.show()
    app.exec()


if __name__ == "__main__":
    start()
