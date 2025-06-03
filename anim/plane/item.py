'''
Generic item
'''

import numpy as np

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPen, QBrush
from PyQt6.QtWidgets import QAbstractGraphicsShapeItem, QGraphicsItem, QGraphicsLineItem, QGraphicsTextItem

from .canva import canva
from .geometry import vector, position as geom_position

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
               zvalue = 0,
               draggable = False):
    '''
    Constructor
    '''

    # ─── Definitions

    # Reference canva
    self.canva:canva = None
    self.ppu = 1

    # QGraphicsItem
    self.qitem:QGraphicsItem = None

    # Assign name
    self.name = None

    # ─── Default internal properties

    self._group = group
    
    # Item position
    if position is not None and isinstance(position, (tuple, list, complex)):
      self._position:geom_position = geom_position(position)

    elif x is None or y is None:
      raise AttributeError("Item position must be specified, either with 'position' or with 'x' and 'y'.")
      
    else:
      self._position:geom_position = geom_position(x,y)

    # Center of rotation
    self.center_of_rotation = center_of_rotation

    self._orientation = orientation
    self._zvalue = zvalue
    self._draggable = draggable

  # ────────────────────────────────────────────────────────────────────────
  def initialize(self):
    '''
    Initialize the item

    This method is meant to be overloaded and called.
    At this point:
    - the canva should be defined (automatically managed by itemDict)
    - the qitem should be defined (managed by the children class)
    '''

    # Add item
    self.qitem.item = self

    # Pixels per unit
    self.ppu = float(self.canva.pixelperunit)

    #  Group
    self.group = self._group

    # Position
    self.setPosition()

    # Orientation
    self.setOrientation()

    # Style
    if isinstance(self, hasColor): self.setColor()
    if isinstance(self, hasStroke): self.setStroke()

    # Z-value
    self.zvalue = self._zvalue

    # Draggability
    if self._draggable:
      self.draggable = self._draggable

  # ════════════════════════════════════════════════════════════════════════
  #                              GETTERS
  # ════════════════════════════════════════════════════════════════════════

  # ────────────────────────────────────────────────────────────────────────
  def Lx(self):
    return self.qitem.boundingRect().width()/self.ppu

  # ────────────────────────────────────────────────────────────────────────
  def Ly(self):
    return self.qitem.boundingRect().height()/self.ppu

  # ════════════════════════════════════════════════════════════════════════
  #                              SETTERS
  # ════════════════════════════════════════════════════════════════════════

  # ────────────────────────────────────────────────────────────────────────
  def setPosition(self, position=None):
    '''
    Sets the qitem's position.
    '''

    # Place on the canva
    if self.qitem is None: return

    if position is None: position = self._position

    self.qitem.setPos(position.x*self.ppu, 
                      position.y*self.ppu)
    
  # ────────────────────────────────────────────────────────────────────────
  def setOrientation(self):
    '''
    Set the qitem orientation
    '''

    # Check qitem
    if self.qitem is None: return

    # Set orientation
    self.qitem.setTransformOriginPoint(
      self.center_of_rotation.x*self.ppu,
      self.center_of_rotation.y*self.ppu)
          
    self.qitem.setRotation(self._orientation*180/np.pi)
    
  # ════════════════════════════════════════════════════════════════════════
  #                             TRANSFORMATIONS
  # ════════════════════════════════════════════════════════════════════════

  # ────────────────────────────────────────────────────────────────────────
  def translate(self, dx, dy=None):
    '''
    Relative translation

    Displaces the item of relative amounts.
    
    Attributes:
      dx (float): :math:`x`-coordinate of the displacement. It can also be a 
        doublet [`dx`,`dy`], or a complex number. In this case the *dy* 
        argument is overridden.
      dy (float): :math:`y`-coordinate of the displacement.
    '''

    # Translation vector
    v = vector(dx, dy)

    # Update position
    self.x += v.x
    self.y += v.y

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
  #                             PROPERTIES
  # ════════════════════════════════════════════════════════════════════════

  # ─── Group ──────────────────────────────────────────────────────────────
  
  ''' The item's group '''

  @property
  def group(self): return self._group

  @group.setter
  def group(self, group):

    # Set group
    self._group = group

    if self.qitem is not None and \
       group is not None and \
       group.qitem is not None:

      # Add to group
      group.qitem.addToGroup(self.qitem)
      
      # Set relative position
      self.position.absolute = False

      # Switch to relative coordinates
      self.setPosition()

  # ─── Position ───────────────────────────────────────────────────────────
  
  ''' The position of the item's reference point '''

  @property
  def x(self): return self._position.x

  @x.setter
  def x(self, v):
    self._position.x = v
    self.setPosition()

  @property
  def y(self): return self._position.y

  @x.setter
  def y(self, v):
    self._position.y = v
    self.setPosition()

  @property
  def position(self): return self._position

  @position.setter
  def position(self, pt):

    # Set point
    v = vector(pt)
    self._position.x = v.x
    self._position.y = v.y

    # Update position
    self.setPosition()

  # ─── Center of rotation ─────────────────────────────────────────────────
  
  ''' The item's center of rotation '''

  @property
  def center_of_rotation(self): return self._center_of_rotation

  @center_of_rotation.setter
  def center_of_rotation(self, pt):

    # Set point    
    self._center_of_rotation = geom_position(pt)

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

    if self._color is not None:

      if isinstance(self._color, (tuple, list)):
        qcolor = QColor(int(self._color[0]*255),
                        int(self._color[1]*255),
                        int(self._color[2]*255))
      else:
        qcolor = QColor(self._color)

      if isinstance(self.qitem, QAbstractGraphicsShapeItem):
        self.qitem.setBrush(QBrush(qcolor))

      if isinstance(self.qitem, QGraphicsTextItem):
        self.qitem.setDefaultTextColor(qcolor)

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

      if self._stroke is None:

        # Transparent stroke
        self.qitem.setPen(QPen(Qt.PenStyle.NoPen))

      else:

        Pen = QPen()

        #  Color
        Pen.setColor(QColor(self._stroke))

        # Thickness
        if self._thickness is not None:
          Pen.setWidthF(self._thickness*self.ppu)

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