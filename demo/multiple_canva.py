'''
Multiple canvas demo

NB: This demo requires to install pytz
pip install pytz
'''

import os
import types
import datetime
import pytz
import numpy as np
import anim

# ═══ 2D Animation ═════════════════════════════════════════════════════════

class clock(anim.plane.canva):

  # ────────────────────────────────────────────────────────────────────────
  def __init__(self, window, city):

    # Parent constructor
    super().__init__(window, 
                     boundaries=[[-1,1], [-1,1.5]],
                     display_boundaries = False)

    # Timezone
    self.timezone = pytz.timezone(city) 

    # Fetch time
    D = self.data()

    # ─── Hours

    self.item.hours = anim.plane.line(
        position = [0,0],
        dimension = [0,0.5],
        thickness = 0.03,
        color = 'white'
      )
    
    # ─── Minutes

    self.item.minutes = anim.plane.line(
        position = [0,0],
        dimension = [0, 1],
        thickness = 0.015,
        color = 'white'
      )
    
    # ─── Seconds

    self.item.seconds = anim.plane.line(
        position = [0,0],
        dimension = [0,1],
        thickness = 0.01,
        color = 'red'
      )
    
    # ─── City name

    self.item.city = anim.plane.text(
      position = [0,1.2],
      string = os.path.basename(city).replace('_', ' '),
      fontsize = 0.2,
      color = 'white'
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

    now = datetime.datetime.now(self.timezone)
    D.m = now.minute
    D.s = now.second

    D.ha = -now.hour/6*np.pi
    D.ma = -now.minute/30*np.pi
    D.sa = -now.second/30*np.pi

    return D

  # ────────────────────────────────────────────────────────────────────────
  def update(self, t):

    # Update timer display
    super().update(t)

    D = self.data()
    
    self.item.hours.orientation = D.ha
    self.item.minutes.orientation = D.ma
    self.item.seconds.orientation = D.sa

# ═══ Main ═════════════════════════════════════════════════════════════════

import os
os.system('clear')

W = anim.window('Multiple canvas',
                height = 0.5,
                aspect_ratio = 3)

# Add animation
W.add(clock, city='America/New_York')
W.add(clock, city='Europe/Paris')
W.add(clock, city='Asia/Singapore')

W.show()