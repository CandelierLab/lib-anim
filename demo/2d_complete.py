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

    from PyQt6.QtCore import Qt
    from PyQt6.QtWidgets import QGraphicsItemGroup, QGraphicsRectItem
    from PyQt6.QtGui import QColor, QPen, QBrush

    # G = QGraphicsItemGroup()
    # print(G.__dict__)
    # G.setPos(0.5, 0.5)
    # self.scene.addItem(G)

    self.item.G = anim.plane.group(
      x = 0,
      y = 0,
      draggable = False,
    )

    self.item.rect = anim.plane.rectangle(
      parent = self.item.G,
      position = [0, 0],
      Lx = 0.5,
      Ly = 0.5,
      fill = 'red'
    )

    R = QGraphicsRectItem()
    R.setBrush(QBrush(QColor('cyan')))
    R.setPen(QPen(Qt.PenStyle.NoPen))
    R.setRect(0.1, 0.1, 0.2, 0.2)

    # self.scene.addItem(R)
    R.setParentItem(self.item.G)


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