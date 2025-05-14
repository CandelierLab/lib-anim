'''
2D text demo
'''

import numpy as np
import anim

# ═══ 2D Animation ═════════════════════════════════════════════════════════

class Canva(anim.plane.canva):

  # ────────────────────────────────────────────────────────────────────────
  def __init__(self, window, **kwargs):

    super().__init__(window, **kwargs)

    self.item.time_dispay = anim.plane.text(
      x = 0.5,
      y = 0.5,
      fontsize = 0.1,
      string = '',
      color = 'darkblue',
      style = 'html { background-color: lightblue; }',
    )

  # ────────────────────────────────────────────────────────────────────────
  def update(self, t):

    # Update timer display
    super().update(t)

    self.item.time_dispay.string = f't = {t.step}'

    self.item.time_dispay.x = (np.sin(t.step/20) + 1)*0.3  + 0.2
    self.item.time_dispay.y = (np.cos(t.step/33) + 1)*0.2  + 0.3
    self.item.time_dispay.orientation = t.step/50

# ═══ Main ═════════════════════════════════════════════════════════════════

import os
os.system('clear')

W = anim.window('2D text demo', display_information=False)

# Add animation
W.add(Canva)

# Allow backward animation
W.allow_backward = True
W.allow_negative_time = True

# Display
W.show()