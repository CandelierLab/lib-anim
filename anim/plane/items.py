import numpy as np
import anim

from PyQt6.QtCore import Qt, QPointF, QRectF, QSize
from PyQt6.QtGui import QColor, QPen, QBrush, QPolygonF, QFont, QPainterPath, QTransform, QPixmap, QImage, qRgb
from PyQt6.QtWidgets import QAbstractGraphicsShapeItem, QGraphicsItem, QGraphicsItemGroup, QGraphicsTextItem, QGraphicsLineItem, QGraphicsEllipseItem, QGraphicsPolygonItem, QGraphicsRectItem, QGraphicsPathItem, QGraphicsPixmapItem

# ══════════════════════════════════════════════════════════════════════════
#                             GENERIC ITEM
# ══════════════════════════════════════════════════════════════════════════

class item():
  """
  Item of the view (generic class)

  Items are the elements displayed in the :py:attr:`view2d.Qscene`. 
  This class provides a common constructor, conversions of positions
  to scene coordinates and styling of ``QAbstractGraphicsShapeItem`` 
  children.

  Attr:

    view (:class:`view2d`): Parent view.

    name (str): Unique identifier of the item.

    parent (:class:`item` *subclass*): Parent item, if any.

    position ([float, float]): Position of the item. See each subclass for
      details.

    zvalue (float): Z-value (stack order).
  """

  # ────────────────────────────────────────────────────────────────────────
  def __init__(self, view, name, **kwargs):
    """
    Generic item constructor

    Args:

      view (:class:`Animaton2d`): The view container.

      name (str): Name of the item. It should be unique, as it is used as an
        identifier in the :py:attr:`view2d.item` dict.

      parent (*QGraphicsItem*): The parent ``QGraphicsItem``.

      zvalue (float): Z-value (stack order).

      position ([float, float]): Position of the item. See each item's 
        documentation for a description.

      draggable (bool): If True, the element will be draggable. (default: ``False``)

      clickable (bool): *TO DO*
    """  

    # Call the other item's constructor, if any
    super().__init__()

    # --- Definitions

    # Reference view
    self.view = view

    # Assign name
    self.name = name

    self._parent = None
    self._behindParent = None
    self._position = [0,0]
    self._shift = [0,0]
    self._transformPoint = [0,0]
    self._orientation = None
    self._scale = None
    self._zvalue = None
    self._draggable = None
      
    # --- Initialization

    if 'parent' in kwargs: self.parent = kwargs['parent']
    if 'behindParent' in kwargs: self.behindParent = kwargs['behindParent']
    if 'position' in kwargs: self.position = kwargs['position']
    if 'transformPoint' in kwargs: self.transformPoint = kwargs['transformPoint']
    if 'orientation' in kwargs: self.orientation = kwargs['orientation']
    if 'scale' in kwargs: self.scale = kwargs['scale']
    if 'zvalue' in kwargs: self.zvalue = kwargs['zvalue']
    if 'draggable' in kwargs: self.draggable = kwargs['draggable']

    # Default color
    self.default_colors = ('white', 'gray') if self.view.window.style=='dark' else ('black', 'gray')

  # ────────────────────────────────────────────────────────────────────────
  def x2scene(self, x):
    """
    Convert the :math:`x` position in scene coordinates

    arg:
      x (float): The :math:`x` position.

    returns:
      The :math:`x` position in scene coordinates.
    """
    if self.parent is None:
      # return x*self.view.factor
      # print(self.view.boundaries['x'][0])
      return (x-self.view.boundaries['x'][0])*self.view.factor
    else:
      return x*self.view.factor

  # ────────────────────────────────────────────────────────────────────────
  def y2scene(self, y):
    """
    Convert the :math:`y` position in scene coordinates

    arg:
      y (float): The :math:`y` position.

    returns:
      The :math:`y` position in scene coordinates.
    """
    
    if self.parent is None:
      return (self.view.boundaries['y'][0]-y)*self.view.factor
    else:
      return -y*self.view.factor

  # ────────────────────────────────────────────────────────────────────────
  def xy2scene(self, xy):
    """
    Convert the :math:`x` and :math:`y` positions in scene coordinates

    arg:
      xy ([float,float]): The :math:`x` and :math:`y` positions.

    returns:
      The :math:`x` and :math:`y` position in scene coordinates.
    """

    return self.x2scene(xy[0]), self.y2scene(xy[1])

  # ────────────────────────────────────────────────────────────────────────
  def d2scene(self, d):
    """
    Convert a distance in scene coordinates

    arg:
      d (float): Distance to convert.

    returns:
      The distance in scene coordinates.
    """

    return d*self.view.factor

  # ────────────────────────────────────────────────────────────────────────
  def a2scene(self, a):
    """
    Convert an angle in scene coordinates (radian to degrees)

    arg:
      a (float): Angle to convert.

    returns:
      The angle in degrees.
    """

    return -a*180/np.pi
  
  # ────────────────────────────────────────────────────────────────────────
  def scene2x(self, u):
    """
    Convert horizontal scene coordinates into :math:`x` position

    arg:
      u (float): The horizontal coordinate.

    returns:
      The :math:`x` position.
    """

    if self._parent is None:
      return self.view.boundaries['x'][0] + u/self.view.factor
    else:
      return u/self.view.factor

  # ────────────────────────────────────────────────────────────────────────
  def scene2y(self, v):
    """
    Convert vertical scene coordinates into :math:`y` position

    arg:
      v (float): The horizontal coordinate.

    returns:
      The :math:`y` position.
    """

    if self._parent is None:
      return self.view.boundaries['y'][0] - v/self.view.factor
    else:
      return -v/self.view.factor

  # ────────────────────────────────────────────────────────────────────────
  def scene2xy(self, pos):
    """
    Convert scene coordinates into :math:`x` and :math:`y` positions

    arg:
      pos ([float,float]): The position in scene coordinates.

    returns:
      The :math:`x` and :math:`y` positions.
    """

    if isinstance(pos, QPointF):
      u = pos.x()
      v = pos.y()
    else:
      u = pos[0]
      v = pos[1]

    return self.scene2x(u), self.scene2y(v)

  # ────────────────────────────────────────────────────────────────────────
  def scene2d(self, d):
   
    return d/self.view.factor

  # ────────────────────────────────────────────────────────────────────────
  def width(self):

    if isinstance(self, group):
      bRect = self.childrenBoundingRect()
    else:
      bRect = self.boundingRect()

    return bRect.width()/self.view.factor

  # ────────────────────────────────────────────────────────────────────────
  def height(self):

    if isinstance(self, group):      
      bRect = self.childrenBoundingRect()
    else:
      bRect = self.boundingRect()

    return bRect.height()/self.view.factor

  # ────────────────────────────────────────────────────────────────────────
  def place(self):
    """
    Absolute positionning

    Places the item at an absolute position.
    
    Attributes:
      x (float): :math:`x`-coordinate of the new position. It can also be a 
        doublet [``x``,``y``], in this case the *y* argument is 
        overridden.
      y (float): :math:`y`-coordinate of the new position.
      z (float): A complex number :math:`z = x+jy`. Specifying ``z``
        overrides the ``x`` and ``y`` arguments.
    """

    # Set position
    self.setPos(self.x2scene(self._position[0])-self._shift[0], 
      self.y2scene(self._position[1])-self._shift[1])

  # ────────────────────────────────────────────────────────────────────────
  def move(self, dx=None, dy=None, z=None):
    """
    Relative displacement

    Displaces the item of relative amounts.
    
    Attributes:
      dx (float): :math:`x`-coordinate of the displacement. It can also be a 
        doublet [`dx`,`dy`], in this case the *dy* argument is overridden.
      dy (float): :math:`y`-coordinate of the displacement.
      z (float): A complex number :math:`z = dx+jdy`. Specifying ``z``
        overrides the ``x`` and ``y`` arguments.
    """

    # Doublet input
    if isinstance(dx, (tuple, list)):
      dy = dx[1]
      dx = dx[0]  

    # Convert from complex coordinates
    if z is not None:
      dx = np.real(z)
      dy = np.imag(z)

    # Store position
    if dx is not None: self._position[0] += dx
    if dy is not None: self._position[1] += dy

    self.place()

  # ────────────────────────────────────────────────────────────────────────
  def rotate(self, angle):
    """
    Relative rotation

    Rotates the item relatively to its current orientation.
    
    Attributes:
      angle (float): Orientational increment (rad)
    """

    self._orientation += angle
    self.setRotation(self.a2scene(self.orientation))

  # ────────────────────────────────────────────────────────────────────────
  def setStyle(self):
    """
    Item styling

    This function does not take any argument, instead it applies the changes
    defined by each item's styling attributes (*e.g.* color, stroke thickness).
    """

    # --- Fill

    if isinstance(self, QAbstractGraphicsShapeItem):

      if self._color['fill'] is not None:
        self.setBrush(QBrush(QColor(self._color['fill'])))

    # --- Stroke

    if isinstance(self, (QAbstractGraphicsShapeItem, QGraphicsLineItem)):

      Pen = QPen()

      #  Color
      if self._color['stroke'] is not None:
        Pen.setColor(QColor(self._color['stroke']))

      # Thickness
      if self._thickness is not None:
        Pen.setWidth(self._thickness)

      # Style
      match self._linestyle:
        case 'dash' | '--': Pen.setDashPattern([3,6])
        case 'dot' | ':' | '..': Pen.setStyle(Qt.PenStyle.DotLine)
        case 'dashdot' | '-.': Pen.setDashPattern([3,3,1,3])
      
      self.setPen(Pen)

  # ────────────────────────────────────────────────────────────────────────
  def mousePressEvent(self, event):
    """
    Simple click event

    For internal use only.

    args:
      event (QGraphicsSceneMouseEvent): The click event.
    """

    self.view.change(event.button(), self)
    super().mousePressEvent(event)

  # ────────────────────────────────────────────────────────────────────────
  def mouseDoubleClickEvent(self, event):
    """
    Double click event

    For internal use only.

    args:
      event (QGraphicsSceneMouseEvent): The double click event.
    """

    self.view.change(event.button().__str__() + '.double', self)
    super().mousePressEvent(event)

  # ────────────────────────────────────────────────────────────────────────
  def itemChange(self, change, value):
    """
    Item change notification

    This method is triggered upon item change. The item's transformation
    matrix has changed either because setTransform is called, or one of the
    transformation properties is changed. This notification is sent if the 
    ``ItemSendsGeometryChanges`` flag is enabled (e.g. when an item is 
    :py:attr:`item.movable`), and after the item's local transformation 
    matrix has changed.

    args:

      change (QGraphicsItem constant): 

    """
    # -- Define type

    type = None

    match change:
      case QGraphicsItem.GraphicsItemChange.ItemPositionHasChanged:
        type = 'move'

    # Report to view
    if type is not None:
      self.view.change(type, self)

    # Propagate change
    return super().itemChange(change, value)

  # --- Parent -------------------------------------------------------------

  @property
  def parent(self): return self._parent

  @parent.setter
  def parent(self, pName):
    self._parent = pName
    self.setParentItem(self.view.item[self._parent])

  # --- belowParent --------------------------------------------------------

  @property
  def behindParent(self): return self._behindParent

  @behindParent.setter
  def behindParent(self, b):
    self._behindParent = b
    self.setFlag(QGraphicsItem.ItemStacksBehindParent, b)

  # --- Position -------------------------------------------------------------

  @property
  def position(self): return self._position

  @position.setter
  def position(self, pos):
    
    if isinstance(pos, complex):

      # Convert from complex coordinates
      x = np.real(pos)
      y = np.imag(pos)

    else:

      # Doublet input
      x = pos[0]  
      y = pos[1]      

    # Store position
    self._position = [x,y]

    # Set position
    self.place()    

  # --- Transform point ----------------------------------------------------

  @property
  def transformPoint(self): return self._transformPoint

  @transformPoint.setter
  def transformPoint(self, pt):
    
    if isinstance(pt, complex):

      # Convert from complex coordinates
      x = np.real(pt)
      y = np.imag(pt)

    else:

      # Doublet input
      x = pt[0]  
      y = pt[1]      

    # Store transform point
    self._transformPoint = [x,y]

    # Set transform point
    self.setTransformOriginPoint(self.x2scene(x), self.y2scene(y))    

  # --- Orientation --------------------------------------------------------

  @property
  def orientation(self): return self._orientation

  @orientation.setter
  def orientation(self, angle):
    self._orientation = angle
    self.setRotation(self.a2scene(angle))

  # --- Scale --------------------------------------------------------

  @property
  def scale(self): return self._scale

  @scale.setter
  def scale(self, scale):
    self._scale = scale
    self.setTransform(QTransform.fromScale(scale[0], scale[1]), True)

  # --- Z-value ------------------------------------------------------------

  @property
  def zvalue(self): return self._zvalue

  @zvalue.setter
  def zvalue(self, z):
    self._zvalue = z
    self.setZValue(self._zvalue)

  # --- Draggability -------------------------------------------------------

  @property
  def draggable(self): return self._draggable

  @draggable.setter
  def draggable(self, z):
    
    self._draggable = z
    
    self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, self._draggable)
    self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges, self._draggable)
    if self._draggable:
      self.setCacheMode(QGraphicsItem.CacheMode.DeviceCoordinateCache)

