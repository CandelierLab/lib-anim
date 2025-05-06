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
      # position = [0.5, 0.5],
      x = 0.5,
      y = 0.5,
      draggable = True,
    )

    self.item.rect = anim.plane.rectangle(
      parent = self.item.G,
      dimension = [0.2, 0.1]
    )

    self.item.rect2 = anim.plane.rectangle(
      parent = self.item.G,
      position = [0.1, 0.1],
      Lx = 0.3,
      Ly = 0.5,
      color = 'red'
    )

    # self.scene.addItem(self.item.rect)

    # self.add(anim.plane.rectangle, 'rect',
    #   position = [0.5, 0.5],
    #   width = 0.5,
    #   height = 0.5,
    #   draggable = True
    # )

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