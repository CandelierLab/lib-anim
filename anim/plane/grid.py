import numpy as np

from PyQt6.QtGui import QColor, QPen
from PyQt6.QtWidgets import QGraphicsLineItem

class grid:

  # ────────────────────────────────────────────────────────────────────────
  def __init__(self,
               spacing = None,
               shift=[0,0],
               color='grey',
               zvalue=-1):
    '''
    TO ADD: linestyle
    '''

    # ─── Definitions

    self.canva = None
    self.spacing = spacing
    self.color = color
    self.thickness = 2
    self.zvalue = zvalue

    self._shift = shift

  # ────────────────────────────────────────────────────────────────────────
  def initialize(self):
    '''
    Create the QGraphicsLineItems
    '''

    # Check
    if self.canva is None: return

    # Default spacing
    if self.spacing is None:
      self.spacing = self.canva.boundaries.width/4

    # ─── Items ─────────────────────────────────

    self.nx = int(np.ceil(self.canva.boundaries.width/self.spacing))
    self.ny = int(np.ceil(self.canva.boundaries.height/self.spacing))

    self.x0 = self.canva.boundaries.x0*self.canva.pixelperunit
    self.y0 = self.canva.boundaries.y0*self.canva.pixelperunit
    self.x1 = self.canva.boundaries.x1*self.canva.pixelperunit
    self.y1 = self.canva.boundaries.y1*self.canva.pixelperunit

    self.line_x = []
    self.line_y = []

    for i in range(self.nx):
      
      line = QGraphicsLineItem()

      Pen = QPen()
      Pen.setColor(QColor(self.color))
      Pen.setWidthF(self.thickness)
      Pen.setCosmetic(True)
      line.setPen(Pen)

      line.setZValue(self.zvalue)

      self.line_x.append(line)
      self.canva.scene.addItem(line)

    for i in range(self.ny):
      
      line = QGraphicsLineItem()

      Pen = QPen()
      Pen.setColor(QColor(self.color))
      Pen.setWidthF(self.thickness)
      Pen.setCosmetic(True)
      line.setPen(Pen)

      line.setZValue(self.zvalue)

      self.line_y.append(line)
      self.canva.scene.addItem(line)

    # Set line geometry
    self.setLines()

  # ════════════════════════════════════════════════════════════════════════
  #                              SETTERS
  # ════════════════════════════════════════════════════════════════════════

  # ────────────────────────────────────────────────────────────────────────
  def setLines(self):
    '''
    Sets the line positions
    '''

    for i in range(self.nx):
      
      # Shifted position
      x = self.x0 + i*self.spacing + self._shift[0] 

      # Periodic conditions
      x = ((x - self.x0) % self.canva.boundaries.width) + self.x0

      self.line_x[i].setLine(x, self.y0, x, self.y1)

    for i in range(self.ny):
      
      # Shifted position
      y = self.y0 + i*self.spacing + self._shift[1] 

      # Periodic conditions
      y = ((y - self.y0) % self.canva.boundaries.height) + self.y0

      self.line_y[i].setLine(self.x0, y, self.x1, y)


  # ─── shift ──────────────────────────────────────────────────────────────

  @property
  def shift(self): return self._shift

  @shift.setter
  def shift(self, s):
    self._shift = s
    self.setLines()
