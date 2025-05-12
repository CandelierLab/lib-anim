'''
Point in the plane

lowercase letters: absolute position, in user coordinates
uppercase letters: absolute position, in QGraphicsScene coordinates
'''

from copy import deepcopy

class point:
  '''
  Point in the plane
  '''

  # ────────────────────────────────────────────────────────────────────────
  def __init__(self, x, y):

    # Relative position
    self.x = x
    self.y = y

    self.shift = [0, 0]

  # ────────────────────────────────────────────────────────────────────────
  def __str__(self):

    return f'═══ Point ({self.x},{self.y})'

  # ─── Scene position ─────────────────────────────────────────────────────
  
  ''' Position of the point in the QGraphicsScene '''

  @property
  def X(self): return self.x + self.shift[0]
   
  @property
  def Y(self): return self.y + self.shift[1]