'''
2D circle demo
'''

import numpy as np
import anim

# ═══ 2D Animation canva ═══════════════════════════════════════════════════

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
        
        self.item[f'circle_{i}_{j}'] = anim.plane.circle(
          position = [i*self.b, j*self.b],
          radius = 0,
          color = 'cyan' if (i+j)%2 else 'blue'
        )
    

  # ────────────────────────────────────────────────────────────────────────
  def update(self, t):

    for i in range(self.a):
      for j in range(self.a):

        shift = ((i + j) % 2)*np.pi/2
        self.item[f'circle_{i}_{j}'].radius = self.b*(np.cos(t.step/30 + shift)*np.sqrt(2))/2

    # Confirm update
    super().update(t)

# ═══ Main ═════════════════════════════════════════════════════════════════

W = anim.window('Circle animation')

# Add animation
W.add(Canva)

# Allow backward animation
W.allow_backward = True
W.allow_negative_time = True

W.show()