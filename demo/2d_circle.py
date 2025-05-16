'''
Complete 2d demo
'''

import numpy as np
import anim

# ═══ 2D Animation ═════════════════════════════════════════════════════════

class Canva(anim.plane.canva):

  # ────────────────────────────────────────────────────────────────────────
  def __init__(self, window, **kwargs):

    super().__init__(window, 
                     boundaries = [[0, 1],[0,1]],
                     display_boundaries = True,    
                     **kwargs)

    # Number of ellipse per axis
    self.a = 4

    # Mesh size
    self.b = 1/(self.a-1)

    for i in range(self.a):
      for j in range(self.a):
        
        self.item[f'ellipse_{i}_{j}'] = anim.plane.ellipse(
          position = [i*self.b, j*self.b],
          dimension = [0,0]
        )
    

  # ────────────────────────────────────────────────────────────────────────
  def update(self, t):

    # Update timer display
    super().update(t)

    for i in range(self.a):
      for j in range(self.a):

        shift = ((i + j) % 2)*np.pi/2

        self.item[f'ellipse_{i}_{j}'].dimension = [
          self.b*(abs(np.cos(t.step/50 + shift)*np.sqrt(2))),
          self.b*(abs(np.cos(t.step/50 + shift)*np.sqrt(2))),
        ]


# ═══ Main ═════════════════════════════════════════════════════════════════

import os
os.system('clear')

W = anim.window('Ellispe animation', display_information=False)

# Add animation
W.add(Canva)

# Allow backward animation
W.allow_backward = True
W.allow_negative_time = True

W.show()