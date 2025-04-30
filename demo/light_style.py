import numpy as np
import anim, anim.plane as a2d

# === 2D Animation =========================================================

class myAnimation(a2d.panel):

  def __init__(self, W):

    super().__init__(W, boundaries=[[0,1],[0,1]])

    self.padding=0.01

    self.x0 = 0.5
    self.y0 = 0.5
    self.R = 0.25
    self.r = 0.01

    self.add(a2d.ellipse, 'E0',
      position = [self.x0, self.y0],
      major = 0.005,
      minor = 0.005,
      colors = ('white', None),
    )

    self.add(a2d.circle, 'C0',
      position = [self.x0, self.y0],
      radius = self.R,
      colors = (None, 'grey'),
      thickness = 2,
      linestyle = '--'
    )

    self.add(a2d.circle, 'C',
      position = [self.x0 + self.R, self.y0],
      radius = self.r,
      colors = ('red', None),
    )

    self.add(a2d.text, 'T',
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

# === Main =================================================================

W = anim.window('Light style', style='light')

W.add(myAnimation)

W.show()