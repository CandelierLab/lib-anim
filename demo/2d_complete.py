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
                     boundaries = [[0,100],[0,100]],
                     display_boundaries = True,
                     padding = 0,                     
                     **kwargs)

    self.add(anim.plane.rectangle, 'rect',
      position = [50, 50],
      width = 50,
      height = 50,
    )

    # self.add(anim.plane.rectangle, 'rect2',
    #   position = [0.5, 0.5],
    #   width = 0.2,
    #   height = 0.5,
    #   color = 'green',
    #   zvalue = -1
    # )

  # ────────────────────────────────────────────────────────────────────────
  def update(self, t):

    # Update timer display
    super().update(t)

    self.item['rect'].draggable = True

    # self.item['rect'].update()


    # Update position
    # self.item['rect'].height = self.h + t.step/100
    # self.item['rect'].position = [0, t.step/100]
    # self.item['rect'].position = [self.x0, self.y0 + t.step/10]

    # self.scene.setSceneRect(QRectF(0, 0, 10, 10))

  # ────────────────────────────────────────────────────────────────────────
  def change(self, type, item):
    
    print(type, item)

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