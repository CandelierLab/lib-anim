'''
2D path demo
'''

import numpy as np
import anim

# ═══ 2D Animation canva ═══════════════════════════════════════════════════

class Canva(anim.plane.canva):

  # ────────────────────────────────────────────────────────────────────────
  def __init__(self, window, **kwargs):

    super().__init__(window)

    # ─── Definitions

    # Number of points
    self.N = 30

    # ─── Items

    self.item.P = anim.plane.path(
      position = [0.5, 0.5],
      points = self.generate(0),
      color = 'lemonchiffon',
      stroke = 'orange'
    )

  # ────────────────────────────────────────────────────────────────────────
  def generate(self, t):

    P = []
    for x in range(self.N):
      P.append([0.4*(2*x/(self.N-1)-1),
                np.sin(x*20/self.N + t/20)/5])

    return P

  # ────────────────────────────────────────────────────────────────────────
  def update(self, t):

    self.item.P.points = self.generate(t.step)

    # Confirm update
    super().update(t)

# ═══ Main ═════════════════════════════════════════════════════════════════

W = anim.window('Simple animation')

# Add animation
W.add(Canva)

# Allow backward animation
W.allow_backward = True
W.allow_negative_time = True

W.show()