import numpy as np
import anim

# === 2D Animation =========================================================

class myAnimation(anim.plane.canva):

  def __init__(self, W):

    super().__init__(W)

    # --- Colorbar

    self.colormap = anim.colormap()
    self.colormap.range = [-1,1]

    self.add(anim.plane.colorbar, 'Cb',
      colormap = self.colormap,
      position = [0.05, 0.1],
      height = 0.8,
      width = 0.01,
      nticks = 5
    )

    # --- Animation

    self.x0 = 0.5
    self.y0 = 0.5
    self.R = 0.25
    self.r = 0.01

    self.add(anim.plane.ellipse, 'E0',
      position = [self.x0, self.y0],
      major = 0.005,
      minor = 0.005,
      colors = ('white', None),
    )

    self.add(anim.plane.circle, 'C0',
      position = [self.x0, self.y0],
      radius = self.R,
      colors = (None, 'grey'),
      thickness = 2,
      linestyle = '--'
    )

    self.add(anim.plane.circle, 'C',
      position = [self.x0 + self.R, self.y0],
      radius = self.r,
      colors = (None, None),
      thickness = 5
    )

  # ========================================================================
  def update(self, t):
    
    # Update timer display
    super().update(t)

    x_ = np.cos(t.time)
    y_ = np.sin(t.time)

    # Update position
    x = self.x0 + self.R*x_
    y = self.y0 + self.R*y_
    self.item['C'].position = [x, y]

    # Update color
    self.item['C'].colors = (self.colormap.qcolor(x_), self.colormap.qcolor(y_))

# === Main =================================================================

W = anim.window('Colorbar')

# Add animation
W.add(myAnimation)


W.show()