# ══════════════════════════════════════════════════════════════════════════
#                                ITEMS
# ══════════════════════════════════════════════════════════════════════════

# ═══ group ════════════════════════════════════════════════════════════════

class group(item, QGraphicsItemGroup):
  """
  Group item

  A group item has no representation upon display but serves as a parent for
  multiple other items in order to create and manipulate composed objects.  
  """

  # ────────────────────────────────────────────────────────────────────────
  def __init__(self, view, name, **kwargs):
    """
    Group item constructor

    Defines a group, which inherits both from ``QGraphicsItemGroup`` and
    :class:`item`.

    Args:

      view (:class:`Animaton2d`): The view container.

      name (str): The item's identifier, which should be unique. It is used as a
        reference by :class:`view2d`. This is the only mandatory argument.

      parent (*QGraphicsItem*): The parent ``QGraphicsItem`` in the ``QGraphicsScene``.
        Default is ``None``, which means the parent is the ``QGraphicsScene`` itself.

      zvalue (float): Z-value (stack order) of the item.

      position ([float,float]): Position of the ``group``, ``text``, 
        ``circle``, and ``rectangle`` elements (scene units).

      orientation (float): Orientation of the item (rad)

      clickable (bool): *TO DO*

      movable (bool): If True, the element will be draggable. (default: ``False``)
    """  

    # Generic item constructor
    super().__init__(view, name, **kwargs)
   
