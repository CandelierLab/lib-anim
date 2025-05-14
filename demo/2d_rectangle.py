'''
2D rectangle demo
'''

import numpy as np
import matplotlib as mpl
import anim

# ═══ 2D Animation ═════════════════════════════════════════════════════════

class Canva(anim.plane.canva):

  # ────────────────────────────────────────────────────────────────────────
  def __init__(self, window, **kwargs):

    super().__init__(window, **kwargs)

    self.item.rect_0 = anim.plane.rectangle(
      position = [0.5, 0.5],
      dimension = [0, 0]
    )

    self.colormap = mpl.colormaps['hsv'].resampled(100)

  # ────────────────────────────────────────────────────────────────────────
  def update(self, t):

    # Update timer display
    super().update(t)

    # Geometry
    self.item.rect_0.Lx = (np.sin(t.step/10) + 1)*0.3  + 0.2
    self.item.rect_0.Ly = (np.cos(t.step/23) + 1)*0.2  + 0.3
    self.item.rect_0.orientation = t.step/40

    # Color
    self.item.rect_0.color = self.colormap(t.step % self.colormap.N)

# ═══ Main ═════════════════════════════════════════════════════════════════

import os
os.system('clear')

W = anim.window('2D rectangle demo', display_information=False)

# Add animation
W.add(Canva)

# Allow backward animation
W.allow_backward = True
W.allow_negative_time = True

# Display
W.show()