'''
2D path demo
'''

import numpy as np
import anim

# ═══ 2D Animation ═════════════════════════════════════════════════════════

class Canva(anim.plane.canva):

  # ────────────────────────────────────────────────────────────────────────
  def __init__(self, window):

    super().__init__(window, boundaries = [[-1, 1], [-1, 1]])

    # ─── Items

    self.item.P = anim.plane.polygon(
      points = self.generate(0),
      color = None,
      stroke = 'pink',
      thickness = 0.02
    )

  # ────────────────────────────────────────────────────────────────────────
  def generate(self, t):

    # Number of points
    Z = 2 + t/20
    N = int(Z)

    P = []
    for i in range(N):
      P.append([np.cos(i*2*np.pi/Z)*0.8,
                np.sin(i*2*np.pi/Z)*0.8])

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
W.allow_negative_time = False

W.show()