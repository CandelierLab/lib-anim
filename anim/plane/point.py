'''
Point in the plane
'''

from copy import deepcopy

from .boundingBox import boundingBox

class point:
  '''
  Point in the plane
  '''

  # ────────────────────────────────────────────────────────────────────────
  def __init__(self, x, y):

    # Relative position
    self.x_rel = x
    self.y_rel = y

    # Absolute position
    self._x_abs = None
    self._y_abs = None

    self.parent = None
    self.boundaries:boundingBox = None

  # ─── Absolute position ──────────────────────────────────────────────────

  ''' Absolute position of the point in the scene '''

  # ────────────────────────────────────────────────────────────────────────
  def setAbsolute(self):

    self._x_abs = self.x_rel
    self._y_abs = self.y_rel

    # ─── Check parenthood

    parent = self.parent
    # parent = deepcopy(self.parent)
    while parent is not None:

      # Shift position
      self._x_abs += parent.position.x_rel
      self._y_abs += parent.position.y_rel

      # Update parent
      parent = parent.parent

  @property
  def x_abs(self): 
    self.setAbsolute()
    return self.x_rel if self.parent is None else self.x_rel + self.parent.position.x_abs
   
  @property
  def y_abs(self): return self.y_rel if self.parent is None else self.y_rel + self.parent.position.y_abs

  # ─── Scene position ─────────────────────────────────────────────────────
  
  ''' Position of the point in the scene '''

  @property
  def scene_x(self): return self.x if self.boundaries is not None else None
   
  @property
  def scene_y(self): return self.boundaries.y1 - self.y if self.boundaries is not None else None