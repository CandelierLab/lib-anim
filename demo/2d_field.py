import numpy as np
import anim

# === 2D Animation =========================================================

class myAnimation(anim.plane.canva):

  def __init__(self, W):

    super().__init__(W)

    self.add(anim.plane.field, 'background',
      field = self.ripple(0),
      cmap = anim.colormap('gnuplot', range=[-1, 1]),
      zvalue = -1,
    )

  def ripple(self, t):
    x = np.linspace(-1, 1, 500)
    X, Y = np.meshgrid(x, x)
    return np.sin((20 * X ** 2) + (20 * Y ** 2) - t/2/np.pi)

  def update(self, t):

    # Update timer display
    super().update(t)

    self.item['background'].field = self.ripple(t.step)

# === Main =================================================================

W = anim.window('Simple animation')

# Add animation
W.add(myAnimation)

# Allow backward animation
W.allow_backward = True
W.allow_negative_time = True

W.show()