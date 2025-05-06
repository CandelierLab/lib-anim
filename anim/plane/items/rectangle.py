import numpy as np

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

    * Lx          (float)           The rectangle's width (length along x). Defau
    * Ly          (float)           The rectangle's height (length along y)
    * dimension   ([float, float])  Dimensions along the axis. Default: [0,0]
                                      The user must define either Lx, Ly or the dimensions.
                                      In case of conflicting definitions, the dimension attribute wins.

    ─── position & transformations ──────────────

    * x           (float)           x-position of the reference point. Default: 0
    * y           (float)           y-position of the reference point. Default: 0
    * position    ([float, float])  Position of the reference point. Default: [0,0]
                                      The user can define either x, y or the position.
                                      In case of conflict, the position attribute  wins.

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
               Lx = None,
               Ly = None,
               dimension = None,
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

    self._Lx = None 
    self._Ly = None 
    self._center = None 

    # ─── Rectangle attributes

    if dimension is not None and isinstance(dimension, (tuple, list, complex)):
      self.dimension = dimension

    elif Lx is None or Ly is None:
      raise AttributeError("Rectangle dimensions must be specified for rectangle items, either with 'dimension' or with 'Lx' and 'Ly'.")
      
    else:
      self.Lx = Lx
      self.Ly = Ly

    self.center = center

  # ────────────────────────────────────────────────────────────────────────
  def initialize(self):
    '''
    Initialize the display
    '''

    # Parent initialization
    super().initialize()

    #  Initialize geometry
    self.put()

  # ────────────────────────────────────────────────────────────────────────
  def put(self):

    # Wait for initialization
    if not self.is_initialized: return

    # Get absolute coordinates
    x, y = self.absoluteCoordinates()

    # Rectangle bottom-left corner
    x0 = x
    y0 = self.canva.boundaries.y1 - y - self._Ly

    # Centering
    if self._center[0]: x0 -= self._Lx/2      
    if self._center[1]: y0 += self._Ly/2

    # Set geometry
    print('Final rect', x0, y0, self._Lx, self._Ly)
    self.setRect(QRectF(x0, y0, self._Lx, self._Ly))

  # ─── width ──────────────────────────────────────────────────────────────
  
  @property
  def Lx(self): return self._Lx

  @Lx.setter
  def Lx(self, w):

    self._Lx = w
    if self._Ly is not None: self.put()
  
  # ─── height ─────────────────────────────────────────────────────────────

  @property
  def Ly(self): return self._Ly

  @Ly.setter
  def Ly(self, h):

    self._Ly = h
    self.put()    

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

    # Set position
    self.put()


  # ─── center ─────────────────────────────────────────────────────────────

  @property
  def center(self): return self._center

  @center.setter
  def center(self, C):

    if isinstance(C, bool):
      self._center = (C,C)
    else:
      self._center = C

    self.put()

 