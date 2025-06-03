'''
Information panel demo
'''

import numpy as np
import anim

# ═══ 2D Animation canva ═══════════════════════════════════════════════════

class Canva(anim.plane.canva):

  # ────────────────────────────────────────────────────────────────────────
  def __init__(self, window):

    super().__init__(window, pixelperunit=1000)

    self.period = 50

    self.item.img = anim.plane.image(
      file = 'demo/images/corgi.png',
      position = [0.5, 0.5],
      dimension = self.scale(0)
    )

    # Initial informations
    self.window.information.html = self.html()

  # ────────────────────────────────────────────────────────────────────────
  def scale(self, t):

    sx = np.sin(t/self.period)/4 + 0.75
    sy = np.sin(t/self.period*np.pi)/4 + 0.75
    return (sx,sy)
  
  # ────────────────────────────────────────────────────────────────────────
  def html(self):

    s = f'<p>Image width: {self.item.img.Lx:.03f}</p>'
    s += f'<p>Image height: {self.item.img.Ly:.03f}</p>'

    return s

  # ────────────────────────────────────────────────────────────────────────
  def update(self, t):

    # Update image
    self.item.img.dimension = self.scale(t.step)

    # Update information
    self.window.information.html = self.html()

    # Confirm update
    super().update(t)

# ═══ Main ═════════════════════════════════════════════════════════════════

W = anim.window('Animation with information panel')

W.information.display(True)

# Add animation
W.add(Canva)

# Allow backward animation
W.allow_backward = True
W.allow_negative_time = True

W.autoplay = False

W.show()