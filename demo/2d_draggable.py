import numpy as np
import anim

# === 2D Animation =========================================================

class myAnimation(anim.plane.panel):

  def __init__(self, window):
    '''
    Items definitions
    '''

    super().__init__(window, boundaries=[[0,1],[0,1]])

    self.x0 = 0.5
    self.y0 = 0.5
    self.R = 0.25
    self.r = 0.05

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
      linestyle = '--',
      zvalue = 2
    )

    self.add(anim.plane.circle, 'C',
      position = [self.x0 + self.R, self.y0 + self.R],
      radius = self.r,
      colors = ('red', None),
      draggable = True,
    )

  def change(self, type, item):
    '''
    Track changes
    '''
    
    if type=='move':

      pos = item.pos()
      x = item.scene2x(pos.x())
      y = item.scene2y(pos.y())
      if ((x-self.x0)**2 + (y-self.y0)**2) <= self.R**2:
        item.colors = ('green', None)
      else:
        item.colors = ('red', None)

# === Main =================================================================

W = anim.window('Simple draggable animation', display_information=False)

# Add animation
W.add(myAnimation)

# Prevent autoplay
W.autoplay = False

W.show()