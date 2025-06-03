import numpy as np

from PyQt6.QtGui import QColor, QFont, QTransform, QTextDocument
from PyQt6.QtWidgets import QGraphicsTextItem

from .item import item, hasColor
from .events import event

# ══════════════════════════════════════════════════════════════════════════
#                                  TEXT
# ══════════════════════════════════════════════════════════════════════════

class text(item, hasColor):
  '''
  A text item is defined by its:

  - position of the point of reference
  - horizontal and vertical centering, with respect to the point of
      reference. The defaut centering is (True,True), while (False,False)
      defines the reference as the bottom-left corner. One can also use a single
      value to set both at the same time.
  - styling: font and color
  
  Parameters
  ══════════

    * name       
        str
        The text item's name

    * string       
        str
        default: ''
        The text's string. HTML formatting is supported by default.

    * group
        anim.plane.group
        default: None
        The text item's group. If None, the position of the reference point and
        center of rotation are in absolute coordinates. Otherwise, the
        position is relative to the group's reference point.

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

    * center
        (bool, bool), [bool, bool], bool
        default: [True,True]
        Boolean Defining the centering around the reference point. For tuple
        and list the first element is for the x-axis and the second is for 
        the y-axis.

    * orientation
        float
        default: 0, unit: radians
        Orientation of the text box, with respect to the positive part of the 
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
        Z-value (stack order) of the text box.
    
    ─── style ────────────────────────────────

    * color
        None, str, QColor
        default: 'grey'
        Fill color. None stands for transparency.

    * fontname
        str
        default: 'Helvetica'
        Font name

    * fontsize
        float
        default: 0.05
        Font size, in scene units.

    * style
        str
        default: ''
        Associated document's css style sheet. Global styling is accessed
        through the html selector.
        Example: 'html { background-color: yellow; }'
  '''

  # ────────────────────────────────────────────────────────────────────────
  def __init__(self, 
               string = '',
               center = (True, True),
               color = 'grey',
               fontname = 'Helvetica',
               fontsize = 0.05,
               style = '',
               group = None,
               x = 0,
               y = 0,
               position = None,
               center_of_rotation = [0,0],
               orientation = 0,
               zvalue = 0,
               draggable = False):
    '''
    text item constructor
    '''  

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
    
    hasColor.__init__(self, color = color)
    
    # ─── Internal properties

    self._string = string
    self._fontname = fontname 
    self._fontsize = fontsize
    self._style = style
    self.center = center

    # ─── QGraphicsItem

    class QText(QGraphicsTextItem, event): pass
    self.qitem = QText()    

    # Document
    self._document = QTextDocument()
    self._document.setDocumentMargin(0)
    self.qitem.setDocument(self._document)

  # ────────────────────────────────────────────────────────────────────────
  def initialize(self):
    '''
    Initialize the text item

    This method is meant to be overloaded and called.
    At this point:
    - the canva should be defined (automatically managed by itemDict)
    - the qitem should be defined (managed by the children class)
    '''

    # Parent initialization
    item.initialize(self)

    # Initialization specifics
    self.setFont()
    self.style = self._style
    self.string = self._string
    self.setGeometry()
  
  # ════════════════════════════════════════════════════════════════════════
  #                              GETTERS
  # ════════════════════════════════════════════════════════════════════════

  # ────────────────────────────────────────────────────────────────────────
  def Lx(self):
    return self.fontsize*self.qitem.boundingRect().width()/self.qitem.boundingRect().height()

  # ────────────────────────────────────────────────────────────────────────
  def Ly(self):
    return self.fontsize

  # ════════════════════════════════════════════════════════════════════════
  #                              SETTERS
  # ════════════════════════════════════════════════════════════════════════

  # ────────────────────────────────────────────────────────────────────────
  def setPosition(self):
    '''
    Override
    '''

    self.setGeometry()

  # ────────────────────────────────────────────────────────────────────────
  def setGeometry(self):
    '''
    Set the text box geometry
    '''

    # Check qitem
    if self.qitem is None: return

    # text box bottom-left corner
    x0 = self.position.x - (self.Lx()/2 if self._center[0] else 0)
    y0 = self.position.y + (self.Ly()/2 if self._center[1] else 0)

    # Set position
    self.qitem.setPos(x0*self.ppu, y0*self.ppu)

  # ────────────────────────────────────────────────────────────────────────
  def setOrientation(self):
    '''
    Set the text item orientation
    '''

    # Check qitem
    if self.qitem is None: return

    # Center of rotation
    self.qitem.setTransformOriginPoint(
      self.qitem.boundingRect().width()/2 if self._center[0] else 0,
      self.qitem.boundingRect().height()/2 if self._center[1] else 0)

    # Rotation
    self.qitem.setRotation(-self._orientation*180/np.pi)

  # ────────────────────────────────────────────────────────────────────────
  def setFont(self):
    '''
    Set the font
    '''

    # ─── Font

    font = QFont(self.fontname)
    self.qitem.setFont(font)

    # ─── Scale

    # Scale factor
    f = self.fontsize/self.qitem.boundingRect().height()

    # Item scale
    self.qitem.setTransform(QTransform.fromScale(f*self.ppu, -f*self.ppu), False)

    # Update geometry
    self.setGeometry()

  # ─── string ─────────────────────────────────────────────────────────────
  
  @property
  def string(self): return self._string

  @string.setter
  def string(self, s):

    self._string = s
    
    # Set text
    self.qitem.setHtml('<html>' + self._string + '</html>')
    self.setGeometry()
  
  # ─── fontname ───────────────────────────────────────────────────────────

  @property
  def fontname(self): return self._fontname

  @fontname.setter
  def fontname(self, s):

    self._fontname = s
    
    # Set text font
    self.setFont()

  # ─── fontsize ───────────────────────────────────────────────────────────
  
  @property
  def fontsize(self): return self._fontsize

  @fontsize.setter
  def fontsize(self, s):
    
    self._fontsize = s

    # Set text font
    self.setFont()

  # ─── style ──────────────────────────────────────────────────────────────
  
  @property
  def style(self): return self._style

  @style.setter
  def style(self, s):
    
    self._style = s

    # Document
    self._document.setDefaultStyleSheet(self._style)

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