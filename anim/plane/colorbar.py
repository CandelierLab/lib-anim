import numpy as np
from PyQt6.QtGui import QLinearGradient

from .group import composite
from .rectangle import rectangle
from .polygon import polygon
from .text import text
from ..colormap import colormap as anim_colormap

class colorbar(composite):
  '''
  Colorbar item (composite)

  ### /!\ ### /!\ ### /!\ ### /!\ ### /!\ ### /!\ ### /!\ ### /!\ ### /!\ ###

  !! This is not finished !!

  ### /!\ ### /!\ ### /!\ ### /!\ ### /!\ ### /!\ ### /!\ ### /!\ ### /!\ ###
  
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

    ─── ticks ───────────────────────────────────

    * ticks_number
        int >1
        default: 2
        Number of ticks to display. This property cannot be changed dynamically 
        after the initialization of the colorbar.

    * ticks_precision
        int >=0
        default: 2
        Number of precision digits for the ticks

    * ticks_color
        str, QColor
        default: 'grey'
        Color of the ticks and colorbar contour.

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

    ─── style ────────────────────────────────

    * ticks_fontname
        str
        default: 'Helvetica'
        Ticks font name

    * ticks_fontsize
        float
        default: 0.05
        Ticks font size, in scene units.

    * ticks_style
        str
        default: ''
        Ticks css style sheet. Global styling is accessed
        through the html selector.
        Example: 'html { background-color: yellow; }'
  '''

  # ────────────────────────────────────────────────────────────────────────
  def __init__(self, 
               colormap,
               title = None,
               ticks_color = 'grey',
               ticks_number = 2,
               ticks_precision = 2,
               ticks_fontname = 'Helvetica',
               ticks_fontsize = 0.05,
               ticks_style = '',
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
                  x = x,
                  y = y,
                  position = position,
                  center_of_rotation = center_of_rotation,
                  orientation = orientation,
                  zvalue = zvalue,
                  draggable = draggable)
    
    # ─── Internal properties

    # Colormap
    self._colormap:anim_colormap = colormap

    # Rectangle attributes
    self.init_dimension = dimension
    self.init_center = center

    if dimension is not None and isinstance(dimension, (tuple, list, complex)):
      self.init_Lx = None
      self.init_Ly = None    

    elif Lx is None or Ly is None:
      raise AttributeError("Colormap dimensions must be specified, either with 'dimension' or with 'Lx' and 'Ly'.")
      
    else:
      self.init_Lx = Lx
      self.init_Ly = Ly

    # Ticks
    self._ticks_number = ticks_number
    self._ticks_precision = ticks_precision
    self._ticks_color = ticks_color
    self._ticks_fontname = ticks_fontname
    self._ticks_fontsize = ticks_fontsize
    self._ticks_style = ticks_style

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

    # ─── Rectangle ─────────────────────────────

    self.subitem.rect = rectangle(
      group = self,
      position = self.position,
      Lx = self.init_Lx,
      Ly = self.init_Ly,
      dimension = self.init_dimension,
      center = self.init_center,
      color = None,
      stroke = self.ticks_color
    )

    # ─── Ticks ─────────────────────────────────

    tp = np.linspace(0, 1, self.ticks_number)
    
    for k, u in enumerate(tp):

      v = self.colormap.range[0] + u*(self.colormap.range[1]-self.colormap.range[0])
      y = u*self.Ly - (self.Ly/2 if self.center[1] else 0)

      # ─── Text

      self.subitem[f'tick_{k}_text'] = text(
        group = self,
        position = [0, y],
        string = f'{v:.{self._ticks_precision}f}',
        color = self.ticks_color,
        fontsize = 0.025,
        center = (False, True))
  
      # ─── Triangle

      self.subitem[f'tick_{k}_marker'] = polygon(
        group = self,
        position = [0, y],
        points = [[0,0]]*3,
        color = 'white',
        stroke = self.ticks_color,
        thickness = 0
      )

    # ─── Set colormap ──────────────────────────

    self.setColormap()

  # ════════════════════════════════════════════════════════════════════════
  #                              SETTERS
  # ════════════════════════════════════════════════════════════════════════

  # ────────────────────────────────────────────────────────────────────────
  def setColormap(self):
    '''
    Sets the colormap grandient in the rectangle item
    '''

    g = QLinearGradient(
      self.subitem.rect.qitem.boundingRect().topLeft(),
      self.subitem.rect.qitem.boundingRect().bottomLeft()
      )
    
    for z in np.linspace(0, 1, self.colormap.ncolors):      
      g.setColorAt(z, self.colormap.qcolor(z, scaled=True))
  
    self.subitem.rect.qitem.setBrush(g)    

    # Set geometry
    self.setGeometry()

  # ────────────────────────────────────────────────────────────────────────
  def setGeometry(self):
    '''
    Colorbar geometry
    '''
    # ─── Ticks

    s = self.ticks_fontsize/4
    v = np.linspace(self.colormap.range[0], self.colormap.range[1], self.ticks_number)

    for k in range(self.ticks_number):

      # Text x-position
      self.subitem[f'tick_{k}_text'].x = - self.subitem[f'tick_{k}_text'].Lx()*1.25 - self.Lx/2 - s

      # Triangles
      self.subitem[f'tick_{k}_marker'].x = -self.Lx/2 - s/4
      self.subitem[f'tick_{k}_marker'].points = [[0,0], [-s,-s/2], [-s,s/2]]
      self.subitem[f'tick_{k}_marker'].color = self.colormap.qcolor(v[k])

  # ════════════════════════════════════════════════════════════════════════
  #                             PROPERTIES
  # ════════════════════════════════════════════════════════════════════════

  # ─── colormap ───────────────────────────────────────────────────────────

  @property
  def colormap(self): return self._colormap

  @colormap.setter
  def colormap(self, C): 
    self._colormap = C
    self.setColormap()

  # ─── Rectangle ──────────────────────────────────────────────────────────
 
  @property
  def Lx(self): return self.subitem.rect.Lx

  @Lx.setter
  def Lx(self, w): self.subitem.rect.Lx = w
  
  @property
  def Ly(self): return self.subitem.rect.Ly

  @Ly.setter
  def Ly(self, w): self.subitem.rect.Ly = w

  @property
  def dimension(self): return self.subitem.rect.dimension

  @dimension.setter
  def dimension(self, D): self.subitem.rect.dimension = D

  @property
  def center(self): return self.subitem.rect.center

  @center.setter
  def center(self, C): self.subitem.rect.center = C

  # ─── Ticks ──────────────────────────────────────────────────────────────

  # ─── number ──────────────────────────────────

  @property
  def ticks_number(self): return self._ticks_number

  @ticks_number.setter
  def ticks_number(self, n):

    self._ticks_number = n
    self.setGeometry()

  # ─── style ───────────────────────────────────

  @property
  def ticks_fontname(self): return self._ticks_fontname

  @ticks_fontname.setter
  def ticks_fontname(self, s):
    self._ticks_fontname = s
    for k in range(self.ticks_number): self.subitem[f'tick_{k}_text'].fontname = s

  @property
  def ticks_fontsize(self): return self._ticks_fontsize

  @ticks_fontsize.setter
  def ticks_fontsize(self, s):
    self._ticks_fontsize = s
    for k in range(self.ticks_number): self.subitem[f'tick_{k}_text'].fontsize = s


  @property
  def ticks_color(self): return self._ticks_color

  @ticks_color.setter
  def ticks_color(self, c):

    self._ticks_color = c

    # Rectangle stroke
    self.subitem.rect.stroke = c

    # Tick text
