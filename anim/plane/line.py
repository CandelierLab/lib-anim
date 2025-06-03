import numpy as np

from PyQt6.QtWidgets import QGraphicsLineItem

from .item import item, hasStroke
from .events import event

# ══════════════════════════════════════════════════════════════════════════
#                                 LINE
# ══════════════════════════════════════════════════════════════════════════

class line(item, hasStroke):
  '''
  A line item is defined by:

  - position of the point of reference
  - dimensions (Lx and Ly)
  - styling
  
  Parameters
  ══════════

    * name       
        str
        The line's name

    * group
        anim.plane.group
        default: None
        The line's group. If None, the position of the reference point is in
        absolute coordinates. Otherwise, the positions are relative to the
        group's reference point.

    ─── position ────────────────────────────────

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

    * center
        bool
        default: False
        Boolean defining the centering around the reference point.

    ─── dimensions ──────────────────────────────

    * Lx          
        float
        The line's width, i.e. length along the x axis when orientation
        is 0. 

    * Ly
        float
        The line's height, i.e.length along the y axis when orientation
        is 0.

    * dimension
        (float, float), [float, float], complex
        default: [0,0]
        Dimensions along the x and y axes when orientation is 0. The user
        must define either Lx, Ly or the dimension array. In case of
        conflicting definitions, the dimension attribute wins.

    ─── transformations ─────────────────────────

    * orientation
        float
        default: 0, unit: radians
        Orientation of the rectangle, with respect to the positive part of the 
        x-axis.

    * draggable
        bool
        default: False
        Boolean specifying if the item can be dragged. If True, the dragging
        callback is defined in the 'itemChange' method of the event class,
        which is transfered to the canva's 'event' method (recommended).

    ─── stack ───────────────────────────────────

    * zvalue
        float
        default: 0
        Z-value (stack order) of the line.
    
    ─── style ────────────────────────────────

    * color
        None, str, QColor
        default: 'grey'
        Line color. None stands for transparency.

    * thickness
        float
        default: 0.005
        Line thickness, in scene units. When it is equal to 0, the stroke
        has the minimal thickness of 1 pixel.

    * linestyle
        'solid'/'-', 'dash'/'--', 'dot'/'..'/':', 'dashdot'/'-.'
        default: '-'
        Line style.
  '''

  # ────────────────────────────────────────────────────────────────────────
  def __init__(self,
               x = 0,
               y = 0,
               position = None,
               Lx = None,
               Ly = None,
               dimension = None,
               orientation = 0,
               center = False,
               color = 'grey',
               thickness = 0.005,
               linestyle = '-',
               group = None,
               zvalue = 0,
               draggable = False):
    '''
    Path item constructor
    '''  

    # ─── Parent constructors

    item.__init__(self, 
                  group = group,
                  x = x,
                  y = y,
                  position = position,
                  center_of_rotation = [0,0],
                  orientation = orientation,
                  zvalue = zvalue,
                  draggable = draggable)
    
    hasStroke.__init__(self,
                       stroke = color,
                       thickness = thickness,
                       linestyle = linestyle)

    
    # ─── Internal properties

    self._Lx = None
    self._Ly = None 
    self._center = center 

    # ─── Line attributes

    if dimension is not None and isinstance(dimension, (tuple, list, complex)):
      self.dimension = dimension

    elif Lx is None or Ly is None:
      raise AttributeError("Line dimensions must be specified, either with 'dimension' or with 'Lx' and 'Ly'.")
      
    else:
      self.Lx = Lx
      self.Ly = Ly

    # ─── QGraphicsItem

    class QLine(QGraphicsLineItem, event): pass
    self.qitem = QLine()

  # ────────────────────────────────────────────────────────────────────────
  def initialize(self):
    '''
    Initialize the line

    At this point:
    - the canva should be defined (automatically managed by itemDict)
    - the qitem should be defined (managed by the children class)
    '''

    # Parent initialization
    item.initialize(self)

    # Initialization specifics
    self.setGeometry()
    
  # ────────────────────────────────────────────────────────────────────────
  def setGeometry(self):
    '''
    Set the line geometry
    '''

    # Check qitem
    if self.qitem is None: return

    # Rectangle bottom-left corner
    x0 = -self.Lx/2 if self._center else 0
    y0 = -self.Ly/2 if self._center else 0

    self.qitem.setLine(x0*self.ppu,
                       y0*self.ppu,
                       (x0 + self.Lx)*self.ppu,
                       (y0 + self.Ly)*self.ppu)

  # ─── width ──────────────────────────────────────────────────────────────
  
  @property
  def Lx(self): return self._Lx

  @Lx.setter
  def Lx(self, w):

    self._Lx = w
    
    # Set geometry
    self.setGeometry()
  
  # ─── height ─────────────────────────────────────────────────────────────

  @property
  def Ly(self): return self._Ly

  @Ly.setter
  def Ly(self, h):

    self._Ly = h
    
    # Set geometry
    self.setGeometry()   

  # ─── dimensions ─────────────────────────────────────────────────────────
  
  @property
  def dimension(self): return [self._Lx, self._Ly]

  @dimension.setter
  def dimension(self, D):
    
    if isinstance(D, complex):

      # Convert from complex coordinates
      self._Lx = np.real(D)
      self._Ly = np.imag(D)

    else:

      # Doublet input
      self._Lx = D[0]
      self._Ly = D[1]

    # Set geometry
    self.setGeometry()

  # ─── center ─────────────────────────────────────────────────────────────

  @property
  def center(self): return self._center

  @center.setter
  def center(self, C):

    self._center = C

    # Set geometry
    self.setGeometry()

  # ─── color ──────────────────────────────────────────────────────────────
  
  @property
  def color(self): return self._stroke

  @color.setter
  def color(self, c): self.stroke = c