# ═══ text ═════════════════════════════════════════════════════════════════

class text(item, QGraphicsTextItem):
  """
  Text item

  The ellipse is defined by it's :py:attr:`ellipse.major` and :py:attr:`ellipse.minor`
  axis lenghts, and by its position and orientation. The position of the 
  center is set by :py:attr:`item.position` and the orientation ... *TO WRITE*.
  
  Attributes:

    major (float): Length of the major axis.

    minor (float): Length of the minor axis.
  """

  def __init__(self, view, name, **kwargs):
    """
    Text item constructor

    Defines a textbox, which inherits both from ``QGraphicsEllipseItem`` and
    :class:`item`.

    Args:

      view (:class:`Animaton2d`): The view container.

      name (str): The item's identifier, which should be unique. It is used as a
        reference by :class:`view2d`. This is the only mandatory argument.

      parent (*QGraphicsItem*): The parent ``QGraphicsItem`` in the ``QGraphicsScene``.
        Default is ``None``, which means the parent is the ``QGraphicsScene`` itself.

      zvalue (float): Z-value (stack order) of the item.

      orientation (float): Orientation of the item (rad)

      position ([float,float]): Position of the ``group``, ``text``, 
        ``circle``, and ``rectangle`` elements (scene units).

      colors ([*color*, *color*]): Fill and stroke colors for ``circle``, 
        ``ellipse``, ``rectangle`` or ``polygon`` elements.  Colors can be 
        whatever input of ``QColor`` (*e.g*: ``darkCyan``, ``#ff112233`` or 
        (255, 0, 0, 127))

      linestyle (str): Stroke style (for ``circle``, ``ellipse``, ``rectangle``
        or ``p    
      clickable (bool): *TO DO*

      movable (bool): If True, the element will be draggable. (default: ``False``)
    """  

    # Generic item constructor
    super().__init__(view, name, **kwargs)
    
    # --- Definitions
  
    self._string = None
    self._color = None
    self._fontname = 'Arial'
    self._fontsize = 12
    self._center = (True, True)
    
    # --- Initialization

    self.string = kwargs['string'] if 'string' in kwargs else '-'
    self.color = kwargs['color'] if 'color' in kwargs else self.default_colors[0]
    if 'fontname' in kwargs: self.fontname = kwargs['fontname']
    if 'fontsize' in kwargs: self.fontsize = kwargs['fontsize']
    if 'center' in kwargs: self.center = kwargs['center'] 

  # --- String -------------------------------------------------------------

  @property
  def string(self): return self._string

  @string.setter
  def string(self, s):
    self._string = s
    self.setHtml(s)

  # --- Color --------------------------------------------------------------

  @property
  def color(self): return self._color

  @color.setter
  def color(self, c):
    self._color = c
    self.setDefaultTextColor(QColor(self._color))

  # --- Fontname -----------------------------------------------------------

  @property
  def fontname(self): return self._fontname

  @fontname.setter
  def fontname(self, name):
    self._fontname = name
    self.setFont((QFont(self._fontname, self._fontsize)))

  # --- Font size ----------------------------------------------------------

  @property
  def fontsize(self): return self._fontsize

  @fontsize.setter
  def fontsize(self, name):
    self._fontsize = name
    self.setFont((QFont(self._fontname, self._fontsize)))

  # --- Center -------------------------------------------------------------

  @property
  def center(self): return self._center

  @center.setter
  def center(self, C):

    if isinstance(C, bool):
      self._center = (C,C)
    else:
      self._center = C

    self._shift = [0,0]
    if self._center[0] or self._center[1]:
      
      bb = self.boundingRect()

      if self.center[0]:
        self._shift[0] = bb.width()/2
      if self._center[1]:
        self._shift[1] = bb.height()/2

    self.place()

