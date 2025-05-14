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
                     boundaries = [[0,1],[0,1]],
                     display_boundaries = True,    
                     **kwargs)

    self.item.G = anim.plane.group(
      x = 0.2,
      y = 0.2,
      draggable = True,
      center_of_rotation = [0, 0]
    )

    self.item.rect = anim.plane.rectangle(
      group = self.item.G,
      Lx = 0.1,
      Ly = 0.3,
      fill = 'red',
    )

    # TO CHECK
    # zvalue

    self.item.rect2 = anim.plane.rectangle(
      group = self.item.G,
      Lx = 0.3, 
      Ly = 0.1,
      zvalue = 1
    )

    # self.item.rect.orientation = -0.05
    self.item.G.orientation = 0.1

    # print(self.item.rect.position)

    # self.item.rect.x = 0.5
    # self.item.rect.y = 0.5
    # self.item.rect.position = [0.5, 0.5]

  # ────────────────────────────────────────────────────────────────────────
  def update(self, t):

    # Update timer display
    super().update(t)

    # self.item['rect'].draggable = True

    # self.item['rect'].update()


    # Update position
    # self.item['rect'].height = self.h + t.step/100
    # self.item['rect'].position = [0, t.step/100]
    # self.item['rect'].position = [self.x0, self.y0 + t.step/10]

    # self.scene.setSceneRect(QRectF(0, 0, 10, 10))

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