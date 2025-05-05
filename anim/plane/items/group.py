import numpy as np

from PyQt6.QtCore import Qt, QPointF, QRectF, QSize
from PyQt6.QtGui import QColor, QPen, QBrush, QPolygonF, QFont, QPainterPath, QTransform, QPixmap, QImage, qRgb
from PyQt6.QtWidgets import QAbstractGraphicsShapeItem, QGraphicsItem, QGraphicsItemGroup, QGraphicsTextItem, QGraphicsLineItem, QGraphicsEllipseItem, QGraphicsPolygonItem, QGraphicsRectItem, QGraphicsPathItem, QGraphicsPixmapItem

from ..itemDict import item

class group(item, QGraphicsItemGroup):
  """
  Group item

  A group item has no representation upon display but serves as a parent for
  multiple other items in order to create and manipulate composed objects.  
  """

  # ────────────────────────────────────────────────────────────────────────
  def __init__(self, view, name, **kwargs):
    """
    Group item constructor

    Defines a group, which inherits both from ``QGraphicsItemGroup`` and
    :class:`item`.

    Args:

      view (:class:`Animaton2d`): The view container.

      name (str): The item's identifier, which should be unique. It is used as a
        reference by :class:`view2d`. This is the only mandatory argument.

      parent (*QGraphicsItem*): The parent ``QGraphicsItem`` in the ``QGraphicsScene``.
        Default is ``None``, which means the parent is the ``QGraphicsScene`` itself.

      zvalue (float): Z-value (stack order) of the item.

      position ([float,float]): Position of the ``group``, ``text``, 
        ``circle``, and ``rectangle`` elements (scene units).

      orientation (float): Orientation of the item (rad)

      clickable (bool): *TO DO*

      movable (bool): If True, the element will be draggable. (default: ``False``)
    """  

    # Generic item constructor
    super().__init__(view, name, **kwargs)
   
  # ────────────────────────────────────────────────────────────────────────
  def width(self):
    return self.childrenBoundingRect().width()

  # ────────────────────────────────────────────────────────────────────────
  def height(self):
    return self.childrenBoundingRect().height()