# --- Ellipse --------------------------------------------------------------

class ellipse(item, QGraphicsEllipseItem):
  """
  Ellipse item

  The ellipse is defined by it's :py:attr:`ellipse.major` and :py:attr:`ellipse.minor`
  axis lenghts, and by its position and orientation. The position of the 
  center is set by :py:attr:`item.position` and the orientation ... *TO WRITE*.
  
  Attributes:

    major (float): Length of the major axis.

    minor (float): Length of the minor axis.
  """

  def __init__(self, view, name, **kwargs):
    """
    Ellipse item constructor

    Defines an ellipse, which inherits both from ``QGraphicsEllipseItem`` and
    :class:`item`.

    Args:

      view (:class:`Animaton2d`): The view container.

      name (str): The item's identifier, which should be unique. It is used as a
        reference by :class:`view2d`. This is the only mandatory argument.

      parent (*QGraphicsItem*): The parent ``QGraphicsItem`` in the ``QGraphicsScene``.
        Default is ``None``, which means the parent is the ``QGraphicsScene`` itself.

      zvalue (float): Z-value (stack order) of the item.

      orientation (float): Orientation of the item (rad)

      position ([float,float]): Position of the ``group``, ``text``, 
        ``circle``, and ``rectangle`` elements (scene units).

      colors ([*color*, *color*]): Fill and stroke colors for ``circle``, 
        ``ellipse``, ``rectangle`` or ``polygon`` elements.  Colors can be 
        whatever input of ``QColor`` (*e.g*: ``darkCyan``, ``#ff112233`` or 
        (255, 0, 0, 127))

      linestyle (str): Stroke style (for ``circle``, ``ellipse``, ``rectangle``
        or ``polygon``). Can have any value among ``solid`` (default), ``dash``
        or ``--``, ``dot`` or ``..`` or ``:``, ``dashdot`` or ``-.``.

      clickable (bool): *TO DO*

      movable (bool): If True, the element will be draggable. (default: ``False``)
    """  

    # Generic item constructor
    super().__init__(view, name, **kwargs)
    
    # --- Definitions

    self._major = None
    self._minor = None
    self._color = (None, None)
    self._thickness = None
    self._linestyle = None
    self._span = None

    # --- Initialization

    if 'major' not in kwargs or 'minor' not in kwargs:
      raise AttributeError("'major' and 'minor' must be specified for ellipse items.")
    else:
      self.major = kwargs['major']
      self.minor = kwargs['minor']

    self.colors = kwargs['colors'] if 'colors' in kwargs else [self.default_colors[1], self.default_colors[0]]
    self.linestyle = kwargs['linestyle'] if 'linestyle' in kwargs else None
    self.thickness = kwargs['thickness'] if 'thickness' in kwargs else 0   
    self.span = kwargs['span'] if 'span' in kwargs else None

  # --- Major axis length --------------------------------------------------

  @property
  def major(self): return self._major

  @major.setter
  def major(self, major):

    self._major = major

    if self._minor is not None:

      # Conversion
      M = self.d2scene(self._major)
      m = self.d2scene(self._minor)

      # Set geometry
      self.setRect(QRectF(-M/2, -m/2, M, m))

  # --- Minor axis length --------------------------------------------------

  @property
  def minor(self): return self._minor

  @minor.setter
  def minor(self, minor):

    self._minor = minor

    # Conversion
    M = self.d2scene(self._major)
    m = self.d2scene(self._minor)

    # Set geometry
    self.setRect(QRectF(-M/2, -m/2, M, m))

  # --- Colors -------------------------------------------------------------

  @property
  def colors(self): return self._color

  @colors.setter
  def colors(self, C):
    self._color = {'fill': C[0], 'stroke': C[1]}
    self.setStyle()

  # --- Thickness ----------------------------------------------------------

  @property
  def thickness(self): return self._thickness

  @thickness.setter
  def thickness(self, t):
    self._thickness = t
    self.setStyle()

  # --- Linestyle ----------------------------------------------------------

  @property
  def linestyle(self): return self._linestyle

  @linestyle.setter
  def linestyle(self, s):
    self._linestyle = s
    self.setStyle()      

 # --- Span ----------------------------------------------------------------

  @property
  def span(self): return self._span

  @span.setter
  def span(self, span):
    self._span = span
    if span is None:
      self.setStartAngle(0)
      self.setSpanAngle(5760)
    else:
      self.setStartAngle(int(span[0]*2880/np.pi))
      self.setSpanAngle(int(span[1]*2880/np.pi))

# --- Circle ---------------------------------------------------------------

