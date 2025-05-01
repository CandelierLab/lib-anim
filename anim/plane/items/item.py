'''
Generic item
'''

import numpy as np

from PyQt6.QtCore import Qt, QPointF, QRectF, QSize
from PyQt6.QtGui import QColor, QPen, QBrush, QPolygonF, QFont, QPainterPath, QTransform, QPixmap, QImage, qRgb
from PyQt6.QtWidgets import QAbstractGraphicsShapeItem, QGraphicsItem, QGraphicsItemGroup, QGraphicsTextItem, QGraphicsLineItem, QGraphicsEllipseItem, QGraphicsPolygonItem, QGraphicsRectItem, QGraphicsPathItem, QGraphicsPixmapItem

# ══════════════════════════════════════════════════════════════════════════
#                               GENERIC ITEM
# ══════════════════════════════════════════════════════════════════════════

class item:
  '''
  Item of the view (generic class)

  Items are the elements displayed in the Qscene. 
  This class provides a common constructor, positioning scheme
  and styling of ``QAbstractGraphicsShapeItem`` children.

  Methods:

    width():  return the item width
    height(): return the item height

  '''

  # ────────────────────────────────────────────────────────────────────────
  def __init__(self, view, name, **kwargs):
    '''
    Constructor
    '''

    # Parent constructor
    super().__init__()

    # ─── Definitions

    # Reference view
    self.view = view

    # Assign name
    self.name = name

    # Internal properties
    self._parent = None
    self._behindParent = None
    self._position = [0,0]
    self._shift = [0,0]
    self._transformPt = [0,0]
    self._orientation = None
    self._scale = None
    self._zvalue = None
    self._draggable = None
      
    # ─── Initialization

    if 'parent' in kwargs: self.parent = kwargs['parent']
    if 'behindParent' in kwargs: self.behindParent = kwargs['behindParent']
    if 'position' in kwargs: self.position = kwargs['position']
    if 'transformPt' in kwargs: self.transformPt = kwargs['transformPt']
    if 'orientation' in kwargs: self.orientation = kwargs['orientation']
    if 'scale' in kwargs: self.scale = kwargs['scale']
    if 'zvalue' in kwargs: self.zvalue = kwargs['zvalue']
    if 'draggable' in kwargs: self.draggable = kwargs['draggable']
    
  # ════════════════════════════════════════════════════════════════════════
  #                              GETTERS
  # ════════════════════════════════════════════════════════════════════════

  # ────────────────────────────────────────────────────────────────────────
  def width(self):
    return self.boundingRect().width()

  # ────────────────────────────────────────────────────────────────────────
  def height(self):
    return self.boundingRect().height()

  # ════════════════════════════════════════════════════════════════════════
  #                              SETTERS
  # ════════════════════════════════════════════════════════════════════════

  # ────────────────────────────────────────────────────────────────────────
  def place(self):
    '''
    Absolute positionning
    '''

    # Set position
    self.setPos(self._position[0]-self._shift[0], self._position[1]-self._shift[1])

  # ────────────────────────────────────────────────────────────────────────
  def move(self, dx=None, dy=None, z=None):
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

    # Store position
    if dx is not None: self._position[0] += dx
    if dy is not None: self._position[1] += dy

    self.place()

  # ────────────────────────────────────────────────────────────────────────
  def rotate(self, angle):
    '''
    Relative rotation

    Rotates the item relatively to its current orientation.
    
    Attributes:
      angle (float): Orientational increment (rad)
    '''

    self._orientation += angle
    self.setRotation(rad2deg(self.orientation))

  # ────────────────────────────────────────────────────────────────────────
  def setStyle(self):
    '''
    Item styling

    This function does not take any argument, instead it applies the changes
    defined by each item's styling attributes (*e.g.* color, stroke thickness).
    '''

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

    self.view.change(event.button(), self)
    super().mousePressEvent(event)

  # ────────────────────────────────────────────────────────────────────────
  def mouseDoubleClickEvent(self, event):
    '''
    Double click event

    For internal use only.

    args:
      event (QGraphicsSceneMouseEvent): The double click event.
    '''

    self.view.change(event.button().__str__() + '.double', self)
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

    # -- Define type

    type = None

    match change:
      case QGraphicsItem.GraphicsItemChange.ItemPositionHasChanged:
        type = 'move'

    # Report to view
    if type is not None:
      self.view.change(type, self)

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
  def parent(self, pName):
    self._parent = pName
    self.setParentItem(self.view.item[self._parent])

  # ─── behindParent ───────────────────────────────────────────────────────
    
  ''' A boolean specifying the stack order '''

  @property
  def behindParent(self): return self._behindParent

  @behindParent.setter
  def behindParent(self, b):
    self._behindParent = b
    self.setFlag(QGraphicsItem.ItemStacksBehindParent, b)

  # ─── Position ───────────────────────────────────────────────────────────
  
  ''' The position of the item's reference point '''

  @property
  def position(self): return self._position

  @position.setter
  def position(self, pos):
    
    if isinstance(pos, complex):

      # Convert from complex coordinates
      x = np.real(pos)
      y = np.imag(pos)

    else:

      # Doublet input
      x = pos[0]  
      y = pos[1]      

    # Store position
    self._position = [x,y]

    # Set position
    self.place()    

  # ─── Transform point ────────────────────────────────────────────────────
  
  ''' The position of the iterm's transformation point (origin) '''

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
    self.setTransformOriginPoint(x, y)    

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
  def draggable(self, z):
    
    self._draggable = z
    
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
  def __init__(self, **kwargs):

    super().__init__()

    # Color
    self._color = kwargs['color'] if 'color' in kwargs else 'gray'

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
  def __init__(self, **kwargs):

    super().__init__()

    # Stroke color
    self._stroke = kwargs['stroke'] if 'stroke' in kwargs else None

    # Thickness
    self._thickness = kwargs['thickness'] if 'thickness' in kwargs else 0

    # Linestyle
    self._linestyle = kwargs['linestyle'] if 'linestyle' in kwargs else '-'

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
  