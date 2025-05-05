import numpy as np

from PyQt6.QtCore import Qt, QPointF, QRectF, QSize
from PyQt6.QtGui import QColor, QPen, QBrush, QPolygonF, QFont, QPainterPath, QTransform, QPixmap, QImage, qRgb
from PyQt6.QtWidgets import QAbstractGraphicsShapeItem, QGraphicsItem, QGraphicsItemGroup, QGraphicsTextItem, QGraphicsLineItem, QGraphicsEllipseItem, QGraphicsPolygonItem, QGraphicsRectItem, QGraphicsPathItem, QGraphicsPixmapItem

from .item import item

class group(item, QGraphicsItemGroup):
  '''
  Group item

  A group item has no representation upon display but serves as a parent for
  multiple other items in order to create and manipulate compositions.

  Parameters
  ══════════

    * name        (str)             The rectangle's name
    * parent      (*QGraphicsItem*) The rectangle's parent item

    ─── position & transformations ──────────────

    * position    ([float, float])  Position of the reference point. Default: [0,0]
    * orientation (float)           Orientation of the item (rad). Default: 0
    * scale       (float)           Scaling factor. Default: None
    * transformPt ([float, float])  Origin of the transformation
    * draggable   (bool)            Boolean specifying if the item can be 
                                      dragged. If True, the dragging callback
                                      is defined in the ... method. 
                                      Default: False.

    ─── stack ───────────────────────────────────

    * zvalue      (float)           Z-value (stack order) of the item. Default: 1
    * behindParent (bool)           Boolean specifying if the item is behind
                                      its parent or not. Default: None    
  '''

  # ────────────────────────────────────────────────────────────────────────
  def __init__(self, 
               parent = None,
               behindParent = False,
               position = [0,0],
               transformPt = [0,0],
               orientation = 0,
               scale = 1,
               zvalue = 0,
               draggable = False):
    '''
    Group item constructor

    Defines a group, which inherits both from ``QGraphicsItemGroup`` and
    :class:`item`.
    '''  

    # Parent constructors    
    item.__init__(self, 
                  parent = parent,
                  behindParent = behindParent,
                  position = position,
                  transformPt = transformPt,
                  orientation = orientation,
                  scale = scale,
                  zvalue = zvalue,
                  draggable = draggable)
   
  # ────────────────────────────────────────────────────────────────────────
  def width(self):
    return self.childrenBoundingRect().width()

  # ────────────────────────────────────────────────────────────────────────
  def height(self):
    return self.childrenBoundingRect().height()