class circle(item, QGraphicsEllipseItem):
  """
  Circle item

  The ellipse is defined by it's :py:attr:`ellipse.major` and :py:attr:`ellipse.minor`
  axis lenghts, and by its position and orientation. The position of the 
  center is set by :py:attr:`item.position` and the orientation ... *TO WRITE*.
  
  Attributes:

    major (float): Length of the major axis.

    minor (float): Length of the minor axis.
  """

  def __init__(self, view, name, **kwargs):
    """
    Circle item constructor

    Defines an ellipse, which inherits both from ``QGraphicsEllipseItem`` and
    :class:`item`.

    Args:

      view (:class:`Animaton2d`): The view container.

      name (str): The item's identifier, which should be unique. It is used as a
        reference by :class:`view2d`. This is the only mandatory argument.

      parent (*QGraphicsItem*): The parent ``QGraphicsItem`` in the ``QGraphicsScene``.
        Default is ``None``, which means the parent is the ``QGraphicsScene`` itself.

      zvalue (float): Z-value (stack order) of the item.

      orientation (float): Orientation of the item (rad)

      position ([float,float]): Position of the ``group``, ``text``, 
        ``circle``, and ``rectangle`` elements (scene units).

      colors ([*color*, *color*]): Fill and stroke colors for ``circle``, 
        ``ellipse``, ``rectangle`` or ``polygon`` elements.  Colors can be 
        whatever input of ``QColor`` (*e.g*: ``darkCyan``, ``#ff112233`` or 
        (255, 0, 0, 127))

      linestyle (str): Stroke style (for ``circle``, ``ellipse``, ``rectangle``
        or ``polygon``). Can have any value among ``solid`` (default), ``dash``
        or ``--``, ``dot`` or ``..`` or ``:``, ``dashdot`` or ``-.``.

      clickable (bool): *TO DO*

      movable (bool): If True, the element will be draggable. (default: ``False``)
    """  

    # Generic item constructor
    super().__init__(view, name, **kwargs)
    
    # --- Definitions

    self._radius = None
    self._color = (None, None)
    self._thickness = None
    self._linestyle = None
    self._span = None

    # --- Initialization

    if 'radius' not in kwargs:
      raise AttributeError("'radius' must be specified for circle items.")
    else:
      self.radius = kwargs['radius']

    self.colors = kwargs['colors'] if 'colors' in kwargs else [self.default_colors[1], self.default_colors[0]]
    self.linestyle = kwargs['linestyle'] if 'linestyle' in kwargs else None
    self.thickness = kwargs['thickness'] if 'thickness' in kwargs else 0
    self.span = kwargs['span'] if 'span' in kwargs else None

  # --- Radius -------------------------------------------------------------

  @property
  def radius(self): return self._radius

  @radius.setter
  def radius(self, r):

    self._radius = r
    R = self.d2scene(r)
    self.setRect(QRectF(-R, -R, 2*R, 2*R))

  # --- Colors -------------------------------------------------------------

  @property
  def colors(self): return self._color

  @colors.setter
  def colors(self, C):
    self._color = {'fill': C[0], 'stroke': C[1]}
    self.setStyle()

  # --- Thickness ----------------------------------------------------------

  @property
  def thickness(self): return self._thickness

  @thickness.setter
  def thickness(self, t):
    self._thickness = t
    self.setStyle()

  # --- Linestyle ----------------------------------------------------------

  @property
  def linestyle(self): return self._linestyle

  @linestyle.setter
  def linestyle(self, s):
    self._linestyle = s
    self.setStyle()      

  # --- Span ----------------------------------------------------------------

  @property
  def span(self): return self._span

  @span.setter
  def span(self, span):
    self._span = span
    if span is None:
      self.setStartAngle(0)
      self.setSpanAngle(5760)
    else:
      self.setStartAngle(int(span[0]*2880/np.pi))
      self.setSpanAngle(int(span[1]*2880/np.pi))

# --- Rectangle ------------------------------------------------------------

class rectangle(item, QGraphicsRectItem):
  """
  Rectangle item

  The ellipse is defined by it's :py:attr:`ellipse.major` and :py:attr:`ellipse.minor`
  axis lenghts, and by its position and orientation. The position of the 
  center is set by :py:attr:`item.position` and the orientation ... *TO WRITE*.
  
  Attributes:

    major (float): Length of the major axis.

    minor (float): Length of the minor axis.
  """

  def __init__(self, view, name, **kwargs):
    """
    Rectangle item constructor

    Defines an ellipse, which inherits both from ``QGraphicsEllipseItem`` and
    :class:`item`.

    Args:

      view (:class:`Animaton2d`): The view container.

      name (str): The item's identifier, which should be unique. It is used as a
        reference by :class:`view2d`. This is the only mandatory argument.

      parent (*QGraphicsItem*): The parent ``QGraphicsItem`` in the ``QGraphicsScene``.
        Default is ``None``, which means the parent is the ``QGraphicsScene`` itself.

      zvalue (float): Z-value (stack order) of the item.

      orientation (float): Orientation of the item (rad)

      position ([float,float]): Position of the ``group``, ``text``, 
        ``circle``, and ``rectangle`` elements (scene units).

      colors ([*color*, *color*]): Fill and stroke colors for ``circle``, 
        ``ellipse``, ``rectangle`` or ``polygon`` elements.  Colors can be 
        whatever input of ``QColor`` (*e.g*: ``darkCyan``, ``#ff112233`` or 
        (255, 0, 0, 127))

      linestyle (str): Stroke style (for ``circle``, ``ellipse``, ``rectangle``
        or ``polygon``). Can have any value among ``solid`` (default), ``dash``
        or ``--``, ``dot`` or ``..`` or ``:``, ``dashdot`` or ``-.``.

      clickable (bool): *TO DO*

      movable (bool): If True, the element will be draggable. (default: ``False``)
    """  

    # Generic item constructor
    super().__init__(view, name, **kwargs)
    
    # --- Definitions

    self._width = None
    self._height = None
    self._center = (True, True)
    self._color = (None, None)
    self._thickness = None
    self._linestyle = None

    # --- Initialization

    if 'width' not in kwargs or 'height' not in kwargs:
      raise AttributeError("'width' and 'height' must be specified for rectangle items.")
    else:
      self.width = kwargs['width']
      self.height = kwargs['height']

    if 'center' in kwargs: self.center = kwargs['center']
    self.colors = kwargs['colors'] if 'colors' in kwargs else [self.default_colors[1], self.default_colors[0]]
    self.linestyle = kwargs['linestyle'] if 'linestyle' in kwargs else None
    self.thickness = kwargs['thickness'] if 'thickness' in kwargs else 0   

  def setGeometry(self):

    # Conversion
    W = self.d2scene(self._width)
    H = self.d2scene(self._height)

    dx = 0
    dy = 0
    if self._center[0] or self._center[1]:
      
      bb = self.boundingRect()
      if self._center[0]: dx = -W/2
      if self._center[1]: dy = H/2

    # Set geometry
    self.setRect(QRectF(dx, dy, W, -H))

  # --- Width --------------------------------------------------------------

  @property
  def width(self): return self._width

  @width.setter
  def width(self, w):

    self._width = w
    if self._height is not None: self.setGeometry()
      
  # --- Height -------------------------------------------------------------

  @property
  def height(self): return self._height

  @height.setter
  def height(self, h):

    self._height = h
    self.setGeometry()    

  # --- Center -------------------------------------------------------------

  @property
  def center(self): return self._center

  @center.setter
  def center(self, C):

    if isinstance(C, bool):
      self._center = (C,C)
    else:
      self._center = C

    self.setGeometry()

  # --- Colors -------------------------------------------------------------

  @property
  def colors(self): return self._color

  @colors.setter
  def colors(self, C):
    self._color = {'fill': C[0], 'stroke': C[1]}
    self.setStyle()

  # --- Thickness ----------------------------------------------------------

  @property
  def thickness(self): return self._thickness

  @thickness.setter
  def thickness(self, t):
    self._thickness = t
    self.setStyle()

  # --- Linestyle ----------------------------------------------------------

  @property
  def linestyle(self): return self._linestyle

  @linestyle.setter
  def linestyle(self, s):
    self._linestyle = s
    self.setStyle()      

