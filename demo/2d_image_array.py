'''
2D image array demo
'''

import numpy as np
import anim

# ═══ 2D Animation ═════════════════════════════════════════════════════════

class Canva(anim.plane.canva):

  # ────────────────────────────────────────────────────────────────────────
  def __init__(self, window):

    super().__init__(window, boundaries=[[0,100],[0,100]])

    self.npix = 500

    self.item.img = anim.plane.image(
      position = [0.5, 0.5],
      dimension = [100, 100],
      file = 'demo/images/corgi.png',
      # colormap = anim.colormap('gnuplot', range=[-1, 1])
    )

    # print(self.item.img.qitem.pixmap().data)

  # ────────────────────────────────────────────────────────────────────────
  def ripple(self, t):

    x = np.linspace(-1, 1, self.npix)
    X, Y = np.meshgrid(x, x)

    R = (np.sin((20 * X ** 2) + (20 * Y ** 2) - t/2/np.pi)+1)/2
    G = (np.sin((20 * X ** 2) + (20 * Y ** 2) - t/2/np.pi+np.pi/2)+1)/2
    B = (np.sin((20 * X ** 2) + (20 * Y ** 2) - t/2/np.pi+np.pi)+1)/2
    
    return np.concatenate((R[:,:,None], G[:,:,None], B[:,:,None]), axis=2)

  # ────────────────────────────────────────────────────────────────────────
  def update(self, t):

    # Update timer display
    super().update(t)

    # self.item.img.array = self.ripple(t.step)

# ═══ Main ═════════════════════════════════════════════════════════════════

import os
os.system('clear')

W = anim.window('Image animation', display_information=False)

# Add animation
W.add(Canva)

# Allow backward animation
W.allow_backward = True
W.allow_negative_time = True

W.autoplay = False

W.show()