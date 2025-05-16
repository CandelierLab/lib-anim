from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import QPolygonF
from PyQt6.QtWidgets import QGraphicsPolygonItem

from ..geometry import point

from .item import item, hasColor, hasStroke

# ══════════════════════════════════════════════════════════════════════════
#                                POLYGON
# ══════════════════════════════════════════════════════════════════════════

class polygon(item, hasColor, hasStroke):
  '''
  A polygon item is defined by its:

  - points (the point of reference is the first point)
  - styling
  
  Parameters
  ══════════

    * name       
        str
        The polygon's name

    * group
        anim.plane.group
        default: None
        The polygon's group. If None, the position of the reference point is in
        absolute coordinates. Otherwise, the positions are relative to the
        group's reference point.

    ─── positions ───────────────────────────────

    * points
        [(float, float)], [[float, float]], [complex]
        Positions of the polygon points.

    ─── transformations ─────────────────────────

    * orientation
        float
        default: 0, unit: radians
        Orientation of the polygon, with respect to the positive part of the 
        x-axis.

    * center_of_rotation
        (float, float), [float, float], complex
        default: None
        Center point for the rotation, relative to the reference point.

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
        Z-value (stack order) of the polygon.
    
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
        default: 0.005
        Stroke thickness, in scene units. When it is equal to 0, the stroke
        has the minimal thickness of 1 pixel.

    * linestyle
        'solid'/'-', 'dash'/'--', 'dot'/'..'/':', 'dashdot'/'-.'
        default: '-'
        Stroke style.
  '''

  # ────────────────────────────────────────────────────────────────────────
  def __init__(self, 
               points,
               color = 'grey',
               stroke = None,
               thickness = 0.005,
               linestyle = '-',
               group = None,
               center_of_rotation = [0,0],
               orientation = 0,
               zvalue = 0,
               draggable = False):
    '''
    Path item constructor
    '''  

    # ─── Parent constructors

    item.__init__(self, 
                  group = group,
                  position = points[0],
                  center_of_rotation = center_of_rotation,
                  orientation = orientation,
                  zvalue = zvalue,
                  draggable = draggable)
    
    hasColor.__init__(self, color = color)

    hasStroke.__init__(self,
                       stroke = stroke,
                       thickness = thickness,
                       linestyle = linestyle)
    
    # ─── Internal properties

    self.points = points

    # ─── QGraphicsItem

    self.qitem = QGraphicsPolygonItem()

    # ─── Initialization

    self.initialize()

  # ────────────────────────────────────────────────────────────────────────
  def initialize(self):
    '''
    Initialize the path

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
    Set the path geometry
    '''

    # Check qitem
    if self.qitem is None: return

    self.qitem.setPolygon(QPolygonF([QPointF(p.x, p.y) for p in self.points]))

  # ─── points ─────────────────────────────────────────────────────────────
  
  @property
  def points(self): return self._points

  @points.setter
  def points(self, P):

    self._points = [point(p) for p in P]
    
    # Set geometry
    self.setGeometry()
