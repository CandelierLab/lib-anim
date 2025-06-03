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

    # ─── Scene boundaries

    self.boundaries = boundingBox(display_boundaries, boundaries, boundaries_color, boundaries_thickness)

    # ─── Qt elements

    # Window
    self.window = window

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
    self.composite = {}
    
    # Stack
    # self.stack = {'vpos': self.boundaries.y1, 
    #               'vmin': self.boundaries.y0,
    #               'vpadding': 0.02}
    
    # ─── Dummy boundary rectangle ──────────────

    bounds = QGraphicsRectItem(self.boundaries.x0*self.pixelperunit, 
                               self.boundaries.y0*self.pixelperunit,
                               self.boundaries.width*self.pixelperunit,
                               self.boundaries.height*self.pixelperunit)
    
    Pen = QPen()
    if self.boundaries.display:
      Pen.setColor(QColor(self.boundaries.color))
    Pen.setWidthF(0)
    Pen.setCosmetic(True)
    bounds.setPen(Pen)

    self.scene.addItem(bounds)

    # ─── Grid ──────────────────────────────────

    self._grid = canva_grid(self, spacing=0.25,) if grid is True else grid
  
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
        
        for name in self.composite:
          if isinstance(self.composite[name], anim.plane.arrow):
            self.composite[name].points = self.composite[name].points

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