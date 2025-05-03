import os

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsItem, QGraphicsRectItem
from PyQt6.QtGui import QBrush, QPen

os.system('clear')

# Define app and scene
app = QApplication([])
scene = QGraphicsScene(0, 0, 500, 500)

# Create a red square
rect = QGraphicsRectItem(100, 100, 100, 100)
rect.setBrush(QBrush(Qt.GlobalColor.red))

# rect.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
# rect.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges, True)

# rect.setCacheMode(QGraphicsItem.CacheMode.ItemCoordinateCache)
# rect.setCacheMode(QGraphicsItem.CacheMode.DeviceCoordinateCache)

# Display
scene.addItem(rect)
view = QGraphicsView(scene)
view.show()
app.exec()