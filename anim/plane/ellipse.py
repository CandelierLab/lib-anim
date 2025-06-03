import numpy as np

from PyQt6.QtCore import QRectF
from PyQt6.QtWidgets import QGraphicsEllipseItem

from .item import item, hasColor, hasStroke
from .events import event

# ══════════════════════════════════════════════════════════════════════════
#                                 ELLIPSE
# ══════════════════════════════════════════════════════════════════════════

class ellipse(item, hasColor, hasStroke):
  '''
  An ellipse item is defined by its:

  - dimensions (major and minor axis length, named here a and b respectively)
  - position of the point of reference
  - orientation of the major axis
  - styling
  
  Parameters
  ══════════

    * name       
        str
        The ellipse's name

    * group
        anim.plane.group
        default: None
        The ellipse's group. If None, the position of the reference point and
        center of rotation are in absolute coordinates. Otherwise, the
        position is relative to the group's reference point.

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

    ─── transformations ─────────────────────────

    * orientation
        float
        default: 0, unit: radians
        Orientation of the ellipse, with respect to the positive part of the 
        x-axis.

    * center_of_rotation
        (float, float), [float, float], complex
        default: None
        Center point for the rotation.

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
        Z-value (stack order) of the ellipse.
    
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
               Lx = None,
               Ly = None,
               dimension = None,
               color = 'grey',
               stroke = None,
               thickness = 0,
               linestyle = '-',
               group = None,
               x = 0,
               y = 0,
               position = None,
               center_of_rotation = [0,0],
               orientation = 0,
               zvalue = 0,
               draggable = False):
    '''
    Ellipse item constructor
    '''  

    # Parent constructors
    item.__init__(self, 
                  group = group,
                  x = x,
                  y = y,
                  position = position,
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

    # ─── QGraphicsItem

    class QEllipse(QGraphicsEllipseItem, event): pass
    self.qitem = QEllipse()


  # ────────────────────────────────────────────────────────────────────────
  def initialize(self):
    '''
    Initialize the ellipse

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
    Set the ellipse's geometry
    '''

    # Check qitem
    if self.qitem is None: return

    # Set geometry
    self.qitem.setRect(QRectF(-self.Lx/2*self.ppu,
                              -self.Ly/2*self.ppu,
                              self.Lx*self.ppu,
                              self.Ly*self.ppu))

  # ─── width ──────────────────────────────────────────────────────────────
  
  @property
  def Lx(self): return self._Lx

  @Lx.setter
  def Lx(self, w):

    self._Lx = abs(w)
    
    # Set geometry
    self.setGeometry()
  
  # ─── height ─────────────────────────────────────────────────────────────

  @property
  def Ly(self): return self._Ly

  @Ly.setter
  def Ly(self, h):

    self._Ly = abs(h)

    # Set geometry
    self.setGeometry() 

  # ─── dimensions ─────────────────────────────────────────────────────────
  
  @property
  def dimension(self): return [self._Lx, self._Ly]

  @dimension.setter
  def dimension(self, D):
    
    if isinstance(D, complex):

      # Convert from complex coordinates
      self._Lx = abs(np.real(D))
      self._Ly = abs(np.imag(D))

    else:

      # Doublet input
      self._Lx = abs(D[0])
      self._Ly = abs(D[1])

    # Set geometry
    self.setGeometry()