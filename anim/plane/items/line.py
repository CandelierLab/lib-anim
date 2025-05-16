from PyQt6.QtGui import QPainterPath
from PyQt6.QtWidgets import QGraphicsLineItem

from ..geometry import point

from .item import item, hasStroke

# ══════════════════════════════════════════════════════════════════════════
#                                 LINE
# ══════════════════════════════════════════════════════════════════════════

class line(item, hasStroke):
  '''
  A line item is defined by its:

  - points (the point of reference is the first point)
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

    ─── positions ───────────────────────────────

    * points
        [(float, float)], [[float, float]], [complex]
        Positions of the line points.

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
               points,
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
                  position = points[0],
                  center_of_rotation = [0,0],
                  orientation = 0,
                  zvalue = zvalue,
                  draggable = draggable)
    
    hasStroke.__init__(self,
                       stroke = color,
                       thickness = thickness,
                       linestyle = linestyle)

    
    # ─── Internal properties

    self.points = points

    # ─── QGraphicsItem

    self.qitem = QGraphicsLineItem()

    # ─── Initialization

    self.initialize()

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

    self.qitem.setLine(self.points[0].x, self.points[0].y,
                       self.points[1].x, self.points[1].y)

  # ─── points ─────────────────────────────────────────────────────────────
  
  @property
  def points(self): return self._points

  @points.setter
  def points(self, P):

    self._points = [point(p) for p in P]
    
    # Set geometry
    self.setGeometry()

  # ─── color ──────────────────────────────────────────────────────────────
  
  @property
  def color(self): return self._stroke

  @color.setter
  def color(self, c): self.stroke = c
