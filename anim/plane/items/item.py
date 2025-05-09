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

'''
May be useful sometimes:

- Stack the item behing its parent:
  self.qitem.setFlag(QGraphicsItem.GraphicsItemFlag.ItemStacksBehindParent, b)
'''

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

    * group
        anim.plane.group
        default: None
        The item's group. If None, the position of the reference point and
        center of rotation are in absolute coordinates. Otherwise, the
        position is relative to the group's reference point.

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
        float, (float, float), [float, float], complex
        default: [1,1]
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
  
    * Lx(): return the item width
    * Ly(): return the item height
  '''

  # ────────────────────────────────────────────────────────────────────────
  def __init__(self, 
               group = None,
               x = 0,
               y = 0,
               position = None,
               center_of_rotation = [0,0],
               orientation = 0,
               scale = [1,1],
               zvalue = 0,
               draggable = False):
    '''
    Constructor
    '''

    # ─── Definitions

    # Reference canva
    self.canva:canva = None

    # QGraphicsItem
    self.qitem:QGraphicsItem = None

    # Assign name
    self.name = None

    # ─── Internal properties

    self._group = group
    
    # Item position
    if position is not None and isinstance(position, (tuple, list, complex)):
      self._position:point = self.point(position)

    elif x is None or y is None:
      raise AttributeError("Item position must be specified, either with 'position' or with 'x' and 'y'.")
      
    else:
      self._position:point = self.point(x,y)

    self._center_of_rotation:point = self.point(center_of_rotation)
    self._orientation = orientation
    self._scale = scale
    self._zvalue = zvalue
    self._draggable = draggable

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

    return point(x, y)

  # ────────────────────────────────────────────────────────────────────────
  def initialize(self):
    '''
    Initialize the item

    This method is meant to be overloaded and called.
    At this point:
    - the canva should be defined (automatically managed by itemDict)
    - the qitem should be defined (managed by the children class)
    '''

    # ─── Set boundaries for all points

    self.position.boundaries = self.canva.boundaries
    self.center_of_rotation.boundaries = self.canva.boundaries

    # ─── Group

    self.group = self._group

    # ─── Geometry and orientation

    self.setGeometry()
    self.setOrientation()

    # ─── Styling

    if isinstance(self, hasColor): self.setColor()
    if isinstance(self, hasStroke): self.setStroke()

    # ─── Draggability

    self.draggable = self._draggable

  # ════════════════════════════════════════════════════════════════════════
  #                              GETTERS
  # ════════════════════════════════════════════════════════════════════════

  # ────────────────────────────────────────────────────────────────────────
  def Lx(self):
    return self.qitem.boundingRect().width()

  # ────────────────────────────────────────────────────────────────────────
  def Ly(self):
    return self.qitem.boundingRect().height()

  # ════════════════════════════════════════════════════════════════════════
  #                              SETTERS
  # ════════════════════════════════════════════════════════════════════════

  # ────────────────────────────────────────────────────────────────────────
  def setGeometry(self):
    '''
    Sets the qitem's geometry

    TO BE OVERLOADED
    '''
    
  # ────────────────────────────────────────────────────────────────────────
  def setOrientation(self):
    '''
    Sets the item's orientation
    '''

    # Check qitem
    if self.qitem is None: return

    # Set orientation
    # self.qitem.setTransformOriginPoint(self.center_of_rotation.X + self.position.X,
    #                                    self.center_of_rotation.Y - self.position.Y)
    
    self.qitem.setTransformOriginPoint(self.center_of_rotation.X,
                                       self.center_of_rotation.Y)
      
    self.qitem.setRotation(-self._orientation*180/np.pi)
    
  # ════════════════════════════════════════════════════════════════════════
  #                               MOTION
  # ════════════════════════════════════════════════════════════════════════

  # ────────────────────────────────────────────────────────────────────────
  def translate(self, dx=0, dy=0, z=None):
    '''
    Relative translation

    Displaces the item of relative amounts.
    
    Attributes:
      dx (float): :math:`x`-coordinate of the displacement. It can also be a 
        doublet [`dx`,`dy`], in this case the *dy* argument is overridden.
      dy (float): :math:`y`-coordinate of the displacement.
      z (float): A complex number :math:`z = dx+jdy`. Specifying ``z``
        overrides the ``x`` and ``y`` arguments.
    '''

    if z is not None:

      # Convert from complex coordinates
      dx = np.real(z)
      dy = np.imag(z)

    elif isinstance(dx, (tuple, list)):

      # Doublet input
      dy = dx[1]
      dx = dx[0]  

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

  # ─── Group ──────────────────────────────────────────────────────────────
  
  ''' The item's group '''

  @property
  def group(self): return self._group

  @group.setter
  def group(self, group):

    self._group = group

    if self.qitem is not None and \
       group is not None and \
       group.qitem is not None:

      # Add to group
      group.qitem.addToGroup(self.qitem)

      # Switch to relative coordinates
      self.position.shift[0] = group.position.x
      self.position.shift[1] = group.position.y
      self.center_of_rotation.shift[0] = group.position.x
      self.center_of_rotation.shift[1] = group.position.y

  # ─── Position ───────────────────────────────────────────────────────────
  
  ''' The position of the item's reference point '''

  @property
  def x(self): return self._position.x

  @x.setter
  def x(self, v):
    self._position.x = v
    self.setGeometry()

  @property
  def y(self): return self._position.y

  @x.setter
  def y(self, v):
    self._position.y = v
    self.setGeometry()

  @property
  def position(self): return self._position

  @position.setter
  def position(self, pt):

    # Set point
    self._position = self.point(pt)
    if self.canva is not None:
      self._position.boundaries = self.canva.boundaries

    # Update geometry
    self.setGeometry()

  # ─── Center of rotation ─────────────────────────────────────────────────
  
  ''' The item's center of rotation '''

  @property
  def center_of_rotation(self): return self._center_of_rotation

  @center_of_rotation.setter
  def center_of_rotation(self, pt):

    # Set point
    self._center_of_rotation = self.point(pt)
    if self.canva is not None: 
      self._center_of_rotation.boundaries = self.canva.boundaries

    # Update orientation
    self.setOrientation()  

  # ─── Orientation ────────────────────────────────────────────────────────
  
  ''' The item's orientation '''

  @property
  def orientation(self): return self._orientation

  @orientation.setter
  def orientation(self, angle):
    self._orientation = angle

    # Update orientation
    self.setOrientation()      

  # ─── Scale ──────────────────────────────────────────────────────────────
  
  ''' The item's scale '''

  @property
  def scale(self): return self._scale

  @scale.setter
  def scale(self, scale):

    if isinstance(scale, numbers.Number):
      scale = [scale, scale]

    self._scale = list(scale)

    if self.qitem is not None:
      self.qitem.setTransform(QTransform.fromScale(scale[0], scale[1]), True)

  # ─── z-value ────────────────────────────────────────────────────────────

  ''' The item's stack position '''

  @property
  def zvalue(self): return self._zvalue

  @zvalue.setter
  def zvalue(self, z):

    self._zvalue = z

    if self.qitem is not None:
      self.qitem.setZValue(self._zvalue)

  # ─── Draggability ───────────────────────────────────────────────────────
  
  ''' The item's draggability '''

  @property
  def draggable(self): return self._draggable

  @draggable.setter
  def draggable(self, bdrag):
    
    self._draggable = bdrag

    if self.qitem is not None:
      self.qitem.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, self._draggable)
      self.qitem.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges, self._draggable)

      if self._draggable:
        self.qitem.setCacheMode(QGraphicsItem.CacheMode.DeviceCoordinateCache)
      
# ══════════════════════════════════════════════════════════════════════════
#                        ITEMS WITH SPECIFIC PROPERTIES
# ══════════════════════════════════════════════════════════════════════════

# ══════════════════════════════════════════════════════════════════════════
class hasColor:

  # ────────────────────────────────────────────────────────────────────────
  def __init__(self, color=None):

    # super().__init__()

    # Hints
    self.qitem:QAbstractGraphicsShapeItem

    # Assign color
    self._color = color

  # ────────────────────────────────────────────────────────────────────────
  def setColor(self):
    '''
    Color styling

    This function does not take any argument, instead it applies the color
    styling defined by the color attribute.
    '''

    if isinstance(self.qitem, QAbstractGraphicsShapeItem) and self._color is not None:
      self.qitem.setBrush(QBrush(QColor(self._color)))

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

    # super().__init__()

    # Hints
    self.qitem:QAbstractGraphicsShapeItem|QGraphicsLineItem

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

    if isinstance(self.qitem, (QAbstractGraphicsShapeItem, QGraphicsLineItem)):

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
      
      self.qitem.setPen(Pen)

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