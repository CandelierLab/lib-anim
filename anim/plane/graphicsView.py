from PyQt6.QtCore import Qt, QRectF, QPointF
from PyQt6.QtGui import QPainter
from PyQt6.QtWidgets import QGraphicsView

from .boundingBox import boundingBox

class graphicsView(QGraphicsView):
    
  # ────────────────────────────────────────────────────────────────────────
  def __init__(self, scene, boundaries:boundingBox, pixelperunit, padding=0, *args, **kwargs):

    # Parent constructor
    super().__init__(*args, *kwargs)

    # ─── View and scene

    self.ppu = float(pixelperunit)
    self.padding = padding

    # Disable scrollbars
    self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    # Antialiasing
    self.setRenderHints(QPainter.RenderHint.Antialiasing)

    # Scene
    self.setScene(scene)

    # ─── Boundaries

    self.boundaries = boundaries
    # if self.boundaries.display:
    #   self.setStyleSheet(f'border: {self.boundaries.thickness}px solid {self.boundaries.color};')

  # ────────────────────────────────────────────────────────────────────────
  def fit(self):

    self.fitInView(QRectF(0, 0,
                          (self.boundaries.width + 2*self.padding)*self.ppu,
                          (self.boundaries.height + 2*self.padding)*self.ppu),
                   Qt.AspectRatioMode.KeepAspectRatio)
    
    # self.centerOn(QPointF(self.boundaries.x0 + self.boundaries.width/2,
    #                       self.boundaries.y0 + self.boundaries.height/2))
    
    self.setSceneRect(QRectF((self.boundaries.x0 - self.padding)*self.ppu,
                             (self.boundaries.y0 - self.padding)*self.ppu,
                             (self.boundaries.width + 2*self.padding)*self.ppu,
                             (self.boundaries.height + 2*self.padding)*self.ppu))
    
    # self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.NoViewportUpdate)

  # ────────────────────────────────────────────────────────────────────────
  def showEvent(self, event):

    self.fit()    
    super().showEvent(event)

  # ────────────────────────────────────────────────────────────────────────
  def resizeEvent(self, event):
    
    self.fit()
    super().resizeEvent(event)

  # ────────────────────────────────────────────────────────────────────────
  def wheelEvent(self, event):
    '''
    Capture the wheel events to avoid scene motion.
    '''
    pass