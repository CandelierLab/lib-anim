from Animation.Window import *
from Animation.Animation_2d import *

# --- 2D Animation ---------------------------------------------------------

class Anim(Animation_2d):

  def __init__(self, W):

    super().__init__(W)

    self.npix = 500

    self.add(image, 'background',
      image = self.ripple(0),
      cmap = Colormap('gnuplot', range=[-1, 1]),
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

# --- Main -----------------------------------------------------------------

if __name__ == "__main__":

  W = Window('Image animation')
  W.add(Anim(W))

  W.show()