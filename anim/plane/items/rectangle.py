from PyQt6.QtCore import QRectF
from PyQt6.QtWidgets import QGraphicsItem, QGraphicsRectItem

from .item import item, hasColor, hasStroke

# ══════════════════════════════════════════════════════════════════════════
#                                 RECTANGLE
# ══════════════════════════════════════════════════════════════════════════

class rectangle(item, hasColor, hasStroke, QGraphicsRectItem):
  '''
  A rectangle item is defined by its:

  - dimensions (width and height)
  - position of the point of reference
  - horizontal and vertical centering, with respect to the point of
      reference. The defaut centering is (True,True), while (False,False)
      defines the reference as the top-left corner. One can also use a single
      value to set both at the same time.
  
  Parameters
  ══════════

    * name        (str)             The rectangle's name
    * parent      (*QGraphicsItem*) The rectangle's parent item

    ─── dimensions ──────────────────────────────

    * width       (str)             The rectangle's width
    * height      (*QGraphicsItem*) The rectangle's height

    ─── position & transformations ──────────────

    * x           (float)           x-position of the reference point. Default: 0
    * y           (float)           y-position of the reference point. Default: 0
    * position    ([float, float])  Position of the reference point. Default: [0,0]
                                      The user can define either x and y or the position.

    * center  ([bool, bool] / bool) Centering around the reference point. Default: [True,True]
    * orientation (float)           Orientation of the item (rad). Default: 0
    * scale       (float)           Scaling factor. Default: None
    * transformPt ([float, float])  Origin of the transformation
    * draggable   (bool)            Boolean specifying if the item can be 
                                      dragged. If True, the dragging callback
                                      is defined in the ... method. 
                                      Default: False.

    ─── stack ───────────────────────────────────

    * zvalue      (float)           Z-value (stack order) of the item. Default: 1
    * behindParent (bool)           Boolean specifying if the item is behind
                                      its parent or not. Default: None
    
    ─── style ────────────────────────────────

    * fill        (str / QColor)    Fill color. None stands for transparency. Default: None
    * stroke      (str / QColor)    Stroke color. None stands for transparency. Default: 'gray'
    * thickness   (float)           Stroke thickness, in scene units. Default: 0.001.
    * linestyle   (str)             Stroke style. Can have any value among 'solid' (default),
                                      'dash' (or '--'), 'dot' (or '..' or ':'), dashdot' (or '-.').
  '''

  # ────────────────────────────────────────────────────────────────────────
  def __init__(self, 
               width,
               height,
               center = (True, True),
               color = None,
               stroke = None,
               thickness = 0,
               linestyle = '-',
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
    Rectangle item constructor
    '''  

    # Parent constructors
    item.__init__(self, 
                  parent = parent,
                  behindParent = behindParent,
                  x = x,
                  y = y,
                  position = position,
                  transformPt = transformPt,
                  orientation = orientation,
                  scale = scale,
                  zvalue = zvalue,
                  draggable = draggable)
    
    hasColor.__init__(self, color)
    hasStroke.__init__(self, 
                       stroke = stroke, 
                       thickness = thickness,
                       linestyle = linestyle)

    # ─── Internal properties

    self._width = None 
    self._height = None 
    self._center = None 

    # ─── Rectangle attributes

    if width is None or height is None:
      raise AttributeError("'width' and 'height' must be specified for rectangle items.")
    else:
      self.width = width
      self.height = height

    self.center = center

  # ────────────────────────────────────────────────────────────────────────
  def initialize(self):
    '''
    Initialize the display
    '''

    # Parent initialization
    super().initialize()

    #  Initialize geometry
    self.setGeometry()

  # ────────────────────────────────────────────────────────────────────────
  def place(self):

    # Wait for initialization
    if not self.is_initialized: return

    # Definitions
    x0 = self._x
    y0 = self.canva.boundaries.y1 - self._y - self._height
    W = self._width
    H = self._height

    # Centering
    if self._center[0]: x0 -= W/2      
    if self._center[1]: y0 += H/2

    # Set geometry
    print('Final rect', x0, y0, W, H)
    self.setRect(QRectF(x0, y0, W, H))

  # ─── width ──────────────────────────────────────────────────────────────
  
  @property
  def width(self): return self._width

  @width.setter
  def width(self, w):

    self._width = w
    if self._height is not None: self.setGeometry()
  
  # ─── height ─────────────────────────────────────────────────────────────

  @property
  def height(self): return self._height

  @height.setter
  def height(self, h):

    self._height = h
    self.setGeometry()    

  # ─── center ─────────────────────────────────────────────────────────────

  @property
  def center(self): return self._center

  @center.setter
  def center(self, C):

    if isinstance(C, bool):
      self._center = (C,C)
    else:
      self._center = C

    self.setGeometry()

 