'''
Generic item
'''

import numbers
import numpy as np

from PyQt6.QtCore import Qt, QPointF, QRectF, QSize
from PyQt6.QtGui import QColor, QPen, QBrush, QPolygonF, QFont, QPainterPath, QTransform, QPixmap, QImage, qRgb
from PyQt6.QtWidgets import QAbstractGraphicsShapeItem, QGraphicsItem, QGraphicsItemGroup, QGraphicsTextItem, QGraphicsLineItem, QGraphicsEllipseItem, QGraphicsPolygonItem, QGraphicsRectItem, QGraphicsPathItem, QGraphicsPixmapItem

from ..canva import canva

# ══════════════════════════════════════════════════════════════════════════
#                               GENERIC ITEM
# ══════════════════════════════════════════════════════════════════════════

class item:
  '''
  Item of the canva (generic class)

  Items are the elements displayed in the Qscene. 
  This class provides a common constructor, positioning scheme
  and styling of ``QAbstractGraphicsShapeItem`` children.

  Methods:

    width():  return the item width
    height(): return the item height

  Position of the item, in parent coordinates. For items with no parent, it is in scene coordinates.

  '''

  # ────────────────────────────────────────────────────────────────────────
  def __init__(self, 
               parent = None,
               behindParent = False,
               x = 0,
               y = 0,
               position = None,
               transformPt = [0,0],
               orientation = 0,
               scale = 1,
               zvalue = 0,
               draggable = False):
    '''
    Constructor
    '''

    # Parent constructor
    super().__init__()

    # Initialization attribute
    self.is_initialized = False

    # ─── Definitions

    # Reference canva
    self.canva:canva = None

    # Assign name
    self.name = None

    # Internal properties
    self._parent = parent
    self.behindParent = behindParent

    self._x = x
    self._y = y
    
    if position is not None and isinstance(position, (tuple, list, complex)):
      self.position = position

    elif x is None or y is None:
      raise AttributeError("Item position must be specified, either with 'position' or with 'x' and 'y'.")
      
    else:
      self.x = x
      self.y = y

    self.transformPt = transformPt
    self.orientation = orientation
    self.scale = scale
    self.zvalue = zvalue
    self.draggable = draggable

  # ────────────────────────────────────────────────────────────────────────
  def initialize(self):
    '''
    Initialize the display
    '''

    # Set as initialized
    self.is_initialized = True

    # ─── Parent

    if self._parent is not None:

      # Assign parent
      self.parent = self._parent

    # ─── Style

    self.setStyle()

  # ════════════════════════════════════════════════════════════════════════
  #                              GETTERS
  # ════════════════════════════════════════════════════════════════════════

  # ────────────────────────────────────────────────────────────────────────
  def Lx(self):
    return self.boundingRect().width()

  # ────────────────────────────────────────────────────────────────────────
  def Ly(self):
    return self.boundingRect().height()

  # ────────────────────────────────────────────────────────────────────────
  def absoluteCoordinates(self):

    x = self._x
    y = self._y

    # Check parenthood
    parent = self._parent
    while parent is not None:

      # Shift position
      x += parent._x
      y += parent._y

      # Update parent
      parent = parent._parent

    return (x, y)

  # ════════════════════════════════════════════════════════════════════════
  #                              SETTERS
  # ════════════════════════════════════════════════════════════════════════

  # ────────────────────────────────────────────────────────────────────────
  def put(self):
    '''
    Place the item in the scene
    '''

    # Wait for initialization
    if not self.is_initialized: return

    # Get absolute coordinates
    x, y = self.absoluteCoordinates()

    # Place on the canva
    self.setPos(x, self.canva.boundaries.y1 - y)

  # ────────────────────────────────────────────────────────────────────────
  def move(self, dx=0, dy=0, z=None):
    '''
    Relative displacement

    Displaces the item of relative amounts.
    
    Attributes:
      dx (float): :math:`x`-coordinate of the displacement. It can also be a 
        doublet [`dx`,`dy`], in this case the *dy* argument is overridden.
      dy (float): :math:`y`-coordinate of the displacement.
      z (float): A complex number :math:`z = dx+jdy`. Specifying ``z``
        overrides the ``x`` and ``y`` arguments.
    '''

    # Doublet input
    if isinstance(dx, (tuple, list)):
      dy = dx[1]
      dx = dx[0]  

    # Convert from complex coordinates
    if z is not None:
      dx = np.real(z)
      dy = np.imag(z)

    # Update position
    self.x += dx
    self.y += dy

  # ────────────────────────────────────────────────────────────────────────
  def rotate(self, angle):
    '''
    Relative rotation

    Rotates the item relatively to its current orientation.
    
    Attributes:
      angle (float): Orientational increment (rad)
    '''

    self.orientation += angle

  # ────────────────────────────────────────────────────────────────────────
  def setStyle(self):
    '''
    Item styling

    This function does not take any argument, instead it applies the changes
    defined by each item's styling attributes (*e.g.* color, stroke thickness).
    '''

    # Wait for initialization
    if not self.is_initialized: return

    # ─── Fill

    if isinstance(self, QAbstractGraphicsShapeItem):

      if self._color is not None:
        self.setBrush(QBrush(QColor(self._color)))

    # ─── Stroke

    if isinstance(self, (QAbstractGraphicsShapeItem, QGraphicsLineItem)):

      Pen = QPen()

      #  Color
      if self._stroke is not None:
        Pen.setColor(QColor(self._stroke))

      # Thickness
      if self._thickness is not None:
        Pen.setWidthF(self._thickness)

      # Style
      match self._linestyle:
        case 'dash' | '--': Pen.setDashPattern([3,6])
        case 'dot' | ':' | '..': Pen.setStyle(Qt.PenStyle.DotLine)
        case 'dashdot' | '-.': Pen.setDashPattern([3,3,1,3])
      
      self.setPen(Pen)

  # ════════════════════════════════════════════════════════════════════════
  #                              EVENTS
  # ════════════════════════════════════════════════════════════════════════

  # ────────────────────────────────────────────────────────────────────────
  def mousePressEvent(self, event):
    '''
    Simple click event

    For internal use only.

    args:
      event (QGraphicsSceneMouseEvent): The click event.
    '''

    self.canva.change(event.button(), self)
    super().mousePressEvent(event)

  # ────────────────────────────────────────────────────────────────────────
  def mouseDoubleClickEvent(self, event):
    '''
    Double click event

    For internal use only.

    args:
      event (QGraphicsSceneMouseEvent): The double click event.
    '''

    self.canva.change(event.button().__str__() + '.double', self)
    super().mousePressEvent(event)

  # ────────────────────────────────────────────────────────────────────────
  def itemChange(self, change, value):
    '''
    Item change notification

    This method is triggered upon item change. The item's transformation
    matrix has changed either because setTransform is called, or one of the
    transformation properties is changed. This notification is sent if the 
    ``ItemSendsGeometryChanges`` flag is enabled (e.g. when an item is 
    :py:attr:`item.movable`), and after the item's local transformation 
    matrix has changed.

    args:

      change (QGraphicsItem constant): 
    '''

    # ─── Define type

    type = None

    match change:
      case QGraphicsItem.GraphicsItemChange.ItemPositionHasChanged:
        type = 'move'

    # Report to canva
    if type is not None:
      self.canva.change(type, self)

    # Propagate change
    return super().itemChange(change, value)

  # ════════════════════════════════════════════════════════════════════════
  #                             PROPERTIES
  # ════════════════════════════════════════════════════════════════════════

  # ─── Parent ─────────────────────────────────────────────────────────────
  
  ''' The parent item '''

  @property
  def parent(self): return self._parent

  @parent.setter
  def parent(self, parent):

    if isinstance(self._parent, str):
      self._parent = self.canva.item[self._parent]
    else:
      self._parent = parent

    self.setParentItem(self._parent)

  # ─── behindParent ───────────────────────────────────────────────────────
    
  ''' A boolean specifying the stack order '''

  @property
  def behindParent(self): return self._behindParent

  @behindParent.setter
  def behindParent(self, b):
    self._behindParent = b
    self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemStacksBehindParent, b)

  # ─── Position ───────────────────────────────────────────────────────────
  
  ''' The position of the item's reference point '''

  @property
  def x(self): return self._x

  @x.setter
  def x(self, f):
    self._x = f
    self.put()

  @property
  def y(self): return self._y

  @x.setter
  def y(self, f):
    self._y = f
    self.put()

  @property
  def position(self): return [self._x, self._y]

  @position.setter
  def position(self, pos):
    
    if isinstance(pos, complex):

      # Convert from complex coordinates
      self._x = np.real(pos)
      self._y = np.imag(pos)

    else:

      # Doublet input
      self._x = pos[0]  
      self._y = pos[1]      

    # Set position
    self.put()

  # ─── Transform point ────────────────────────────────────────────────────
  
  ''' The position of the item's transformation point (origin) '''

  @property
  def transformPt(self): return self._transformPt

  @transformPt.setter
  def transformPt(self, pt):
    
    if isinstance(pt, complex):

      # Convert from complex coordinates
      x = np.real(pt)
      y = np.imag(pt)

    else:

      # Doublet input
      x = pt[0]  
      y = pt[1]      

    # Store transform point
    self._transformPt = [x,y]

    # Set transform point
    self.setTransformOriginPoint(x, -y)

    # ─── Orientation ──────────────────────────────────────────────────────
  
  ''' The item's orientation '''

  @property
  def orientation(self): return self._orientation

  @orientation.setter
  def orientation(self, angle):
    self._orientation = angle
    self.setRotation(rad2deg(angle))

  # ─── Scale ──────────────────────────────────────────────────────────────
  
  ''' The item's scale '''

  @property
  def scale(self): return self._scale

  @scale.setter
  def scale(self, scale):

    if isinstance(scale, numbers.Number):
      scale = (scale, scale)

    self._scale = scale    

    self.setTransform(QTransform.fromScale(scale[0], scale[1]), True)

  # ─── z-value ────────────────────────────────────────────────────────────

  ''' The item's stack position '''

  @property
  def zvalue(self): return self._zvalue

  @zvalue.setter
  def zvalue(self, z):
    self._zvalue = z
    self.setZValue(self._zvalue)

  # ─── Draggability ───────────────────────────────────────────────────────
  
  ''' The item's draggability '''

  @property
  def draggable(self): return self._draggable

  @draggable.setter
  def draggable(self, bdrag):
    
    self._draggable = bdrag
    
    self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, self._draggable)
    self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges, self._draggable)

    if self._draggable:
      self.setCacheMode(QGraphicsItem.CacheMode.DeviceCoordinateCache)
      
