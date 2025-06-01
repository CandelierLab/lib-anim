from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtGui import QColor, QPen
from PyQt6.QtWidgets import QGraphicsScene, QGraphicsRectItem

import anim
from .graphicsView import graphicsView
from .boundingBox import boundingBox

from .itemDict import itemDict

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
               coordinates = 'xy'):
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

    # Number/spacing
    # Color
    # Shift
    # Zvalue: -1

  # # ────────────────────────────────────────────────────────────────────────
  # def add(self, type, name, **kwargs):
  #   '''
  #   Add an item to the scene.
  #   '''

  #   # Stack
  #   if 'stack' in kwargs:
  #     stack = kwargs['stack']
  #     del kwargs['stack']
  #   else:
  #     stack = False

  #   height = kwargs['height'] if 'height' in kwargs else None

  #   if height=='fill':
  #     height = self.stack['vpos']-self.boundaries['y'][0]
  #     kwargs['height'] = height
      
  #   # ─── Add element ───────────────────────────

  #   if issubclass(type, anim.plane.composite):

  #     ''' COMPOSITES '''

  #     # Let composite elements create their own items
  #     self.composite[name] = type(self, name, **kwargs)

  #   else:

  #     ''' ITEMS '''

  #     # Create item
  #     self.item[name] = type(self, name, **kwargs)

  #     # Add item to the scene
  #     if self.item[name].parent is None:
  #       self.scene.addItem(self.item[name])
    
  #   # Place the item on the canva (once created)
  #   self.item[name].init_display()

  #   # ─── Stack ─────────────────────────────────

  #   if stack:

  #     x = 0
  #     y = self.stack['vpos']

  #     if height is None:
  #       self.stack['vpos'] -= self.item[name].height()
  #     else:
  #       self.stack['vpos'] -= height
  #       y -= height

  #     # Set position
  #     self.item[name].position = [x, y]

  #     # Bottom padding
  #     self.stack['vpos'] -= kwargs['vpadding'] if 'vpadding' in kwargs else self.stack['vpadding']

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