'''
2D arrow demo
'''

import types
import datetime
import numpy as np
import anim

# ═══ 2D Animation canva ═══════════════════════════════════════════════════

class Canva(anim.plane.canva):

  # ────────────────────────────────────────────────────────────────────────
  def __init__(self, window):

    super().__init__(window, boundaries=[[-1,1], [-1,1]])

    D = self.data()

    # ─── Hours

    self.item.hours = anim.plane.arrow(
        points = D.hp,
        string = D.h,
        thickness = 0.02,
        color = 'white',
        text_location = 0.70,
      )
    
    # ─── Minutes

    self.item.minutes = anim.plane.arrow(
        points = D.mp,
        string = D.m,
        thickness = 0.015,
        color = 'white',
        text_location = 0.85,
      )
    
    # ─── Seconds

    self.item.seconds = anim.plane.arrow(
        points = D.sp,
        string = D.s,
        thickness = 0.01,
        color = 'red',        
        head_shape = 'disk',
        head_location = 0.75,
        text_location = 0.95,
      )

    # ─── Decorations

    self.item.center = anim.plane.circle(
      radius = 0.03 
    )

    r = 0.75
    for i in range(12):
     a = i*np.pi/6
     self.item[f'marker_{i}'] = anim.plane.line(
      position = [r*np.cos(a), r*np.sin(a)],
      dimension = [0.2, 0],
      orientation = a,
      zvalue = -1
    ) 
    
  # ────────────────────────────────────────────────────────────────────────
  def data(self):

    D = types.SimpleNamespace()

    now = datetime.datetime.now()
    D.h = now.hour
    D.m = now.minute
    D.s = now.second

    D.hp = [[0,0], [-0.5*np.sin(-D.h/6*np.pi), 0.5*np.cos(-D.h/6*np.pi)]]
    D.mp = [[0,0], [-0.9*np.sin(-D.m/30*np.pi), 0.9*np.cos(-D.m/30*np.pi)]]
    D.sp = [[0,0], [-0.9*np.sin(-D.s/30*np.pi), 0.9*np.cos(-D.s/30*np.pi)]]

    return D

  # ────────────────────────────────────────────────────────────────────────
  def update(self, t):

    D = self.data()
    
    self.item.hours.string = D.h
    self.item.hours.points = D.hp

    self.item.minutes.string = D.m
    self.item.minutes.points = D.mp

    self.item.seconds.string = D.s
    self.item.seconds.points = D.sp

    # Confirm update
    super().update(t)

# ═══ Main ═════════════════════════════════════════════════════════════════

W = anim.window('Arrow animation')

# Add animation
W.add(Canva)

W.show()