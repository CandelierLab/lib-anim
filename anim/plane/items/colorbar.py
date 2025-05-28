import numpy as np

from .group import composite
from .path import path
from .polygon import polygon
from .circle import circle
from .text import text

class colorbar(composite):
  '''
  Colorbar item (composite)

  A colorbar is defined by its:

    - position and dimension. The reference point is the center of the colorbar 
        rectangle, and the dimensions are those of the colorbar rectangle. The 
        ticks take some extra space.
    - colormap
    - ticks
    
  Parameters
  ══════════

    * name       
        str
        The colormap's name

    * colormap
        anim.colormap
        The colormap associated with the colorbar

    * title
        str, [*  str(*)]
        default: ''
        The colorbar title. HTML formating is supported by default.

    * group
        anim.plane.group
        default: None
        The colorbar's group. If None, the position of the reference point is in
        absolute coordinates. Otherwise, the positions are relative to the
        group's reference point.

    ─── dimensions ──────────────────────────────

    * Lx          
        float
        The colorbar rectangle width, i.e. length along the x axis when orientation
        is 0. 

    * Ly
        float
        The colorbar rectangle height, i.e.length along the y axis when orientation
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

    * center
        (bool, bool), [bool, bool], bool
        default: [True,True]
        Boolean defining the centering around the reference point. For tuple
        and list the first element is for the x-axis and the second is for 
        the y-axis.

    ─── transformations ─────────────────────────

    * draggable
        bool
        default: False
        Boolean specifying if the colorbar can be dragged. If True, the dragging
        callback is defined in the 'itemChange' method of the event class,
        which is transfered to the canva's 'event' method (recommended).

    ─── stack ───────────────────────────────────

    * zvalue
        float
        default: 0
        Z-value (stack order) of the colorbar.
  '''

  # ────────────────────────────────────────────────────────────────────────
  def __init__(self, 
               colormap,
               title = None,
               ticks_number = 2,
               ticks_precision = 2,
               group = None,
               x = 0,
               y = 0,
               position = None,
               Lx = None,
               Ly = None,
               dimension = None,
               center = [True, True],
               center_of_rotation = [0,0],
               orientation = 0,
               zvalue = 0,
               draggable = False):
    '''
    Colorbar item constructor
    '''  

    # ─── Parent constructor
    
    super().__init__(group = group,
                     position = points[0],
                     zvalue = zvalue,
                     draggable = draggable)
    
    # ─── Properties

    # General
    self._color = color

    # Path
    self._points = points
    self.init_thickness = thickness
    self.init_linestyle = linestyle
    self._path_color = path_color

    # Head
    self._head_position = None
    self._head_shape = head_shape
    self._head_segment = head_segment
    self._head_location = head_location
    self._head_color = head_color

    # Text
    self.init_string = str(string)
    self.init_fontname = fontname
    self._fontsize = fontsize
    self._text_segment = text_segment
    self._text_location = text_location
    self._text_color = text_color
    self.init_text_style = text_style
    
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
      points = [[0,0], [0,0]],
      thickness = self.init_thickness,
      stroke = self._color if self._path_color is None else self._path_color,      
      linestyle = self.init_linestyle
    )

    # ─── Head

    self.setHeadShape()

    # ─── String

    self.subitem.text = text(
      group = self,
      string = self.init_string,
      color = self._color if self._text_color is None else self._text_color,
      fontname = self.init_fontname,
      style = self.init_text_style
    )

    # ─── Geometry

    self.setGeometry()

  # ════════════════════════════════════════════════════════════════════════
  #                              SETTERS
  # ════════════════════════════════════════════════════════════════════════

  # ────────────────────────────────────────────────────────────────────────
  def setHeadShape(self):

    if 'head' in self.subitem and self.subitem.head.qitem is not None:
      self.canva.scene.removeItem(self.subitem.head.qitem)

    # Color
    color = self._color if self._head_color is None else self._head_color

    match self._head_shape:

      case 'dart':

        pts = np.array([[-8, -3], [0, 0], [-8, 3], [-6, 0]])*self.subitem.path.thickness/1.5

        self.subitem.head = polygon(
          group = self,
          points = pts,
          color = color,
        )

      case 'disk':

        self.subitem.head = circle(
          group = self,
          position = [0,0],
          radius = 2*self.subitem.path.thickness,
          color = color
        )

    # Update position
    self.setGeometry()

  # ────────────────────────────────────────────────────────────────────────
  def setGeometry(self):
    '''
    Arrow geometry

    * Sets the path points
    * Sets the arrow head position and orientation
    * Adjust the last path point to leave the arrowhead tip
    '''

    # ─── Positions

    # Set reference point
    self.position = self._points[0]

    # Relative points
    points = [[p[0]-self.position.x, p[1]-self.position.y] for p in self._points]

    # Thickness
    thickness = self.thickness

    # ─── Arrow head

    if 'head' in self.subitem and self.subitem.head.qitem is not None:

      # Segment number
      k = self._head_segment if self._head_segment>=0 else len(self.points)-2

      # Segment coordinates
      x0 = points[k][0]
      y0 = points[k][1]
      x1 = points[k+1][0]
      y1 = points[k+1][1]

      # Position
      x = x0 + (x1-x0)*self._head_location
      y = y0 + (y1-y0)*self._head_location
      self.subitem.head.position = [x,y]

      # Orientation
      if self._head_shape in ['dart']:
        self.subitem.head.orientation = np.angle(x1-x0 + 1j*(y1-y0))

      # Path tip adjustment
      if self._head_shape in ['dart']:
        r = np.sqrt((x1-x0)**2 + (y1-y0)**2)
        x = x0 + (x1-x0)*(r-thickness*3)/r
        y = y0 + (y1-y0)*(r-thickness*3)/r
        points[-1] = [x, y]

    # ─── Adjust arrow path

    # Path points
    self.subitem.path.points = points

    # ─── Text

    if 'text' in self.subitem and self.subitem.text.qitem is not None:

      # Fontsize
      fontsize = thickness*10 if self._fontsize is None else self._fontsize
      self.subitem.text.fontsize = fontsize

      # Segment number
      k = self._text_segment if self._text_segment>=0 else len(self.points)-2

      # Segment coordinates
      x0 = points[k][0]
      y0 = points[k][1]
      x1 = points[k+1][0]
      y1 = points[k+1][1]

      # Segment orientation
      a = np.angle(x1-x0 + 1j*(y1-y0))

      # Position
      r = fontsize/2*(1 if np.abs(a)<=np.pi/2 else -1)
      x = x0 + (x1-x0)*self._text_location - r*np.sin(a)
      y = y0 + (y1-y0)*self._text_location + r*np.cos(a)
      self.subitem.text.position = [x,y]

      # Orientation
      self.subitem.text.orientation = a if np.abs(a)<=np.pi/2 else a+np.pi

  # ════════════════════════════════════════════════════════════════════════
  #                             PROPERTIES
  # ════════════════════════════════════════════════════════════════════════

  # ─── path ───────────────────────────────────────────────────────────────

  # ─── points ──────────────────────────────────
  
  @property
  def points(self): return self.subitem.path.points

  @points.setter
  def points(self, P): 

    self._points = P

    # Update geometry
    self.setGeometry()

  # ─── thickness ───────────────────────────────
  
  @property
  def thickness(self): return self.subitem.path.thickness

  @thickness.setter
  def thickness(self, t): 
    self.subitem.path.thickness = t
    self.setGeometry()

  # ─── linestyle ───────────────────────────────
  
  @property
  def linestyle(self): return self.subitem.path.linestyle

  @thickness.setter
  def linestyle(self, s): self.subitem.path.linestyle = s

  # ─── color ───────────────────────────────────
  
  @property
  def path_color(self): return self.subitem.path.stroke

  @path_color.setter
  def path_color(self, c): self.subitem.path.stroke = c

  # ─── arrowhead ──────────────────────────────────────────────────────────
  
  # ─── shape ───────────────────────────────────

  @property
  def head_shape(self): return self._head_shape

  @head_shape.setter
  def head_shape(self, s):
    self._head_shape = s
    self.setHeadShape()

  # ─── segment ─────────────────────────────────
  
  @property
  def head_segment(self): return self._head_segment

  @head_segment.setter
  def head_segment(self, k): 
    self._head_segment = k
    self.setGeometry()

  # ─── location ────────────────────────────────

  @property
  def head_location(self): return self._head_location

  @head_location.setter
  def head_location(self, r):
    self._head_location = r
    self.setGeometry()

  # ─── color ───────────────────────────────────
  
  @property
  def head_color(self): return self.subitem.head.color

  @head_color.setter
  def head_color(self, c): self.subitem.head.color = c

  # ─── text ───────────────────────────────────────────────────────────────
  
  @property
  def string(self): return self.subitem.text.string

  @string.setter
  def string(self, s): self.subitem.text.string = str(s)

  # ─── color ───────────────────────────────────
  
  @property
  def text_color(self): return self.subitem.text.color

  @text_color.setter
  def text_color(self, c): self.subitem.text.color = c

  # ─── fontname ────────────────────────────────

  @property
  def fontname(self): return self.subitem.text.fontname

  @fontname.setter
  def fontname(self, s): self.subitem.text.fontname = s

  # ─── fontsize ────────────────────────────────

  @property
  def fontsize(self): return self.subitem.text.fontsize

  @fontsize.setter
  def fontsize(self, s):
    self.subitem.text.fontsize = s
    self.setGeometry()

  # ─── segment ─────────────────────────────────

  @property
  def text_segment(self): return self._text_segment

  @fontname.setter
  def text_segment(self, k):
    self._text_segment = k
    self.setGeometry()

  # ─── location ────────────────────────────────

  @property
  def text_location(self): return self._text_location

  @text_location.setter
  def text_location(self, r):
    self._text_location = r
    self.setGeometry()

  # ─── style ───────────────────────────────────

  @property
  def style(self): return self.subitem.text.style

  @style.setter
  def style(self, s): self.subitem.text.style = s

  # ─── color ──────────────────────────────────────────────────────────────
  
  @property
  def color(self): return self._color

  @color.setter
  def color(self, c):
    self._color = c
    if self._path_color is None: self.subitem.path.stroke = c
    if self._head_color is None: self.subitem.head.color = c
    if self._text_color is None: self.subitem.text.color = c
