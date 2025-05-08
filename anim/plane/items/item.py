'''
Generic item
'''

import numbers
from copy import deepcopy
import numpy as np

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPen, QBrush, QTransform
from PyQt6.QtWidgets import QAbstractGraphicsShapeItem, QGraphicsItem, QGraphicsLineItem

from ..canva import canva
from ..point import point

# ══════════════════════════════════════════════════════════════════════════
#                               GENERIC ITEM
# ══════════════════════════════════════════════════════════════════════════

class item:
  '''
  Item of the canva (generic class), i.e. elements displayed in the Qscene.

  This is an abstract class providing a common constructor, positioning
  scheme and styling of ``QAbstractGraphicsShapeItem`` children. It is not
  intented to be instantiated directly.

  Parameters
  ══════════

    * name       
        str
        The item name.

    * parent
        QGraphicsItem (or derived object)
        default: None
        The item's parent. If None, the position of the reference point and
        center of rotation are in absolute coordinates. Otherwise, the
        position is relative to the parent's reference point.

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

    * behindParent
        bool
        Default: False
        Boolean specifying if the item is behind its parent or not.
    
  Methods
  ═══════
  
    * Lx(): return the item width
    * Ly(): return the item height
  '''

  # ────────────────────────────────────────────────────────────────────────
  def __init__(self, 
               parent = None,
               behindParent = False,
               x = 0,
               y = 0,
               position = None,
               center_of_rotation = [0,0],
               orientation = 0,
               scale = 1,
               zvalue = 0,
               draggable = False):
    '''
    Constructor
    '''

    # Initialization attribute
    self.is_initialized = False

    # ─── Definitions

    # Reference canva
    self.canva:canva = None

    # Assign name
    self.name = None

    # Internal properties
    self.parent = parent
    self.behindParent = behindParent
    
    # Item position
    if position is not None and isinstance(position, (tuple, list, complex)):
      self.position:point = self.point(position)

    elif x is None or y is None:
      raise AttributeError("Item position must be specified, either with 'position' or with 'x' and 'y'.")
      
    else:
      self.position:point = self.point(x,y)

    self.center_of_rotation:point = self.point(center_of_rotation)
    self.orientation = orientation
    self.scale = scale
    self.zvalue = zvalue
    self.draggable = draggable

# ────────────────────────────────────────────────────────────────────────
  def point(self, x, y=None):
    ''' 
    Point in absolute coordinates
    '''

    # ─── Input heterogeneity

    if y is None:

      if isinstance(x, complex):

        # Convert from complex coordinates
        y = np.imag(x)
        x = np.real(x)

      else:

        # Doublet input
        y = x[1]
        x = x[0]  

    # ─── Check parenthood, i.e. convert realtive positions to absolute

    if self.parent is not None:

      x += self.parent.position.x
      y += self.parent.position.y

    return point(x, y)

  # ────────────────────────────────────────────────────────────────────────
  def initialize(self):
    '''
    Initialize the item
    '''

    # ─── Set boundaries for all points

    self.position.boundaries = self.canva.boundaries
    self.center_of_rotation.boundaries = self.canva.boundaries

    # ─── Styling

    if isinstance(self, hasColor): self.setColor()
    if isinstance(self, hasStroke): self.setStroke()

    # ─── Set as initialized

    self.is_initialized = True

  # ════════════════════════════════════════════════════════════════════════
  #                              GETTERS
  # ════════════════════════════════════════════════════════════════════════

  # ────────────────────────────────────────────────────────────────────────
  def Lx(self):
    return self.boundingRect().width()

  # ────────────────────────────────────────────────────────────────────────
  def Ly(self):
    return self.boundingRect().height()

  # ════════════════════════════════════════════════════════════════════════
  #                              SETTERS
  # ════════════════════════════════════════════════════════════════════════

  # ────────────────────────────────────────────────────────────────────────
  # def put(self):
  #   '''
  #   Place the item in the scene

  #   TO BE OVERLOADED for each item
  #   '''
  #   pass

  #   # # Wait for initialization
  #   # if not self.is_initialized: return

  #   # # Get absolute coordinates
  #   # x, y = self.absoluteCoordinates()

  #   # # Place on the canva
  #   # self.setPos(x, self.canva.boundaries.y1 - y)

  #   # print(self._orientation)
  #   # self.setRotation(self._orientation)

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
  def parent(self): return self.parentItem()

  @parent.setter
  def parent(self, parent):

    # #  _parent attribute

    # if isinstance(parent, str):

    #   if not self.is_initialized:
    #     self._parent = parent
    #     return
      
    #   self._parent = self.canva.item[parent]

    # else:
    #   self._parent = parent

    # if self.is_initialized:

    self.setParentItem(parent)

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
  def x(self): return self._position.x

  @x.setter
  def x(self, v):
    self._position.x = v
    # self.put()

  @property
  def y(self): return self._position.y

  @x.setter
  def y(self, v):
    self._position.y = v
    # self.put()

  @property
  def position(self): return self._position

  @position.setter
  def position(self, pos):    
    self._position = pos
    # self.put()

  # ─── Center of rotation ─────────────────────────────────────────────────
  
  ''' The position of the item's transformation point (origin) '''

  @property
  def center_of_rotation(self): return self._center_of_rotation

  @center_of_rotation.setter
  def center_of_rotation(self, pt):
    
    # Store transform point
    self._center_of_rotation = pt

  # ─── Orientation ────────────────────────────────────────────────────────
  
  ''' The item's orientation '''

  @property
  def orientation(self): return -self._orientation*np.pi/180

  @orientation.setter
  def orientation(self, angle):
    self._orientation = -angle*180/np.pi

    # Update orientation
    if self.is_initialized:
      self.setRotation(self._orientation)

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
  def __init__(self, color=None):

    super().__init__()

    # Assign color
    self._color = color

  # ────────────────────────────────────────────────────────────────────────
  def setColor(self):
    '''
    Color styling

    This function does not take any argument, instead it applies the color
    styling defined by the color attribute.
    '''

    if isinstance(self, QAbstractGraphicsShapeItem) and self._color is not None:
      self.setBrush(QBrush(QColor(self._color)))

  # ─── color ──────────────────────────────────────────────────────────────

  @property
  def color(self): return self._color

  @color.setter
  def color(self, C):
    self._color = C
    self.setColor()

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

  # ────────────────────────────────────────────────────────────────────────
  def setStroke(self):
    '''
    Stroke styling

    This function does not take any argument, instead it applies the stroke
    style defined by the attributes.
    '''

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

  # ─── stroke ─────────────────────────────────────────────────────────────

  @property
  def stroke(self): return self._stroke

  @stroke.setter
  def stroke(self, s):
    self._stroke = s
    self.setStroke()

  # ─── thickness ──────────────────────────────────────────────────────────

  @property
  def thickness(self): return self._thickness

  @thickness.setter
  def thickness(self, t):
    self._thickness = t
    self.setStroke()

  # ─── linestyle ──────────────────────────────────────────────────────────

  @property
  def linestyle(self): return self._linestyle

  @linestyle.setter
  def linestyle(self, s):
    self._linestyle = s
    self.setStroke()