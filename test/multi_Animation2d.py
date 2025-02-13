from Animation.Window import *
from Animation.Animation_2d import *

# === Animation ============================================================

class Anim(Animation_2d):

  def __init__(self, W, color):

    super().__init__(W)

    self.padding = 0.01

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
      colors = (color, None),
    )

  def update(self, t):
    
    # Update timer display
    super().update(t)

    # Update position
    x = self.x0 + self.R*np.cos(t.time)
    y = self.y0 + self.R*np.sin(t.time)
    self.item['C'].position = [x, y]

# === Main =================================================================

if __name__ == "__main__":

  W = Window(display_information=True)

  W.title = 'Multiple animation'

  W.add(Anim(W, 'red'))
  W.add(Anim(W, 'green'))

  W.show()
