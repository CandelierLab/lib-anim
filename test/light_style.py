from Animation.Window import *
from Animation.Animation_2d import *

# --- 2D Animation ---------------------------------------------------------

class Anim(Animation_2d):

  def __init__(self, W):

    super().__init__(W, boundaries=[[0,1],[0,1]])

    self.padding=0.01

    self.x0 = 0.5
    self.y0 = 0.5
    self.R = 0.25
    self.r = 0.01

    self.add(ellipse, 'E0',
      position = [self.x0, self.y0],
      major = 0.005,
      minor = 0.005,
      colors = ('white', None),
    )

    self.add(circle, 'C0',
      position = [self.x0, self.y0],
      radius = self.R,
      colors = (None, 'grey'),
      thickness = 2,
      linestyle = '--'
    )

    self.add(circle, 'C',
      position = [self.x0 + self.R, self.y0],
      radius = self.r,
      colors = ('red', None),
    )

    self.add(text, 'T',
      position = [0.5, 0.53],
      string = 'a&#946;c',
      fontsize = 25,
      center = True
    )

  def update(self, t):
        # Update timer display
    super().update(t)

    # Update position
    x = self.x0 + self.R*np.cos(t.time)
    y = self.y0 + self.R*np.sin(t.time)
    self.item['C'].position = [x, y]

# --- Main -----------------------------------------------------------------

if __name__ == "__main__":

  W = Window('Simple animation', style='light')
  W.add(Anim(W))

  W.show()