# --- Line -----------------------------------------------------------------

class line(item, QGraphicsLineItem):
  """
  Line item

  The ellipse is defined by it's :py:attr:`ellipse.major` and :py:attr:`ellipse.minor`
  axis lenghts, and by its position and orientation. The position of the 
  center is set by :py:attr:`item.position` and the orientation ... *TO WRITE*.
  
  Attributes:

    major (float): Length of the major axis.

    minor (float): Length of the minor axis.
  """

  def __init__(self, view, name, **kwargs):
    """
    Line item constructor

    Defines an ellipse, which inherits both from ``QGraphicsEllipseItem`` and
    :class:`item`.

    Args:

      view (:class:`Animaton2d`): The view container.

      name (str): The item's identifier, which should be unique. It is used as a
        reference by :class:`view2d`. This is the only mandatory argument.

      parent (*QGraphicsItem*): The parent ``QGraphicsItem`` in the ``QGraphicsScene``.
        Default is ``None``, which means the parent is the ``QGraphicsScene`` itself.

      zvalue (float): Z-value (stack order) of the item.

      orientation (float): Orientation of the item (rad)

      position ([float,float]): Position of the ``group``, ``text``, 
        ``circle``, and ``rectangle`` elements (scene units).

      colors ([*color*, *color*]): Fill and stroke colors for ``circle``, 
        ``ellipse``, ``rectangle`` or ``polygon`` elements.  Colors can be 
        whatever input of ``QColor`` (*e.g*: ``darkCyan``, ``#ff112233`` or 
        (255, 0, 0, 127))

      linestyle (str): Stroke style (for ``circle``, ``ellipse``, ``rectangle``
        or ``polygon``). Can have any value among ``solid`` (default), ``dash``
        or ``--``, ``dot`` or ``..`` or ``:``, ``dashdot`` or ``-.``.

      clickable (bool): *TO DO*

      movable (bool): If True, the element will be draggable. (default: ``False``)
    """  

    # Generic item constructor
    super().__init__(view, name, **kwargs)
    
    # --- Definitions

    self._points = None
    self._color = (None, None)
    self._thickness = None
    self._linestyle = None

    # --- Initialization

    if 'points' not in kwargs:
      raise AttributeError("'points' must be specified for line items.")
    else:
      self.points = kwargs['points']

    self.color = kwargs['color'] if 'color' in kwargs else self.default_colors[0]
    self.linestyle = kwargs['linestyle'] if 'linestyle' in kwargs else None
    self.thickness = kwargs['thickness'] if 'thickness' in kwargs else 0   

  # --- Points -------------------------------------------------------------

  @property
  def points(self): return self._points

  @points.setter
  def points(self, p):

    self._points = p

    x1 = self.x2scene(p[0][0])
    y1 = self.y2scene(p[0][1])
    x2 = self.x2scene(p[1][0])
    y2 = self.y2scene(p[1][1])
    self.setLine(x1, y1, x2, y2)
  
  # --- Color --------------------------------------------------------------

  @property
  def color(self): return self._color

  @color.setter
  def color(self, C):
    self._color = {'fill': None, 'stroke': C}
    self.setStyle()

  # --- Thickness ----------------------------------------------------------

  @property
  def thickness(self): return self._thickness

  @thickness.setter
  def thickness(self, t):
    self._thickness = t
    self.setStyle()

  # --- Linestyle ----------------------------------------------------------

  @property
  def linestyle(self): return self._linestyle

  @linestyle.setter
  def linestyle(self, s):
    self._linestyle = s
    self.setStyle()      

# --- Polygon --------------------------------------------------------------

