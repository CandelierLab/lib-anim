import numpy as np

from PyQt6.QtCore import QRectF
from PyQt6.QtWidgets import QGraphicsEllipseItem

from .item import item, hasColor, hasStroke
from .events import event

# ══════════════════════════════════════════════════════════════════════════
#                                 CIRCLE
# ══════════════════════════════════════════════════════════════════════════
   
class circle(item, hasColor, hasStroke):
  '''
  A circle item is defined by its:

  - radius
  - position of the point of reference
  - styling
  
  Parameters
  ══════════

    * name       
        str
        The circle's name

    * group
        anim.plane.group
        default: None
        The circle's group. If None, the position of the reference point is
        in absolute coordinates. Otherwise, the position is relative to the
        group's reference point.

    ─── size ────────────────────────────────────

    * radius
        float
        The circle's radius.

    ─── position ────────────────────────────────

    * x           
        float
        default: 0
        x-position of the center point.

    * y
        float
        default: 0
        y-position of the center point.

    * position
        (float, float), [float, float], complex
        default: [0,0]
        Position of the center point. The user can define either x, y or
        the position. In case of conflict, the position attribute wins.

    ─── transformations ─────────────────────────

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
        Z-value (stack order) of the circle.
    
    ─── style ────────────────────────────────

    * color
        None, str, QColor
        default: 'grey'
        Fill color. None stands for transparency.

    * stroke
        None, str, QColor
        default: None
        Stroke color. None stands for transparency.

    * thickness
        float
        default: 0
        Stroke thickness, in scene units. When it is equal to 0, the stroke
        has the minimal thickness of 1 pixel.

    * linestyle
        'solid'/'-', 'dash'/'--', 'dot'/'..'/':', 'dashdot'/'-.'
        default: '-'
        Stroke style.
  '''

  # ────────────────────────────────────────────────────────────────────────
  def __init__(self, 
               radius,
               color = 'grey',
               stroke = None,
               thickness = 0,
               linestyle = '-',
               group = None,
               x = 0,
               y = 0,
               position = None,
               zvalue = 0,
               draggable = False):
    '''
    Circle item constructor
    '''  

    # Parent constructors
    item.__init__(self, 
                  group = group,
                  x = x,
                  y = y,
                  position = position,
                  zvalue = zvalue,
                  draggable = draggable)
    
    hasColor.__init__(self, color = color)
    hasStroke.__init__(self,
                       stroke = stroke,
                       thickness = thickness,
                       linestyle = linestyle)

    # ─── Internal properties

    self.radius = radius

    # ─── QGraphicsItem

    class QCircle(QGraphicsEllipseItem, event): pass
    self.qitem = QCircle()

  # ────────────────────────────────────────────────────────────────────────
  def initialize(self):
    '''
    Initialize the circle

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
    Set the circle's geometry
    '''

    # Check qitem
    if self.qitem is None: return

    # Set geometry
    self.qitem.setRect(QRectF(-self.radius*self.ppu,
                              -self.radius*self.ppu,
                              2*self.radius*self.ppu,
                              2*self.radius*self.ppu))

  # ─── radius ─────────────────────────────────────────────────────────────
  
  @property
  def radius(self): return self._radius

  @radius.setter
  def radius(self, r):

    self._radius = abs(r)
    
    # Set geometry
    self.setGeometry()