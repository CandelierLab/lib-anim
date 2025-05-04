import os

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsItem, QGraphicsRectItem
from PyQt6.QtGui import QBrush, QPen

import anim

os.system('clear')

W = anim.window('minimal', display_information=False)

C = anim.plane.canva(W, boundaries=[[0,2], [0,2]])
W.add(C)

# C.

# # Define app and scene
# scene = QGraphicsScene(0, 0, 500, 500)

# # Create a red square
# rect = QGraphicsRectItem(100, 100, 100, 100)
# rect.setBrush(QBrush(Qt.GlobalColor.red))

# rect.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
# # rect.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges, True)

# # rect.setCacheMode(QGraphicsItem.CacheMode.ItemCoordinateCache)
# # rect.setCacheMode(QGraphicsItem.CacheMode.DeviceCoordinateCache)

# # Display
# scene.addItem(rect)
# view = QGraphicsView(scene)

# W.mainWidget = view
# W.setCentralWidget(W.mainWidget)

W.show()