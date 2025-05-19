'''
2D image file demo
'''

import numpy as np
import anim

# ═══ 2D Animation ═════════════════════════════════════════════════════════

class Canva(anim.plane.canva):

  # ────────────────────────────────────────────────────────────────────────
  def __init__(self, window):

    super().__init__(window, pixelperunit=1000)

    self.period = 50

    self.item.img = anim.plane.image(
      file = 'demo/images/corgi.png',
      position = [0.5, 0.5],
      dimension = [0.2, 0.2]
    )

  # ────────────────────────────────────────────────────────────────────────
  def update(self, t):

    # Update timer display
    super().update(t)

    scale = np.sin(t.step/self.period)/4 + 0.75
    self.item.img.dimension = (scale, scale)

# ═══ Main ═════════════════════════════════════════════════════════════════

import os
os.system('clear')

W = anim.window('Image animation', display_information=False)

# Add animation
W.add(Canva)

# Allow backward animation
W.allow_backward = True
W.allow_negative_time = True

W.show()