from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtGui import QColor, QPen
from PyQt6.QtWidgets import QGraphicsScene, QGraphicsRectItem

import anim
from .graphicsView import graphicsView
from .boundingBox import boundingBox
from .itemDict import itemDict
from .grid import grid as canva_grid

class canva(QObject):

  # Events
  signal = pyqtSignal()

  # ────────────────────────────────────────────────────────────────────────
  def __init__(self, window:anim.window,
               boundaries = None,
               display_boundaries = True, 
               boundaries_color = None,
               boundaries_thickness = None,
               padding = 0,
               background_color = None,
               pixelperunit = 1,
               coordinates = 'xy',
               grid = None):
    '''
    Canva constructor
    '''

    # Parent constructor
    super().__init__()

    # Window
    self.window = window

    # ─── Scene boundaries

    if boundaries_color is None:
      match self.window.style:
        case 'white' | 'light': boundaries_color = 'black'
        case _: boundaries_color = 'white'
    
    self._boundaries = boundingBox(display_boundaries, boundaries, boundaries_color, boundaries_thickness)

    # ─── Qt elements

    # Scene
    self.scene = QGraphicsScene()  

    # View
    self.view = graphicsView(self.scene, self.boundaries, pixelperunit, padding=padding)

    # Coordinates
    self.coordinates = coordinates
    if self.coordinates=='xy': self.view.scale(1,-1)

    # Pixels per scene unit
    self.pixelperunit = pixelperunit
    
    # ─── Background color

    if background_color is not None:

      if isinstance(background_color, str):
        self.view.setBackgroundBrush(QColor(background_color))
      elif isinstance(background_color, QColor):
        self.view.setBackgroundBrush(background_color)
    
    # ─── Display items ────────────────────────────

    self.item = itemDict(self) 
      
    # ─── Dummy boundary rectangle ──────────────

    self.bounds = QGraphicsRectItem(self.boundaries.x0*self.pixelperunit, 
                               self.boundaries.y0*self.pixelperunit,
                               self.boundaries.width*self.pixelperunit,
                               self.boundaries.height*self.pixelperunit)
    
    self.scene.addItem(self.bounds)
    self.setBoundaryStyle()

    # ─── Grid ──────────────────────────────────

    self._grid = canva_grid(self, spacing=0.25,) if grid is True else grid
  
  # ────────────────────────────────────────────────────────────────────────
  def setBoundaryStyle(self):
    '''
    Sets the boundary style
    '''

    Pen = QPen()
    Pen.setColor(QColor(self.boundaries.color))
    Pen.setWidthF(0)
    Pen.setCosmetic(True)
    self.bounds.setPen(Pen)
    self.bounds.setVisible(self.boundaries.display)

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

    match event.type:

      case 'show':
        
        pass

      case 'update':

        # Update dispay
        self.update(event.time)

      case 'stop':
        self.stop()

      case _:
        # print(event)
        pass
        
  # ────────────────────────────────────────────────────────────────────────
  def event(self, item, desc):
    '''
    Event notification

    This method is triggered whenever an event occurs.
    It has to be reimplemented in subclasses.

    args:
      type (str): Event type (``move``).
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

  # ─── grid ───────────────────────────────────────────────────────────────

  @property
  def grid(self): return self._grid

  @grid.setter
  def grid(self, g):
    self._grid = g
    self._grid.canva = self
    self._grid.initialize()

  # ─── Boundaries ─────────────────────────────────────────────────────────

  @property
  def boundaries(self): return self._boundaries

  @boundaries.setter
  def boundaries(self, B):

    self._boundaries = boundingBox(self._boundaries.display,
                                   B,
                                   self._boundaries.color, 
                                   self._boundaries.thickness)
    
    # Update view
    self.view.boundaries = self.boundaries
    self.view.fit()

    # Update bounds
    self.bounds.setRect(self.boundaries.x0*self.pixelperunit,
                        self.boundaries.y0*self.pixelperunit,
                        self.boundaries.width*self.pixelperunit,
                        self.boundaries.height*self.pixelperunit)
    
  # ─── Boundary display ───────────────────────────────────────────────────

  @property
  def display_boundaries(self): return self.boundaries.display

  @display_boundaries.setter
  def display_boundaries(self, b):
    self.boundaries.display = b
    self.setBoundaryStyle()