from PyQt6.QtCore import QRectF
from PyQt6.QtWidgets import QGraphicsRectItem

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
    reference. The defaut centering is (True, True), while (False,False)
    defines the reference as the top-left corner.
  
  Parameters
  ══════════

    * name        (str)             The rectangle's name
    * parent      (*QGraphicsItem*) The rectangle's parent item

    ─── position & transformations ──────────────

    * position    ([float, float])  Position of the reference point. Default: [0,0]
    * center  ([bool, bool] / bool) Centering around the reference point. Default: [True,True]
    * shift       ([float, float])  Shift wi. Default: [0,0]
    * orientation (float)           Orientation of the item (rad). Default: 0
    * scale       (float)           Scaling factor. Default: None
    * transformPt ([float, float])  Origin of the transformation

    ─── stack ───────────────────────────────────

    * zvalue      (float)           Z-value (stack order) of the item. Default: 1
    * behindParent (bool)           Boolean specifying if the item is behind
                                      its parent or not. Default: None
    * draggable   (bool)            Boolean specifying if the item can be 
                                      dragged. If True, the dragging callback
                                      is defined in the ... method. 
                                      Default: False.

    ─── style ────────────────────────────────

    * fill        (str / QColor)    Fill color. None stands for transparency. Default: None
    * stroke      (str / QColor)    Stroke color. None stands for transparency. Default: 'gray'
    * thickness   (float)           Stroke thickness, in scene units. Default: 0.001.
    * linestyle   (str)             Stroke style. Can have any value among 'solid' (default),
                                      'dash' (or '--'), 'dot' (or '..' or ':'), dashdot' (or '-.').
  '''

  # ────────────────────────────────────────────────────────────────────────
  def __init__(self, view, name, **kwargs):
    '''
    Rectangle item constructor
    '''  

    # Parent constructors    
    item.__init__(self, view, name, **kwargs)
    hasColor.__init__(self, **kwargs)
    hasStroke.__init__(self, **kwargs)
        
    # ─── Definitions

    self._width = None
    self._height = None
    self._center = (True, True)

    # ─── Initialization

    if 'width' not in kwargs or 'height' not in kwargs:
      raise AttributeError("'width' and 'height' must be specified for rectangle items.")
    else:
      self.width = kwargs['width']
      self.height = kwargs['height']

    if 'center' in kwargs: self.center = kwargs['center']

    # Initialize style
    self.setStyle()

  # ────────────────────────────────────────────────────────────────────────
  def setGeometry(self):

    # Conversion
    W = self._width
    H = self._height

    dx = 0
    dy = 0
    if self._center[0] or self._center[1]:
      
      bb = self.boundingRect()
      if self._center[0]: dx = -W/2
      if self._center[1]: dy = -H/2

    # Set geometry
    print((dx, dy, W, H))
    self.setRect(QRectF(dx, dy, W, H))

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

 