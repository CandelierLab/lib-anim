'''
2D grid demo
'''

import numpy as np
import anim

# ═══ 2D Animation ═════════════════════════════════════════════════════════

class Canva(anim.plane.canva):

  # ────────────────────────────────────────────────────────────────────────
  def __init__(self, window, **kwargs):

    super().__init__(window, **kwargs)

    self.item.dot = anim.plane.circle(
      position = [0.5,0.5],
      radius = 0.01,
      color = 'red'
    )
    

  # ────────────────────────────────────────────────────────────────────────
  def update(self, t):

    # Update timer display
    super().update(t)

    pass

# ═══ Main ═════════════════════════════════════════════════════════════════

import os
os.system('clear')

W = anim.window('Grid animation', display_information=False)

# Add animation
W.add(Canva, grid=True)

W.show()