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

    self.item.rect = anim.plane.rectangle(
      x = 0.5,
      y = 0.5,
      Lx = 0.5,
      Ly = 0.5,
      center = True,
      draggable = True
    )
    
    # print(self.item.rect.qitem.__class__)

  # ────────────────────────────────────────────────────────────────────────
  def event(self, item, desc):

    p = self.item.rect.qitem.pos()
    
    print(self.item.rect.x + p.x(), self.item.rect.y + p.y())
    



# ═══ Main ═════════════════════════════════════════════════════════════════

import os
os.system('clear')

W = anim.window('Simple animation', display_information=False)

# Add animation
W.add(Canva)

W.autoplay = False
W.show()