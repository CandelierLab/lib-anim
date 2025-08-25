'''
3D demo
'''

import os
import numpy as np
from PyQt6.Qt3DExtras import QSphereMesh

import anim

os.system('clear')

# ═══ 3D Animation canva ═══════════════════════════════════════════════════

class Canva(anim.volume.canva):

  # ────────────────────────────────────────────────────────────────────────
  def __init__(self, window):

    super().__init__(window)

    self.item.S = anim.volume.sphere(radius=5)

  # ────────────────────────────────────────────────────────────────────────
  def update(self, t):

    # Confirm update
    super().update(t)

    self.item.S.radius = np.sin(t.step/30)*3+5

# ═══ Main ═════════════════════════════════════════════════════════════════

W = anim.window('3D demo')

# Add animation
W.add(Canva)

W.information.display(True)

# Allow backward animation
# W.allow_backward = True
# W.allow_negative_time = True

# W.autoplay = False

# Display
W.show()