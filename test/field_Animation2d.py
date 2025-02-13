from Animation.Window import *
from Animation.Animation_2d import *

# --- 2D Animation ---------------------------------------------------------

class Anim(Animation_2d):

  def __init__(self, W):

    super().__init__(W)

    self.add(field, 'background',
      field = self.ripple(0),
      cmap = Colormap('gnuplot', range=[-1, 1]),
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

# --- Main -----------------------------------------------------------------

if __name__ == "__main__":

  W = Window('Field animation')
  W.add(Anim(W))

  W.show()