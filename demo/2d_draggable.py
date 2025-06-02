'''
2D draggable demo
'''

import anim

# === 2D Animation =========================================================

class myAnimation(anim.plane.canva):

  # ────────────────────────────────────────────────────────────────────────
  def __init__(self, window):
    '''
    Items definitions
    '''

    super().__init__(window, boundaries=[[-1,1], [-1,1]])

    self.R = 0.6

    # ─── Zone

    self.item.zone = anim.plane.circle(
      radius = self.R,
      color = None,
      stroke = 'white',
      thickness = 0.005,
      linestyle = '--'
    )

    # ─── Disk

    self.item.disk = anim.plane.circle(
      radius = 0.1,
      color = 'green',
      draggable = True
    )

  # ────────────────────────────────────────────────────────────────────────
  def event(self, qitem, desc):
    '''
    Track changes
    '''
    
    if desc=='motion':

      pos = qitem.pos()
      x = pos.x()
      y = pos.y()

      if (x**2 + y**2) <= self.R**2:
        qitem.item.color = 'green'
      else:
        qitem.item.color = 'red'

# === Main =================================================================

W = anim.window('Draggable animation', display_information=False)

# Add animation
W.add(myAnimation)

# Prevent autoplay
W.autoplay = False

W.show()