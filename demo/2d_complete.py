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

    self.item.line = anim.plane.line(
      x = 0.5,
      y = 0.5,
      Lx = 0.3,
      Ly = 0, 
      center = True,
      orientation = 0.2
    )

    # self.item.A = anim.plane.arrow(
    #   points = [[0.1,0.9], [0.5,0.5]],
    #   color = 'pink',
    #   string = '0.18',
    #   draggable = True
    # )
    
    # print(self.item.A.subitem.path.position)

  # ────────────────────────────────────────────────────────────────────────
  def update(self, t):

    # Update timer display
    super().update(t)

# ═══ Main ═════════════════════════════════════════════════════════════════

import os
os.system('clear')

W = anim.window('Simple animation', display_information=False)

# Add animation
W.add(Canva)

# Allow backward animation
W.allow_backward = True
W.allow_negative_time = False

W.autoplay = False

W.show()