# ══════════════════════════════════════════════════════════════════════════
#                        ITEMS WITH SPECIFIC PROPERTIES
# ══════════════════════════════════════════════════════════════════════════

# ══════════════════════════════════════════════════════════════════════════
class hasColor:

  # ────────────────────────────────────────────────────────────────────────
  def __init__(self, color='grey'):

    super().__init__()

    # Default color
    if color is None: color = 'grey'

    # Assign color
    self._color = color

  # ─── color ──────────────────────────────────────────────────────────────

  @property
  def color(self): return self._color

  @color.setter
  def color(self, C):
    self._color = C
    self.setStyle()

# ══════════════════════════════════════════════════════════════════════════
class hasStroke:

  # ────────────────────────────────────────────────────────────────────────
  def __init__(self, stroke=None, thickness=0, linestyle='-'):

    super().__init__()

    # Stroke color
    self._stroke = stroke

    # Thickness
    self._thickness = thickness

    # Linestyle
    self._linestyle = linestyle

  # ─── stroke ─────────────────────────────────────────────────────────────

  @property
  def stroke(self): return self._stroke

  @stroke.setter
  def stroke(self, s):
    self._stroke = s
    self.setStyle()

  # ─── thickness ──────────────────────────────────────────────────────────

  @property
  def thickness(self): return self._thickness

  @thickness.setter
  def thickness(self, t):
    self._thickness = t
    self.setStyle()

  # ─── linestyle ──────────────────────────────────────────────────────────

  @property
  def linestyle(self): return self._linestyle

  @linestyle.setter
  def linestyle(self, s):
    self._linestyle = s
    self.setStyle()      

# ──────────────────────────────────────────────────────────────────────────
def rad2deg(a):
  ''' Convert an angle in scene coordinates (radian to degrees) '''

  return -a*180/np.pi
  