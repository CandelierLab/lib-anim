'''
2D grid demo
'''

import numpy as np
import anim

# ═══ 2D Animation canva ═══════════════════════════════════════════════════

class Canva(anim.plane.canva):

  # ────────────────────────────────────────────────────────────────────────
  def __init__(self, window):

    super().__init__(window, boundaries=[[-1,1], [-1,1]])

    self.pos = np.zeros((100, 2))

    # ─── Grid

    self.grid = anim.plane.grid(spacing = 0.4)

    # ─── Dot

    self.item.dot = anim.plane.circle(
      position = [0,0],
      radius = 0.02,
      color = 'red'
    )

    # ─── Tail

    self.item.tail = anim.plane.path(
      position = [0,0],
      points = self.pos,
      stroke = 'red'
    )

  # ────────────────────────────────────────────────────────────────────────
  def update(self, t):

    # ─── Update dot position

    new_pos = np.array(self.pos[-1]) + np.random.randn(2)/50
    self.pos = np.roll(self.pos, -1, axis=0)
    self.pos[-1] = new_pos

    self.item.dot.position = self.pos[-1,:]
    self.item.tail.points = self.pos

    # ─── Update grid

    self.grid.shift = np.mean(self.pos, axis=0)

    # Confirm update
    super().update(t)

# ═══ Main ═════════════════════════════════════════════════════════════════

W = anim.window('Grid animation')

# Add animation
W.add(Canva)

W.show() 