import numpy as np
import animate

# === 2D Animation =========================================================

class myAnimation(animate.plane.view):

  def __init__(self, W):

    super().__init__(W)

    self.npix = 500

    self.add(animate.plane.image, 'background',
      image = self.ripple(0),
      cmap = animate.colormap('gnuplot', range=[-1, 1]),
      zvalue = -1,
    )

  def ripple(self, t):
    x = np.linspace(-1, 1, self.npix)
    X, Y = np.meshgrid(x, x)

    R = (np.sin((20 * X ** 2) + (20 * Y ** 2) - t/2/np.pi)+1)/2
    G = (np.sin((20 * X ** 2) + (20 * Y ** 2) - t/2/np.pi+np.pi/2)+1)/2
    B = (np.sin((20 * X ** 2) + (20 * Y ** 2) - t/2/np.pi+np.pi)+1)/2
    
    return np.concatenate((R[:,:,None], G[:,:,None], B[:,:,None]), axis=2)

  def update(self, t):

    # Update timer display
    super().update(t)

    self.item['background'].image = self.ripple(t.step)

# === Main =================================================================

W = animate.window('Simple animation')

# Add animation
W.add(myAnimation)

W.show()