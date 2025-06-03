'''
GEOMETRICAL OBJECTS

- Vector of 2D coordinates
'''

import numpy as np

# ══════════════════════════════════════════════════════════════════════════
#                                   VECTOR
# ══════════════════════════════════════════════════════════════════════════

class vector:

  # ────────────────────────────────────────────────────────────────────────
  def __init__(self, x, y=None):
    ''' 
    Set of 2 coordinates
    '''

    # ─── Input heterogeneity

    if y is None:

      if isinstance(x, complex):

        # Convert from complex coordinates
        self.x = np.real(x)
        self.y = np.imag(x)

      elif isinstance(x, (tuple, list, np.ndarray)):

        # Doublet input
        self.x = x[0]  
        self.y = x[1]

      else:
        raise TypeError(f'A {self.__class__.__name__} can be defined with complex, tuples or lists.') 

    else:

      self.x = x
      self.y = y

  # ────────────────────────────────────────────────────────────────────────
  def __str__(self):

    return f'[vector] ({self.x},{self.y})'

# ══════════════════════════════════════════════════════════════════════════
#                                 POSITION
# ══════════════════════════════════════════════════════════════════════════

class position(vector):

  # ────────────────────────────────────────────────────────────────────────
  def __init__(self, x, y=None, absolute=True):
    ''' 
    Position
    '''

    super().__init__(x, y)

    self.absolute = absolute

  # ────────────────────────────────────────────────────────────────────────
  def __str__(self):

    q = 'absolute' if self.absolute else 'relative'
    return f'[{q} position] ({self.x},{self.y})'

# # ══════════════════════════════════════════════════════════════════════════
# #                                   POINT
# # ══════════════════════════════════════════════════════════════════════════

# class point(vector):
#   '''
#   Point in the plane
#   '''

#   # ────────────────────────────────────────────────────────────────────────
#   def __init__(self, x, y=None):

#     # Parent constructor
#     super().__init__(x, y)

#     # Shifts
#     self.shift = {}

#   # ────────────────────────────────────────────────────────────────────────
#   def __str__(self):

#     s = '═══ Point: '
#     s += f'({self.x},{self.y})'
#     for k, v in self.shift.items():
#       s += f' + shift_{k} ({v.x},{v.y})'
#     s += f' = ({self.X},{self.Y})'

#     return s

#   # ─── Scene position ─────────────────────────────────────────────────────
  
#   ''' Position of the point in the QGraphicsScene '''

#   @property
#   def X(self): return sum([v.x for v in self.shift.values()], self.x)
   
#   @property
#   def Y(self): return sum([v.y for v in self.shift.values()], self.y)