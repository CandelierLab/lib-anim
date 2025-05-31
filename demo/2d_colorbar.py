'''
2D colorbar array demo
'''

import numpy as np
import anim

# ═══ 2D Animation ═════════════════════════════════════════════════════════

class Canva(anim.plane.canva):

  # ────────────────────────────────────────────────────────────────────────
  def __init__(self, window):

    # Number of pixels in the image
    self.npix = 1000

    # Colormap
    self.cmap = anim.colormap('magma', range=[-1, 1])

    super().__init__(window,
                     display_boundaries = False,
                     pixelperunit = self.npix)

    # ─── display

    self.item.img = anim.plane.image(
      position = [0.57, 0.5],
      dimension = [0.8, 0.8],
      array = self.phase(0),
      colormap = self.cmap
    )

    # ─── colorbar

    self.item.cbar = anim.plane.colorbar(
      position = [0.1, 0.5],
      dimension = [0.05, 0.4],
      colormap = self.cmap,
      ticks_number = 5,
    )

  # ────────────────────────────────────────────────────────────────────────
  def phase(self, t):

    # Base field
    x = np.linspace(-0.5, 0.5, self.npix)
    X, Y = np.meshgrid(x, x)
    return np.angle(np.exp(t/(X + 1j*Y)/10))/np.pi

  # ────────────────────────────────────────────────────────────────────────
  def update(self, t):

    # Update timer display
    super().update(t)

    self.item.img.array = self.phase(t.step)

# ═══ Main ═════════════════════════════════════════════════════════════════

import os
os.system('clear')

W = anim.window('Colorbar animation', display_information=False)

# Add animation
W.add(Canva)

# Allow backward animation
W.allow_backward = True
W.allow_negative_time = True

W.show()