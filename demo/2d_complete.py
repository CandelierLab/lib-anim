'''
Complete 2d demo
'''

import numpy as np
import anim

# ═══ 2D Animation ═════════════════════════════════════════════════════════

class Canva(anim.plane.canva):

  # ────────────────────────────────────────────────────────────────────────
  def __init__(self, window, **kwargs):

    super().__init__(window, 
                     boundaries = [[0, 1],[0,1]],
                     display_boundaries = True,    
                     **kwargs)

    # self.item.G = anim.plane.group(
    #   x = 0.5,
    #   y = 0.5,
    #   draggable = True,
    #   center_of_rotation = [0, 0]
    # )

    self.item.pth = anim.plane.path(
      points = [[0.1,0.9], [0.5,0.5], [0.9,0.9]]
    )
    
    # print(self.item.rect.qitem.__class__)

  # ────────────────────────────────────────────────────────────────────────
  def update(self, t):

    # Update timer display
    super().update(t)

# ═══ Main ═════════════════════════════════════════════════════════════════

import os
os.system('clear')

W = anim.window('Simple animation', display_information=False)

# Add animation
W.add(Canva, background_color='yellow')

# Allow backward animation
W.allow_backward = True
W.allow_negative_time = False

W.autoplay = False

W.show()