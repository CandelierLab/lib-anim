import numpy as np

from PyQt6.QtGui import QColor, QPen
from PyQt6.QtWidgets import QGraphicsLineItem

class grid:

  # ────────────────────────────────────────────────────────────────────────
  def __init__(self, canva, spacing, shift=[0,0], color='grey', zvalue=-1):
    '''
    TO ADD: linestyle
    '''

    # ─── Definitions

    self.canva = canva
    self.spacing = spacing
    self.color = color
    self.zvalue = zvalue

    self._shift = shift

    # ─── Items ─────────────────────────────────

    nx = int(np.ceil(self.canva.boundaries.width/self.spacing))
    ny = int(np.ceil(self.canva.boundaries.height/self.spacing))

    x0 = self.canva.boundaries.x0*self.canva.pixelperunit
    y0 = self.canva.boundaries.y0*self.canva.pixelperunit
    x1 = self.canva.boundaries.x1*self.canva.pixelperunit
    y1 = self.canva.boundaries.y1*self.canva.pixelperunit

    for i in range(nx):
      
      x = x0 + i*spacing + self._shift[0] 
      line = QGraphicsLineItem(x, y0, x, y1)

      Pen = QPen()
      Pen.setColor(QColor(self.color))
      Pen.setWidthF(3)
      Pen.setCosmetic(True)
      line.setPen(Pen)

      line.setZValue(self.zvalue)

      self.canva.scene.addItem(line)

    for i in range(ny):
      
      y = y0 + i*spacing + self._shift[1] 
      line = QGraphicsLineItem(x0, y, x1, y)

      Pen = QPen()
      Pen.setColor(QColor(self.color))
      Pen.setWidthF(3)
      Pen.setCosmetic(True)
      line.setPen(Pen)

      line.setZValue(self.zvalue)

      self.canva.scene.addItem(line)