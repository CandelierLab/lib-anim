import numpy as np

from PyQt6.QtCore import Qt, QPointF, QRectF, QSize
from PyQt6.QtGui import QColor, QPen, QBrush, QPolygonF, QFont, QPainterPath, QTransform, QPixmap, QImage, qRgb
from PyQt6.QtWidgets import QAbstractGraphicsShapeItem, QGraphicsItem, QGraphicsItemGroup, QGraphicsTextItem, QGraphicsLineItem, QGraphicsEllipseItem, QGraphicsPolygonItem, QGraphicsRectItem, QGraphicsPathItem, QGraphicsPixmapItem

from .item import item

class group(item):
  '''
  Group item

  A group item has no representation upon display but serves as a parent for
  multiple other items in order to create and manipulate compositions.

  Note on rotation: 
    Be carefull to rotate the group AFTER having added the items.

  Parameters
  ══════════

    * name       
        str
        The group name.

    * parent
        QGraphicsItem (or derived object)
        default: None
        The group's parent. If None, the position (x, y) is in absolute
        scene coordinates. Otherwise, the position is relative to the 
        parent's reference point.

    ─── position & transformations ──────────────

    * x           
        float
        default: 0
        x-position of the reference point.

    * y
        float
        default: 0
        y-position of the reference point.

    * position
        (float, float), [float, float], complex
        default: [0,0]
        Position of the reference point. The user can define either x, y or
        the position. In case of conflict, the position attribute wins.

    * orientation
        float
        default: 0, unit: radians
        Orientation of the item, with respect to the positive part of the 
        x-axis.

    * center_of_rotation
        None, (float, float), [float, float], complex
        default: None
        Center point for the rotation. If None, it is set to the current [x,y].

    * scale
        float
        default: 1
        Scaling factor.

    * draggable
        bool
        default: False
        Boolean specifying if the item can be dragged. If True, the dragging
        callback is defined in the 'itemChange' method, which is transfered
        to the canva's 'change' method (recommended).

    ─── stack ───────────────────────────────────

    * zvalue
        float
        default: 0
        Z-value (stack order) of the item.

  Methods
  ═══════
  
    * Lx(): return the group's total width
    * Ly(): return the group's total height
  '''

  # ────────────────────────────────────────────────────────────────────────
  def __init__(self,
               group = None,
               x = 0,
               y = 0,
               position = None,
               center_of_rotation = [0,0],
               orientation = 0,
               scale = 1,
               zvalue = 0,
               draggable = False):
    '''
    Group item constructor

    Defines a group, which inherits both from ``QGraphicsItemGroup`` and
    :class:`item`.
    '''  

    # ─── Parent constructor
    
    item.__init__(self, 
                  group = group,
                  x = x,
                  y = y,
                  position = position,
                  center_of_rotation = center_of_rotation,
                  orientation = orientation,
                  scale = scale,
                  zvalue = zvalue,
                  draggable = draggable)

    # ─── QGraphicsItem
    
    self.qitem = QGraphicsItemGroup()
  
  # ────────────────────────────────────────────────────────────────────────
  def setGeometry(self):
    '''
    Sets the group's position at the reference point.
    '''

    # Place on the canva
    if self.qitem is not None:
      self.qitem.setPos(self.position.X, self.position.Y)

  # ────────────────────────────────────────────────────────────────────────
  def Lx(self):
    return self.qitem.childrenBoundingRect().width()

  # ────────────────────────────────────────────────────────────────────────
  def Ly(self):
    return self.qitem.childrenBoundingRect().height()
