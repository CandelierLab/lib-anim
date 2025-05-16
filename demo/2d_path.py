'''
2D path demo
'''

import numpy as np
import anim

# ═══ 2D Animation ═════════════════════════════════════════════════════════

class Canva(anim.plane.canva):

  # ────────────────────────────────────────────────────────────────────────
  def __init__(self, window, **kwargs):

    super().__init__(window)

    # ─── Definitions

    # Number of points
    self.N = 50

    # ─── Items

    self.item.P = anim.plane.path(
      points = self.generate(0),
      color = 'lemonchiffon',
      stroke = 'orange'
    )

  # ────────────────────────────────────────────────────────────────────────
  def generate(self, t):

    P = []
    for x in range(self.N):
      P.append([0.1+x*0.8/(self.N-1),
                0.5 + np.sin(x*20/self.N + t/20)/5])

    return P

  # ────────────────────────────────────────────────────────────────────────
  def update(self, t):

    # Update timer display
    super().update(t)

    self.item.P.points = self.generate(t.step)

# ═══ Main ═════════════════════════════════════════════════════════════════

import os
os.system('clear')

W = anim.window('Simple animation', display_information=False)

# Add animation
W.add(Canva)

# Allow backward animation
W.allow_backward = True
W.allow_negative_time = True

W.show()