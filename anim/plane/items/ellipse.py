import numpy as np

from PyQt6.QtCore import QRectF
from PyQt6.QtWidgets import QGraphicsEllipseItem

from .item import item, hasColor, hasStroke

# ══════════════════════════════════════════════════════════════════════════
#                                 ELLIPSE
# ══════════════════════════════════════════════════════════════════════════

class ellipse(item, hasColor, hasStroke, QGraphicsEllipseItem):
  '''
  An ellipse item is defined by its:

  - dimensions (major and minor axis length, named here a and b respectively)
  - position of the point of reference
  - orientation of the major axis
  
  Parameters
  ══════════

    * name       
        str
        The ellipse's name

    * parent
        QGraphicsItem (or derived object)
        default: None
        The ellipse's parent. If None, the position (x, y) is in absolute
        scene coordinates. Otherwise, the position is relative to the 
        parent's reference point.

    ─── dimensions ──────────────────────────────

    * Lx          
        float
        The ellipse's width, i.e. length along the x axis when orientation
        is 0. 

    * Ly
        float
        The ellipse's height, i.e.length along the y axis when orientation
        is 0.

    * dimension
        (float, float), [float, float], complex
        default: [0,0]
        Dimensions along the x and y axes when orientation is 0. The user
        must define either Lx, Ly or the dimension array. In case of
        conflicting definitions, the dimension attribute wins.

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
        Orientation of the ellipse, with respect to the positive part of the 
        x-axis.

    * center_of_rotation
        (float, float), [float, float], complex
        default: None
        Center point for the rotation. If None, it is set to the current [x,y].

    * scale
        float
        default: 1
        Scaling factor.

    * draggable
        bool
        default: False
        Boolean specifying if the ellipse can be dragged. If True, the
        dragging callback is defined in the 'itemChange' method, which is
        transfered to the canva's 'change' method (recommended).


    ─── stack ───────────────────────────────────

    * zvalue
        float
        default: 0
        Z-value (stack order) of the ellipse.

    * behindParent
        bool
        Default: False
        Boolean specifying if the ellipse is behind its parent or not.
    
    ─── style ────────────────────────────────

    * fill
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
               Lx = None,
               Ly = None,
               dimension = None,
               color = 'grey',
               stroke = None,
               thickness = 0,
               linestyle = '-',
               parent = None,
               behindParent = False,
               x = 0,
               y = 0,
               position = None,
               center_of_rotation = None,
               orientation = 0,
               scale = 1,
               zvalue = 0,
               draggable = False):
    '''
    Ellipse item constructor
    '''  

    # Parent constructors
    item.__init__(self, 
                  parent = parent,
                  behindParent = behindParent,
                  x = x,
                  y = y,
                  position = position,
                  center_of_rotation = center_of_rotation,
                  orientation = orientation,
                  scale = scale,
                  zvalue = zvalue,
                  draggable = draggable)
    
    hasColor.__init__(self, color = color)
    hasStroke.__init__(self,
                       stroke = stroke,
                       thickness = thickness,
                       linestyle = linestyle)

    # ─── Internal properties

    self._Lx = None 
    self._Ly = None 

    # ─── Ellipse attributes

    if dimension is not None and isinstance(dimension, (tuple, list, complex)):
      self.dimension = dimension

    elif Lx is None or Ly is None:
      raise AttributeError("Ellipse dimensions must be specified, either with 'dimension' or with 'Lx' and 'Ly'.")
      
    else:
      self.Lx = Lx
      self.Ly = Ly

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

    # Check for Nones
    if self._Lx is None or self._Ly is None: return

    # Get absolute coordinates
    x, y = self.absoluteCoordinates()

    # Bounding box bottom-left corner
    x0 = x - self._Lx/2
    y0 = self.canva.boundaries.y1 - y - self._Ly/2

    # Set geometry
    self.setRect(QRectF(x0, y0, self._Lx, self._Ly))

  # ─── width ──────────────────────────────────────────────────────────────
  
  @property
  def Lx(self): return self._Lx

  @Lx.setter
  def Lx(self, w):

    self._Lx = w
    self.put()
  
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