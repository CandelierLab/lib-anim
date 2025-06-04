'''
2D colorbar array demo
'''

import numpy as np
import anim

# ═══ 2D Animation canva ═══════════════════════════════════════════════════

class Canva(anim.plane.canva):

  # ────────────────────────────────────────────────────────────────────────
  def __init__(self, window, cmap):

    # Number of pixels in the image
    self.npix = 500

    # Colormap
    self.cmap = cmap

    super().__init__(window,
                     display_boundaries = False,
                     pixelperunit = self.npix)

    # ─── display

    self.item.img = anim.plane.image(
      position = [0.5, 0.5],
      dimension = [1, 1],
      array = self.phase(0),
      colormap = self.cmap
    )

  # ────────────────────────────────────────────────────────────────────────
  def phase(self, t):

    # Base field
    x = np.linspace(-0.5, 0.5, self.npix)
    X, Y = np.meshgrid(x, x)
    return np.angle(np.exp(t/(X + 1j*Y)/10))/np.pi

  # ────────────────────────────────────────────────────────────────────────
  def update(self, t):

    self.item.img.array = self.phase(t.step)

    # Confirm update
    super().update(t)

# ═══ Main ═════════════════════════════════════════════════════════════════

W = anim.window('Colorbar animation')

# colormap
cmap = anim.colormap('turbo', range=[-1, 1])

# ─── Information panel

W.information.display(True)

# This may be useful to setup the information canva dimensions
# W.information.canva.display_boundaries = True

# Set boundaries size
W.information.canva.boundaries = [[0,1],[0,3]]

W.information.canva.item.cbar = anim.plane.colorbar(
  position = [0.8, 1],
  dimension = [0.2, 2],
  colormap = cmap,
  ticks_number = 5,
  ticks_fontsize = 0.1,
  ticks_color = '#AAA'
)

# Add animation
W.add(Canva, cmap=cmap)

# Allow backward animation
W.allow_backward = True
W.allow_negative_time = True

W.show()