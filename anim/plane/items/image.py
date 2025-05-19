from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QImage, QPixmap, QTransform
from PyQt6.QtWidgets import QGraphicsItem, QGraphicsPixmapItem

from ..geometry import point

from .item import item

# ══════════════════════════════════════════════════════════════════════════
#                                IMAGE
# ══════════════════════════════════════════════════════════════════════════

class image(item):
  '''
  An image item is defined by its:

  - source image (numpy array or file)
  - colormap
  - dimensions (width and height)
  - position of the point of reference
  - horizontal and vertical centering, with respect to the point of
      reference. The defaut centering is (True,True), while (False,False)
      defines the reference as the bottom-left corner. One can also use a single
      value to set both at the same time.
  - flipping (vertical and horizontal)
  
  Parameters
  ══════════

    * name       
        str
        The image item's name

    * group
        anim.plane.group
        default: None
        The image's group. If None, the position of the reference point and
        center of rotation are in absolute coordinates. Otherwise, the
        position is relative to the group's reference point.

    ─── image ───────────────────────────────────

    * file
        path
        The image file. The user should define either a file or an array.

    * array
        numpy array
        The image array. If 2D then it is assumed to be greyscale. If 3D,
        the 3 channels are RGB.

    * flip
        [boolean, boolean], (boolean, boolean)
        default: [False, False]
        Horizontal and vertical flipping of the image.

    * colormap
        Colormap object
        default: Colormap('grey', ncolors=256) / RGB
        Image colormap.

    ─── dimensions ──────────────────────────────

    * Lx          
        float
        The image width, i.e. length along the x axis when orientation is 0. 

    * Ly
        float
        The image height, i.e.length along the y axis when orientation is 0.

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

    * center
        (bool, bool), [bool, bool], bool
        default: [True,True]
        Boolean Defining the centering around the reference point. For tuple
        and list the first element is for the x-axis and the second is for 
        the y-axis.

    ─── transformations ─────────────────────────

    * orientation
        float
        default: 0, unit: radians
        Orientation of the image, with respect to the positive part of the 
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
        Z-value (stack order) of the image.
  '''

  # ════════════════════════════════════════════════════════════════════════
  #                              INITIALIZATION
  # ════════════════════════════════════════════════════════════════════════

  # ────────────────────────────────────────────────────────────────────────
  def __init__(self,
               file = None,
               array = None,
               flip = [False, False],
               colormap = None,
               Lx = None,
               Ly = None,
               dimension = None,
               center = [True, True],
               group = None,
               x = 0,
               y = 0,
               position = None,
               center_of_rotation = [0,0],
               orientation = 0,
               zvalue = 0,
               draggable = False):
    '''
    Image constructor
    '''  

    # ─── Checks

    if file is None and array is None:
      raise ValueError("Either the 'file' or 'array' parameter should be defined.")

    # ─── Parent constructors

    item.__init__(self, 
                  group = group,
                  x = x,
                  y = y,
                  position = position,
                  center_of_rotation = center_of_rotation,
                  orientation = orientation,
                  zvalue = zvalue,
                  draggable = draggable)
    
    # ─── Internal properties

    self._file = file
    self._array = array
    self._flip = flip
    self._colormap = colormap

    self._pixmap = None

    # ─── geometrical properties

    self._Lx = None 
    self._Ly = None 
    self._center = None

    if dimension is not None and isinstance(dimension, (tuple, list, complex)):
      self.dimension = dimension

    elif Lx is None or Ly is None:
      raise AttributeError("Image dimensions must be specified, either with 'dimension' or with 'Lx' and 'Ly'.")
      
    else:
      self.Lx = Lx
      self.Ly = Ly

    self.center = center

    # ─── QGraphicsItem

    self.qitem = QGraphicsPixmapItem()

    # Smooth display
    # self.qitem.setTransformationMode(Qt.TransformationMode.SmoothTransformation)
    self.qitem.setCacheMode(QGraphicsItem.CacheMode.DeviceCoordinateCache)

  # ────────────────────────────────────────────────────────────────────────
  def initialize(self):
    '''
    Initialize the image

    At this point:
    - the canva should be defined (automatically managed by itemDict)
    - the qitem should be defined (managed by the children class)
    '''

    # Parent initialization
    item.initialize(self)

    # Data
    if self.file is not None: self.file = self._file
    elif self.aray is not None: self.array = self._array

    # Initialization specifics
    self.setGeometry()
    
  # ════════════════════════════════════════════════════════════════════════
  #                                   SETTERS
  # ════════════════════════════════════════════════════════════════════════

  # ────────────────────────────────────────────────────────────────────────
  def setGeometry(self):
    '''
    Set the image geometry
    '''

    # Check qitem
    if self.qitem is None: return

    # Rectangle bottom-left corner
    x0 = self.position.X - (self.Lx/2 if self._center[0] else 0)
    y0 = self.position.Y - (self.Ly/2 if self._center[1] else 0)

    if self._pixmap is not None:      
      self.setPixmap()

  # ────────────────────────────────────────────────────────────────────────
  def setPixmap(self):
    '''
    Set the pixmap
    '''

    # Check pixmap
    if self._pixmap is None: return

    # Set size
    self._pixmap = self._pixmap.scaled(QSize(self.Lx, self.Ly))
    # self._pixmap = self._pixmap

    # Flipping
    T = QTransform().scale(1-self.flip[0]*2, self.flip[1]*2-1)

    #  Set the pixmap
    self.qitem.setPixmap(self._pixmap.transformed(T))

  # ════════════════════════════════════════════════════════════════════════
  #                            DYNAMIC PROPERTIES
  # ════════════════════════════════════════════════════════════════════════

  # ─── file ───────────────────────────────────────────────────────────────

  @property
  def file(self): return self._file

  @file.setter
  def file(self, path):

    self._file = path

    # Define pixmap
    self._pixmap = QPixmap.fromImage(QImage(self._file))
    
    # Set image
    self.setPixmap()

  # ─── array ──────────────────────────────────────────────────────────────

  @property
  def array(self): return self._array

  @array.setter
  def array(self, A):

    self._array = A
    
    # Set image
    self.setPixmap()

  # ─── flip ───────────────────────────────────────────────────────────────

  @property
  def flip(self): return self._flip

  @flip.setter
  def flip(self, f):

    self._flip = list(f)
    
    # Set image
    self.setPixmap()

  # ─── colormap ───────────────────────────────────────────────────────────
  
  @property
  def colormap(self): return self._colormap

  @colormap.setter
  def colormap(self, cmap):

    self._colormap = list(cmap)
    
    # Set image
    self.setPixmap()

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

    if isinstance(C, bool):
      self._center = (C,C)
    else:
      self._center = C

    # Set geometry
    self.setGeometry()