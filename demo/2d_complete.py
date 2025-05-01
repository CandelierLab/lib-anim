'''
Complete 2d demo
'''

import numpy as np
import anim

# ═══ 2D Animation ═════════════════════════════════════════════════════════

class myAnimation(anim.plane.panel):

  # ────────────────────────────────────────────────────────────────────────
  def __init__(self, window, **kwargs):

    super().__init__(window, 
                     boundaries = [[0,1],[0,1]],
                     display_boundaries = True,
                     padding = 0,                     
                     **kwargs)

    self.add(anim.plane.rectangle, 'rect',
      position = [0, 0],
      width = 0.5,
      height = 0.2,
      color = 'cyan',
    )

    self.add(anim.plane.rectangle, 'rect2',
      position = [0.5, 0.5],
      width = 0.2,
      height = 0.5,
      color = 'green',
    )

    # self.item['rect'].stroke = 'red'
    # self.item['rect'].linestyle = '--'

  # ────────────────────────────────────────────────────────────────────────
  def update(self, t):

    # Update timer display
    super().update(t)

    # Update position
    # self.item['rect'].height = self.h + t.step/100
    self.item['rect'].position = [self.x0, self.y0 + t.step/10]
    # self.item['rect'].position = [self.x0, self.y0 + t.step/10]

    # self.scene.setSceneRect(QRectF(0, 0, 10, 10))


# ═══ Main ═════════════════════════════════════════════════════════════════

import os
os.system('clear')

W = anim.window('Simple animation', display_information=False)

# Add animation
W.add(myAnimation)

# Allow backward animation
W.allow_backward = True
W.allow_negative_time = False

W.autoplay = False

W.show()