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
    self.a = 10

    # Mesh size
    self.b = 1/(self.a-1)

    for i in range(self.a):
      for j in range(self.a):
        
        self.item[f'ellipse_{i}_{j}'] = anim.plane.ellipse(
          position = [i*self.b, j*self.b],
          dimension = [0,0],
          color = 'cyan' if (i+j)%2 else 'blue'
        )
    
  # ────────────────────────────────────────────────────────────────────────
  def update(self, t):

    # Update timer display
    super().update(t)

    for i in range(self.a):
      for j in range(self.a):

        L = self.b*(1 + np.cos(t.step/20)/2)
        self.item[f'ellipse_{i}_{j}'].dimension = [L, 2*self.b-L] if (i+j)%2 else [2*self.b-L, L]

# ═══ Main ═════════════════════════════════════════════════════════════════

import os
os.system('clear')

W = anim.window('Ellipse animation', display_information=False)

# Add animation
W.add(Canva)

# Allow backward animation
W.allow_backward = True
W.allow_negative_time = True

W.show()