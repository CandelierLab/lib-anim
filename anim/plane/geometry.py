'''
GEOMETRICAL OBJECTS

- Vector of 2D coordinates
- Point in the plane

lowercase letters: absolute position, in user coordinates
uppercase letters: absolute position, in QGraphicsScene coordinates
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

      elif isinstance(x, (tuple, list)):

        # Doublet input
        self.x = x[0]  
        self.y = x[1]

      else:
        raise TypeError('Vectors can be defined with complex, tuples or lists.') 

    else:

      self.x = x
      self.y = y

# ══════════════════════════════════════════════════════════════════════════
#                                   POINT
# ══════════════════════════════════════════════════════════════════════════

class point(vector):
  '''
  Point in the plane
  '''

  # ────────────────────────────────────────────────────────────────────────
  def __init__(self, x, y=None):

    # Parent constructor
    super().__init__(x, y)

    # Shifts
    self.shift = vector(0,0)

  # ────────────────────────────────────────────────────────────────────────
  def __str__(self):

    s = '═══ Point\n'
    s += f'initial: ({self.x},{self.y})\n'
    s += f'shift: ({self.shift.x},{self.shift.y})\n'
    s += f'scene position: ({self.X},{self.Y})'

    return s

  # ─── Scene position ─────────────────────────────────────────────────────
  
  ''' Position of the point in the QGraphicsScene '''

  @property
  def X(self): return self.x + self.shift.x
   
  @property
  def Y(self): return self.y + self.shift.y

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

#     s = '═══ Point\n'
#     s += f'initial: ({self.x},{self.y})\n'
#     for k, v in self.shift.items():
#       s += f'shift {k}: ({v.x},{v.y})\n'
#     s += f'scene position: ({self.X},{self.Y})'

#     return s

#   # ─── Scene position ─────────────────────────────────────────────────────
  
#   ''' Position of the point in the QGraphicsScene '''

#   @property
#   def X(self): return sum([v.X for v in self.shift.values()], self.x)
   
#   @property
#   def Y(self): return sum([v.Y for v in self.shift.values()], self.y)