'''
2D image array demo
'''

import numpy as np
import anim

# ═══ 2D Animation canva ═══════════════════════════════════════════════════

class Canva(anim.plane.canva):

  # ────────────────────────────────────────────────────────────────────────
  def __init__(self, window):

    # Number of channels (1 or 3)
    self.nchannel = 1

    # Number of pixels in the image
    self.npix = 500

    super().__init__(window, pixelperunit=self.npix)

    self.item.img = anim.plane.image(
      position = [0.5, 0.5],
      dimension = [1, 1],
      array = self.ripple(0),
      # colormap = anim.colormap('gnuplot', range=[-1, 1])
    )

  # ────────────────────────────────────────────────────────────────────────
  def ripple(self, t):

    # Base field
    x = np.linspace(-1, 1, self.npix)
    X, Y = np.meshgrid(x, x)
    base_field = (20 * X**2) + (20 * Y**2)

    match self.nchannel:

      case 1:
        ''' Single channel '''

        return np.sin(base_field - t/2/np.pi)

      case 3:
        ''' RGB channels '''

        R = np.sin(base_field - t/2/np.pi)
        G = np.sin(base_field - t/2/np.pi+np.pi/2)
        B = np.sin(base_field - t/2/np.pi+np.pi)
        
        return np.concatenate((R[:,:,None], G[:,:,None], B[:,:,None]), axis=2)

  # ────────────────────────────────────────────────────────────────────────
  def update(self, t):

    self.item.img.array = self.ripple(t.step)

    # Confirm update
    super().update(t)

# ═══ Main ═════════════════════════════════════════════════════════════════

W = anim.window('Image animation')

# Add animation
W.add(Canva)

# Allow backward animation
W.allow_backward = True
W.allow_negative_time = True

W.show()