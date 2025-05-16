'''
2D line demo
'''

import numpy as np
import anim

# ═══ 2D Animation ═════════════════════════════════════════════════════════

class Canva(anim.plane.canva):

  # ────────────────────────────────────────────────────────────────────────
  def __init__(self, window, **kwargs):

    super().__init__(window)

    # ─── Definitions

    # Number of lines
    self.N = 20

    # x-positions
    self.X = np.linspace(0.1, 0.9, self.N)

    # ─── Items

    Y = self.generate(0)

    for i in range(self.N):
      self.item[f'line_{i}'] = anim.plane.line(
        points = [[self.X[i], 0.5-Y[i]/4], [self.X[i], 0.5+Y[i]]],
        color = 'white'
      )

  # ────────────────────────────────────────────────────────────────────────
  def generate(self, t):

    return np.sin(self.X*10+ t/10)/4

  # ────────────────────────────────────────────────────────────────────────
  def update(self, t):

    # Update timer display
    super().update(t)

    Y = self.generate(t.step)
    for i in range(self.N):
      self.item[f'line_{i}'].points = [[self.X[i], 0.5-Y[i]/4], [self.X[i], 0.5+Y[i]]]

# ═══ Main ═════════════════════════════════════════════════════════════════

import os
os.system('clear')

W = anim.window('Simple animation', display_information=False)

# Add animation
W.add(Canva)

# Allow backward animation
W.allow_backward = True
W.allow_negative_time = True

W.show()