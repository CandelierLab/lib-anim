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

    self.item.G = anim.plane.group(
      x = 0.5,
      y = 0.5,
      draggable = True,
      center_of_rotation = [0, 0]
    )

    sz = 0.1

    self.item.rect = anim.plane.rectangle(
      group = self.item.G,
      x = 0,
      y = 0,
      Lx = 0.5,
      Ly = sz,
      center = True
    )

    self.item.rect2 = anim.plane.rectangle(
      group = self.item.G,
      x = 0,
      y = 0,
      Lx = 0.01,
      Ly = sz,
      fill = 'yellow',
      zvalue = 1
    )

    self.item.text = anim.plane.text(
      x = 0.5,
      y = 0.5,
      fontsize = sz,
      string = 'RRR<br>WWW',
      color = 'red',
      style = 'html { background-color: yellow; }',
      zvalue = 10,
      center = True
    )

  # ────────────────────────────────────────────────────────────────────────
  def update(self, t):

    # Update timer display
    super().update(t)

    print(self.item.text.qitem.boundingRect())


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