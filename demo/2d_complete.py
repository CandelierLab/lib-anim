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

    self.item.A = anim.plane.arrow(
      points = [[0.1, 0.1], [0.4, 0.5], [0.3,0.7]],
      color = 'magenta',
      string = 0.18,
      head_shape = 'dart',
      head_location = 1,
      head_segment = 1,
      text_color = 'white',
      draggable = True,
    )

    # self.item.R = anim.plane.rectangle(
    #   position = [0.6, 0.4],
    #   dimension = [0.1, 0.2],
    #   center = [False, False]
    # )

    # self.item.T = anim.plane.text(
    #   string = 'ok',
    #   position = [0.5,0.5],
    #   fontsize = 0.11,
    # )

    # self.item.T2 = anim.plane.text(
    #   string = 'ok',
    #   position = [0.5,0.5],
    #   fontsize = 0.1,
    #   color = 'white'
    # )

    # self.item.T.fontsize = 0.15
    # self.item.A.points = [[0.5,0.5], [0.75,0.25]]
    
    # print(self.item.A.position)

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