from PyQt6.QtCore import Qt, QObject, QRectF, pyqtSignal
from PyQt6.QtGui import QColor, QPainter, QPen, QColorConstants
from PyQt6.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsRectItem

import anim

# ══════════════════════════════════════════════════════════════════════════
#                              BOUNDING BOX
# ══════════════════════════════════════════════════════════════════════════

class boundingBox:

  # ────────────────────────────────────────────────────────────────────────
  def __init__(self, display, boundaries, color, thickness):
    '''
    Boundaries inputs are formated as [[x0,x1],[y0,y1]]
    '''

    self.display = display

    # ─── Reference points (bottom-left and top-right corners)

    # Default values
    if boundaries is None:
      self.x0 = 0
      self.x1 = 1
      self.y0 = 0
      self.y1 = 1
    else:
      self.x0 = boundaries[0][0]
      self.x1 = boundaries[0][1]
      self.y0 = boundaries[1][0]
      self.y1 = boundaries[1][1]
      
    # ─── Extension

    self.width = self.x1 - self.x0
    self.height = self.y1 - self.y0

    # ─── Aspect ratio

    self.aspect_ration = self.width/self.height

    # ─── Color

    self.color = color if color is not None else 'gray'

    # ─── Thickness

    self.thickness = thickness if thickness is not None else 1

# ══════════════════════════════════════════════════════════════════════════
#                                 VIEW
# ══════════════════════════════════════════════════════════════════════════

class GraphicsView(QGraphicsView):
    
  # ────────────────────────────────────────────────────────────────────────
  def __init__(self, scene, boundaries:boundingBox, padding=0, *args, **kwargs):

    # Parent constructor
    super().__init__(*args, *kwargs)

    # ─── View and scene

    self.padding = padding
    self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    # Antialiasing
    self.setRenderHints(QPainter.RenderHint.Antialiasing)

    # Scene
    self.setScene(scene)

    # ─── Boundaries

    self.boundaries = boundaries
    if self.boundaries.display:
      self.setStyleSheet(f'border: {self.boundaries.thickness}px solid {self.boundaries.color};')


  # ────────────────────────────────────────────────────────────────────────
  def fit(self):

    self.fitInView(QRectF(self.boundaries.x0 - self.padding,
                          self.boundaries.y1 - self.padding,
                          self.boundaries.width + 2*self.padding,
                          self.boundaries.height + 2*self.padding),
                   Qt.AspectRatioMode.KeepAspectRatio)

  # ────────────────────────────────────────────────────────────────────────
  def showEvent(self, E):

    self.fit()    
    super().showEvent(E)

  # ────────────────────────────────────────────────────────────────────────
  def resizeEvent(self, E):
    
    self.fit()
    super().resizeEvent(E)

# ══════════════════════════════════════════════════════════════════════════
#                                 PANEL
# ══════════════════════════════════════════════════════════════════════════

class panel(QObject):

  # Events
  signal = pyqtSignal()

  # ────────────────────────────────────────────────────────────────────────
  def __init__(self, window:anim.window,
               boundaries = None,
               display_boundaries = True, 
               boundaries_color = None,
               boundaries_thickness = None,
               padding = 0,
               background_color = None):
    '''
    Panel constructor
    '''

    # Parent constructor
    super().__init__()

    # ─── Scene boundaries

    self.boundaries = boundingBox(display_boundaries, boundaries, boundaries_color, boundaries_thickness)

    # ─── Qt elements

    # Window
    self.window = window

    # Scene
    self.scene = QGraphicsScene()    

    # View
    self.view = GraphicsView(self.scene, self.boundaries, padding=padding)
    
    # Scale factor
    self.factor = 1 # self.view.si/self.boundaries['height']

    # ─── Background color

    if background_color is not None:

      if isinstance(background_color, str):
        self.view.setBackgroundBrush(QColor(background_color))
      elif isinstance(background_color, QColor):
        self.view.setBackgroundBrush(background_color)
    
    # ─── Display items ────────────────────────────

    self.item = {}
    self.composite = {}
    
    # Stack
    self.stack = {'vpos': self.boundaries.y1, 
                  'vmin': self.boundaries.y0,
                  'vpadding': 0.02}
    
  # ────────────────────────────────────────────────────────────────────────
  def add(self, type, name, **kwargs):
    '''
    Add an item to the scene.
    '''

    # Stack
    if 'stack' in kwargs:
      stack = kwargs['stack']
      del kwargs['stack']
    else:
      stack = False

    height = kwargs['height'] if 'height' in kwargs else None

    if height=='fill':
      height = self.stack['vpos']-self.boundaries['y'][0]
      kwargs['height'] = height
      
    # Add items
    if issubclass(type, anim.plane.composite):

      # Let composite elements create their own items
      self.composite[name] = type(self, name, **kwargs)

    else:

      # Create item
      self.item[name] = type(self, name, **kwargs)

      # Add item to the scene
      if self.item[name].parent is None:
        self.scene.addItem(self.item[name])
    
    # --- Stack

    if stack:

      x = 0
      y = self.stack['vpos']

      if height is None:
        self.stack['vpos'] -= self.item[name].height()
      else:
        self.stack['vpos'] -= height
        y -= height

      # Set position
      self.item[name].position = [x, y]

      # Bottom padding
      self.stack['vpos'] -= kwargs['vpadding'] if 'vpadding' in kwargs else self.stack['vpadding']

  # ────────────────────────────────────────────────────────────────────────
  def update(self, t=None):
    """
    Update animation state
    """

    # Repaint
    self.view.viewport().repaint()

    # Confirm update
    self.signal.emit()

  # ────────────────────────────────────────────────────────────────────────
  def receive(self, event):
    """
    Event reception
    """

    match event['type']:

      case 'show':
        
        for name in self.composite:
          if isinstance(self.composite[name], anim.plane.arrow):
            self.composite[name].points = self.composite[name].points

      case 'update':

        # Update dispay
        self.update(event['time'])

      case 'stop':
        self.stop()

      case _:
        # print(event)
        pass
        
  # ────────────────────────────────────────────────────────────────────────
  def change(self, type, item):
    '''
    Change notification

    This method is triggered whenever an item is changed.
    It does nothing and has to be reimplemented in subclasses.

    .. Note::
      To catch motion an item has to be declared as ``movable``,
      which is not the default.

    args:
      type (str): Type of change (``move``).
      item (:class:`item` *subclass*): The changed item.
    '''

    pass
  
  # ────────────────────────────────────────────────────────────────────────
  def stop(self):
    '''
    Stop notification

    This method is triggered when the window is closed.
    It does nothing and has to be reimplemented in subclasses.
    '''

    pass
