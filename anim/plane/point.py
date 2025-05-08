'''
Point in the plane

lowercase letters: absolute position, in user coordinates
uppercase letters: absolute position, in QGraphicsScene coordinates
'''

from copy import deepcopy

from .boundingBox import boundingBox

class point:
  '''
  Point in the plane
  '''

  # ────────────────────────────────────────────────────────────────────────
  def __init__(self, x, y, boundaries:boundingBox=None):

    # Relative position
    self.x = x
    self.y = y

    self.boundaries = boundaries

  # ────────────────────────────────────────────────────────────────────────
  def __str__(self):

    return f'═══ Point ({self.x},{self.y})'

  # ─── Scene position ─────────────────────────────────────────────────────
  
  ''' Position of the point in the QGraphicsScene '''

  @property
  def X(self): return self.x if self.boundaries is not None else None
   
  @property
  def Y(self): return self.boundaries.y1 - self.y if self.boundaries is not None else None