class polygon(item, QGraphicsPolygonItem):
  """
  Polygon item

  The ellipse is defined by it's :py:attr:`ellipse.major` and :py:attr:`ellipse.minor`
  axis lenghts, and by its position and orientation. The position of the 
  center is set by :py:attr:`item.position` and the orientation ... *TO WRITE*.
  
  Attributes:

    major (float): Length of the major axis.

    minor (float): Length of the minor axis.
  """

  def __init__(self, view, name, **kwargs):
    """
    Polygon item constructor

    Defines an ellipse, which inherits both from ``QGraphicsEllipseItem`` and
    :class:`item`.

    Args:

      view (:class:`Animaton2d`): The view container.

      name (str): The item's identifier, which should be unique. It is used as a
        reference by :class:`view2d`. This is the only mandatory argument.

      parent (*QGraphicsItem*): The parent ``QGraphicsItem`` in the ``QGraphicsScene``.
        Default is ``None``, which means the parent is the ``QGraphicsScene`` itself.

      zvalue (float): Z-value (stack order) of the item.

      orientation (float): Orientation of the item (rad)

      position ([float,float]): Position of the ``group``, ``text``, 
        ``circle``, and ``rectangle`` elements (scene units).

      colors ([*color*, *color*]): Fill and stroke colors for ``circle``, 
        ``ellipse``, ``rectangle`` or ``polygon`` elements.  Colors can be 
        whatever input of ``QColor`` (*e.g*: ``darkCyan``, ``#ff112233`` or 
        (255, 0, 0, 127))

      linestyle (str): Stroke style (for ``circle``, ``ellipse``, ``rectangle``
        or ``polygon``). Can have any value among ``solid`` (default), ``dash``
        or ``--``, ``dot`` or ``..`` or ``:``, ``dashdot`` or ``-.``.

      clickable (bool): *TO DO*

      movable (bool): If True, the element will be draggable. (default: ``False``)
    """  

    # Generic item constructor
    super().__init__(view, name, **kwargs)
    
    # --- Definitions

    self._points = None
    self._color = (None, None)
    self._thickness = None
    self._linestyle = None

    # --- Initialization

    if 'points' not in kwargs:
      raise AttributeError("'points' must be specified for polygon items.")
    else:
      self.points = kwargs['points']

    self.colors = kwargs['colors'] if 'colors' in kwargs else [self.default_colors[1], self.default_colors[0]]
    self.linestyle = kwargs['linestyle'] if 'linestyle' in kwargs else None
    self.thickness = kwargs['thickness'] if 'thickness' in kwargs else 0   

  # --- Points -------------------------------------------------------------

  @property
  def points(self): return self._points

  @points.setter
  def points(self, points):

    self._points = points

    poly = []
    for p in self._points:
      poly.append(QPointF(self.d2scene(p[0]), -self.d2scene(p[1])))
    self.setPolygon(QPolygonF(poly))
  
  # --- Color --------------------------------------------------------------

  @property
  def colors(self): return self._color

  @colors.setter
  def colors(self, C):
    self._color = {'fill': C[0], 'stroke': C[1]}
    self.setStyle()

  # --- Thickness ----------------------------------------------------------

  @property
  def thickness(self): return self._thickness

  @thickness.setter
  def thickness(self, t):
    self._thickness = t
    self.setStyle()

  # --- Linestyle ----------------------------------------------------------

  @property
  def linestyle(self): return self._linestyle

  @linestyle.setter
  def linestyle(self, s):
    self._linestyle = s
    self.setStyle()      

# --- Path -----------------------------------------------------------------

class path(item, QGraphicsPathItem):
  """
  Path item

  The ellipse is defined by it's :py:attr:`ellipse.major` and :py:attr:`ellipse.minor`
  axis lenghts, and by its position and orientation. The position of the 
  center is set by :py:attr:`item.position` and the orientation ... *TO WRITE*.
  
  Attributes:

    major (float): Length of the major axis.

    minor (float): Length of the minor axis.
  """

  def __init__(self, view, name, **kwargs):
    """
    Path item constructor

    Defines an ellipse, which inherits both from ``QGraphicsEllipseItem`` and
    :class:`item`.

    Args:

      view (:class:`Animaton2d`): The view container.

      name (str): The item's identifier, which should be unique. It is used as a
        reference by :class:`view2d`. This is the only mandatory argument.

      parent (*QGraphicsItem*): The parent ``QGraphicsItem`` in the ``QGraphicsScene``.
        Default is ``None``, which means the parent is the ``QGraphicsScene`` itself.

      zvalue (float): Z-value (stack order) of the item.

      orientation (float): Orientation of the item (rad)

      position ([float,float]): Position of the ``group``, ``text``, 
        ``circle``, and ``rectangle`` elements (scene units).

      colors ([*color*, *color*]): Fill and stroke colors for ``circle``, 
        ``ellipse``, ``rectangle`` or ``polygon`` elements.  Colors can be 
        whatever input of ``QColor`` (*e.g*: ``darkCyan``, ``#ff112233`` or 
        (255, 0, 0, 127))

      linestyle (str): Stroke style (for ``circle``, ``ellipse``, ``rectangle``
        or ``polygon``). Can have any value among ``solid`` (default), ``dash``
        or ``--``, ``dot`` or ``..`` or ``:``, ``dashdot`` or ``-.``.

      clickable (bool): *TO DO*

      movable (bool): If True, the element will be draggable. (default: ``False``)
    """  

    # Generic item constructor
    super().__init__(view, name, **kwargs)
    
    # --- Definitions

    self._points = None
    self._color = (None, None)
    self._thickness = None
    self._linestyle = None

    # --- Initialization

    if 'points' not in kwargs:
      raise AttributeError("'points' must be specified for path items.")
    else:
      self.points = kwargs['points']

    self.colors = kwargs['colors'] if 'colors' in kwargs else [self.default_colors[1], self.default_colors[0]]
    self.linestyle = kwargs['linestyle'] if 'linestyle' in kwargs else None
    self.thickness = kwargs['thickness'] if 'thickness' in kwargs else 0   

  # --- Points -------------------------------------------------------------

  @property
  def points(self): return self._points

  @points.setter
  def points(self, points):

    self._points = points

    P = QPainterPath()
    for k,p in enumerate(points):
      if k:
        P.lineTo(self.x2scene(p[0]), self.y2scene(p[1]))
      else:
        P.moveTo(self.x2scene(p[0]), self.y2scene(p[1]))

    self.setPath(P)
  
  # --- Color --------------------------------------------------------------

  @property
  def colors(self): return self._color

  @colors.setter
  def colors(self, C):
    self._color = {'fill': C[0], 'stroke': C[1]}
    self.setStyle()

  # --- Thickness ----------------------------------------------------------

  @property
  def thickness(self): return self._thickness

  @thickness.setter
  def thickness(self, t):
    self._thickness = t
    self.setStyle()

  # --- Linestyle ----------------------------------------------------------

  @property
  def linestyle(self): return self._linestyle

  @linestyle.setter
  def linestyle(self, s):
    self._linestyle = s
    self.setStyle()      

# --- Image -----------------------------------------------------------------

