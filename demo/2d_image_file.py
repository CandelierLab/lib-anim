'''
2D image file demo
'''

import numpy as np
import anim

# ═══ 2D Animation canva ═══════════════════════════════════════════════════

class Canva(anim.plane.canva):

  # ────────────────────────────────────────────────────────────────────────
  def __init__(self, window):

    super().__init__(window, pixelperunit=1000)

    self.period = 50

    self.item.img = anim.plane.image(
      file = 'demo/images/corgi.png',
      position = [0.5, 0.5],
      dimension = self.scale(0)
    )

  # ────────────────────────────────────────────────────────────────────────
  def scale(self, t):

    s = np.sin(t/self.period)/4 + 0.75
    return (s,s)

  # ────────────────────────────────────────────────────────────────────────
  def update(self, t):

    self.item.img.dimension = self.scale(t.step)

    # Confirm update
    super().update(t)

# ═══ Main ═════════════════════════════════════════════════════════════════

W = anim.window('Image animation')

# Add animation
W.add(Canva)

# Allow backward animation
W.allow_backward = True
W.allow_negative_time = True

W.show()