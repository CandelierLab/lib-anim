import numpy as np

from .item import item
from .group import composite
from .path import path
from .polygon import polygon
from .circle import circle
from .text import text

class arrow(composite):
  '''
  Arrow item (composite)

  An arrow is defined by its:

    - points (the point of reference is the first point)
    - head
    - text (optional)
    - styling
    
  Parameters
  ══════════

    * name       
        str
        The arrow's name

    * head_shape
        'dart', 'circle'
        default: 'dart'
        The arrow head shape.

    * string
        str, [*  str(*)]
        default: ''
        The arrow text's string. HTML formatting is supported by default.

    * group
        anim.plane.group
        default: None
        The arrow's group. If None, the position of the reference point is in
        absolute coordinates. Otherwise, the positions are relative to the
        group's reference point.

    ─── positions ───────────────────────────────

    * points
        [(float, float)], [[float, float]], [complex]
        Positions of the arrow points.

    * head_segment
        int
        default: -1
        Path segment where the arrowhead stands

    * head_location
        float ∈ [0,1]
        default: 1
        Location of the arrowhead on the specified path segment

    ─── transformations ─────────────────────────

    * draggable
        bool
        default: False
        Boolean specifying if the arrow can be dragged. If True, the dragging
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
        Arrow color. None stands for transparency.

    * thickness
        float
        default: 0.005
        Arrow line thickness, in scene units. When it is equal to 0, the stroke
        has the minimal thickness of 1 pixel.

    * linestyle
        'solid'/'-', 'dash'/'--', 'dot'/'..'/':', 'dashdot'/'-.'
        default: '-'
        Line style.
  '''

  # ────────────────────────────────────────────────────────────────────────
  def __init__(self, 
               points,
               head_shape = 'dart',
               head_segment = -1,
               head_location = 1,
               string = '',
               color = 'grey',
               thickness = 0.005,
               linestyle = '-',
               group = None,
               zvalue = 0,
               draggable = False):
    '''
    Arrow item constructor
    '''  

    # ─── Parent constructor
    
    super().__init__(group = group,
                     position = points[0],
                     zvalue = zvalue,
                     draggable = draggable)
    
    # ─── Properties

    self._color = color
    self.init_string = string
    self._points = points

    self.head_shape = head_shape
    
  # ────────────────────────────────────────────────────────────────────────
  def initialize(self):
    '''
    Initialize the item

    At this point:
    - the canva should be defined (automatically managed by itemDict)
    - the qitem should be defined (managed by the children class)
    '''

    # Parent constructor
    super().initialize()

    # ─── Child items (for composite items) ─────

    # ─── Path

    self.subitem.path = path(
      group = self,
      points = [[p[0]-self.position.x, p[1]-self.position.y] for p in self._points],
      stroke = self.color
    )

    # ─── Arrowhead

    match self.head_shape:

      case 'dart':

        pts = np.array([[0,0], [0.1,0], [0,0.1]])

        self.subitem.head = polygon(
          group = self,
          points = pts
        )

      case 'disk':

        pass
        # self.animation.item[self.head] = anim.plane.circle(self.animation, self.head,
        #   parent = self.name,
        #   position = [0,0],
        #   radius = 0)

    # # ─── String

    # self.subitem.string = text(
    #   group = self,
    #   string = self.init_string
    # )

    # ─── Update geometry ───────────────────────

    # self.setGeometry()

  # # ────────────────────────────────────────────────────────────────────────
  # def setGeometry(self):
  #   '''
  #   Sets the elements geometry
  #   '''

  #   # Check qitem
  #   if self.qitem is None: return 

  #   # Group positionning
  #   super().setGeometry()


  # ─── points ─────────────────────────────────────────────────────────────
  
  @property
  def points(self): return self.subitem.path.points

  @points.setter
  def points(self, P): 

    self._points = P

    # Set reference point
    self.position = self._points[0]

    # Path points
    self.subitem.path.points = [[p[0]-self.position.x, p[1]-self.position.y] for p in self._points]

  # ─── string ─────────────────────────────────────────────────────────────
  
  @property
  def string(self): 
    # print(self.subitem)
    return self.subitem.string.string

  @string.setter
  def string(self, s): 
    self.subitem.string.string = s

  # ─── color ──────────────────────────────────────────────────────────────
  
  @property
  def color(self): return self._color

  @color.setter
  def color(self, c):
    self._color = c