class image(item, QGraphicsPixmapItem):
  """
  RGB Image item from a numpy array or a file.
  If the source is a numpy array, the three channels must have values in [0,1]
  """

  def __init__(self, view, name, position=[0,0], width=None, height=None, **kwargs):
    """
    Image item constructor
    """  

    # Generic item constructor
    super().__init__(view, name, **kwargs)
    
    # --- Definitions

    self._width = None
    self._height = None
    self._file = None
    self._image = None
    self._table = None
    self.pixmap = None
    self.flip_vertical = kwargs['flip_vertical'] if 'flip_vertical' in kwargs else False
    
    # --- Initialization

    self.width = width if width is not None else self.view.boundaries['width']
    self.height = height if height is not None else self.view.boundaries['height']
    self.position = position

    self.cmap = kwargs['cmap'] if 'cmap' in kwargs else Colormap('grey', ncolors=256)

    # --- Image

    if 'file' in kwargs:
      self.file = kwargs['file']
    elif 'image' in kwargs:
      self.image = kwargs['image']
    else:
      self.image = np.zeros((1,1))
      
    # Adjust position
    # self.setPos(0,-self.height)

  # --- Position -----------------------------------------------------------

  @property
  def position(self): return self._position

  @position.setter
  def position(self, p):
    self._position = [p[0], p[1] + self.height]
    self.place() 

  # --- Width --------------------------------------------------------------

  @property
  def width(self): return self.scene2d(self._width)

  @width.setter
  def width(self, w):

    self._width = int(self.d2scene(w))
    if self.pixmap is not None:
      self.pixmap = self.pixmap.scaled(QSize(self._width, self._height))
      self.setPixmap(self.pixmap)
  
  # --- Height --------------------------------------------------------------

  @property
  def height(self): return self.scene2d(self._height)

  @height.setter
  def height(self, h):

    self._height = int(self.d2scene(h))
    if self.pixmap is not None:
      self.pixmap = self.pixmap.scaled(QSize(self._width, self._height))
      self.setPixmap(self.pixmap)
  
  # --- File ---------------------------------------------------------------

  @property
  def file(self): return self._file

  @file.setter
  def file(self, fname):

    if fname is not None:
      self._file = fname

      self.pixmap = QPixmap.fromImage(QImage(self._file)).scaled(QSize(self._width, self._height))
      self.setPixmap(self.pixmap)

  # --- Image ---------------------------------------------------------------

  @property
  def image(self): return self._image

  @image.setter
  def image(self, img):

    # Rescale on [0,255]
    img[img<0] = 0
    img[img>1] = 1
    self._image = (img*255).astype(np.uint8)
    
    # Build image
    qImg = QImage(self._image.data, self._image.shape[1], self._image.shape[0], QImage.Format.Format_RGB888)

    # Apply colormap
    qImg.setColorTable(self._ctable)
      
    self.pixmap = QPixmap.fromImage(qImg).scaled(QSize(self._width, self._height))
    # self.pixmap = QPixmap.fromImage(qImg)

    if self.flip_vertical:
      self.pixmap = self.pixmap.transformed(QTransform().scale(1, -1))

    self.setPixmap(self.pixmap)

  # --- Colormap -----------------------------------------------------------

  @property
  def cmap(self): return self._cmap

  @cmap.setter
  def cmap(self, C):

    self._cmap = C
    self._ctable = C.colortable()

# --- Field ----------------------------------------------------------------

class field(item, QGraphicsPixmapItem):
  """
  field item
  """

  def __init__(self, view, name, position=[0,0], width=None, height=None, **kwargs):
    """
    Field item constructor
    """  

    # Generic item constructor
    super().__init__(view, name, **kwargs)
    
    # --- Definitions

    self._width = None
    self._height = None
    self._field = None
    self._table = None
    self.pixmap = None
    self.flip_vertical = kwargs['flip_vertical'] if 'flip_vertical' in kwargs else False
    
    # --- Initialization

    self.width = width if width is not None else self.view.boundaries['width']
    self.height = height if height is not None else self.view.boundaries['height']
    self.position = position

    self.cmap = kwargs['cmap'] if 'cmap' in kwargs else Colormap('turbo', ncolors=256)

    # --- Field

    self.field = kwargs['field'] if 'field' in kwargs else np.zeros((1,1))
      
    # Adjust position
    # self.setPos(0,-self.height)

  # --- Position -----------------------------------------------------------

  @property
  def position(self): return self._position

  @position.setter
  def position(self, p):
    self._position = [p[0], p[1] + self.height]
    self.place() 

  # --- Width --------------------------------------------------------------

  @property
  def width(self): return self.scene2d(self._width)

  @width.setter
  def width(self, w):

    self._width = int(self.d2scene(w))
    if self.pixmap is not None:
      self.pixmap = self.pixmap.scaled(QSize(self._width, self._height))
      self.setPixmap(self.pixmap)
  
  # --- Height --------------------------------------------------------------

  @property
  def height(self): return self.scene2d(self._height)

  @height.setter
  def height(self, h):

    self._height = int(self.d2scene(h))
    if self.pixmap is not None:
      self.pixmap = self.pixmap.scaled(QSize(self._width, self._height))
      self.setPixmap(self.pixmap)

  # --- Image ---------------------------------------------------------------

  @property
  def field(self): return self._field

  @field.setter
  def field(self, img):

    # Rescale on [0,255]
    img = 255*(img - self._cmap.range[0])/(self._cmap.range[1] - self._cmap.range[0])
    img[img<0] = 0
    img[img>255] = 255
    self._field = img.astype(np.uint8)
    
    # Build image
    qImg = QImage(self._field.data, self._field.shape[1], self._field.shape[0], self._field.shape[1], QImage.Format.Format_Indexed8)

    # Apply colormap
    qImg.setColorTable(self._ctable)
      
    self.pixmap = QPixmap.fromImage(qImg).scaled(QSize(self._width, self._height))

    if self.flip_vertical:
      self.pixmap = self.pixmap.transformed(QTransform().scale(1, -1))

    self.setPixmap(self.pixmap)

  # --- Colormap -----------------------------------------------------------

  @property
  def cmap(self): return self._cmap

  @cmap.setter
  def cmap(self, C):

    self._cmap = C
    self._ctable = C.colortable()